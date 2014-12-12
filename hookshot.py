#!/home/pspeter3/hookshot/venv/bin/python
import forecast
import influxdb
import ninja

def main():
  points = []
  points.append(forecast.data())
  points.append(ninja.data())
  influxdb.write(points)

if __name__ == '__main__':
  main()
