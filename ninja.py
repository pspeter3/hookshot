import conversions
import requests
import os

def data(token = None, whitelist = None):
  if token is None:
    token = os.getenv("NINJA_TOKEN")
  if whitelist is None:
    whitelist = set(os.getenv("NINJA_GUIDS").split(","))
  response = requests.get("https://api.ninja.is/rest/v0/devices", params={
    "user_access_token": token
  })
  payload = response.json()
  data = {
    "name": "ninja",
    "time_precision": "ms",
    "columns": [],
    "points": []
  }
  has_time = False
  for guid, status in payload.get("data", {}).iteritems():
    if guid in whitelist:
      last_data = status.get("last_data", {})
      type = status.get("device_type", guid)
      value = last_data.get("DA")
      if not has_time:
        data["columns"].append("time")
        data["points"].append(last_data.get("timestamp"))
        has_time = True
      if type == "temperature":
        value = conversions.temperature(value)
      data["columns"].append(type)
      data["points"].append(value)
  data["points"] = [data["points"]]
  return data
