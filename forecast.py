import re
import requests
import os

def _convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def data(token=None, lat_lon=None):
  if token is None:
    token = os.getenv("FORECAST_TOKEN")
  if lat_lon is None:
    lat_lon = os.getenv("FORECAST_LAT_LON")
  response = requests.get(
    "https://api.forecast.io/forecast/%s/%s" %(token, lat_lon))
  payload = response.json()
  data = {
    "name": "forecast",
    "columns": [],
    "points": []
  }
  for key, value in payload.get("currently", {}).iteritems():
    if key is not "icon" and key is not "summary":
      data["columns"].append(_convert(key))
      data["points"].append(value)
  data["points"] = [data["points"]]
  return data
