import json
import requests
import os

def write(points, base_url=None, database=None, user=None, password=None):
  if base_url is None:
    base_url = os.getenv("INFLUXDB_BASE_URL", "http://localhost:8086")
  if database is None:
    database = os.getenv("INFLUXDB_DATABASE", "hookshot")
  if user is None:
    user = os.getenv("INFLUXDB_USER", "root")
  if password is None:
    password = os.getenv("INFLUXDB_PASSWORD", "root")
  url = "%s/db/%s/series?u=%s&p=%s" %(base_url, database, user, password)
  data = json.dumps(points)
  print "curl -X POST -d '%s' '%s'" %(data, url)
  requests.post(url, data=data)