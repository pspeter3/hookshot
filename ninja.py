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
  points = []
  for guid, status in payload.get("data", {}).iteritems():
    if guid in whitelist:
      data = status.get("last_data", {})
      type = status.get("device_type", guid)
      value = data.get("DA")
      timestamp = data.get("timestamp") / 1000.
      if type in transforms:
        value = transforms[type](value)
      points.append([timestamp, type, value])
  return {
    "name": "ninja",
    "columns": ["time", "type", "value"],
    "points": points
  }
)