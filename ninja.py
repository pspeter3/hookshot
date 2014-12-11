from influxdb import client as influxdb
import requests
import os

DEVICES_URL = "https://api.ninja.is/rest/v0/devices"
TOKEN_KEY = "user_access_token"
DATA_KEY = "DA"
TIMESTAMP_KEY = "timestamp"

TRANSFORMS = {
  "temperature": lambda x: ((9 * x)/ 5.) + 32
}

def device_data(req, token, whitelist):
  params = {}
  params[TOKEN_KEY] = token
  res = req.get(DEVICES_URL, params=params)
  payload = res.json()
  points = []
  for guid, status in payload.get("data", {}).iteritems():
    if guid in whitelist:
      data = status.get("last_data", {})
      if DATA_KEY in data and TIMESTAMP_KEY in data:
        type = status.get("device_type", guid)
        value = data.get(DATA_KEY)
        timestamp = data.get(TIMESTAMP_KEY)
        if type in TRANSFORMS:
          value = TRANSFORMS[type](value)
        points.append([type, value, timestamp])
  return points

def main(req, token, whitelist, client):
  points = device_data(req, token, whitelist)
  data = {
    "name": "ninja",
    "columns": ["type", "value", "time"],
    "points": points
  }
  client.write_points(data)

if __name__ == '__main__':
  token = os.environ.get("NINJA_ACCESS_TOKEN")
  whitelist = set(os.environ.get("NINJA_GUIDS").split(","))
  client = influxdb.InfluxDBClient(username=os.environ.get("INFLUXDB_USERNAME"),
    password=os.environ.get("INFLUXDB_PASSWORD"), 
    database=os.environ.get("INFLUXDB_DB"))
  main(requests, token, whitelist, client)