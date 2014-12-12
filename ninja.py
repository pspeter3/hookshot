import requests
import os

transforms = {
  "temperature": lambda x: ((9 * x)/ 5.) + 32
}

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
      data = status.get("last_data", {})
      type = status.get("device_type", guid)
      value = data.get("DA")
      if not has_time:
        data["columns"].append("time")
        data["points"].append(data.get("timestamp"))
      if type in transforms:
        value = transforms[type](value)
      data["columns"].append(type)
      data["points"].append(value)
  return data
