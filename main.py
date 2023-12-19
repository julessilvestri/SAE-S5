import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import csv

bucket = "IUT_BUCKET"
org = "INFO"
token = "q4jqYhdgRHuhGwldILZ2Ek1WzGPhyctQ3UgvOII-bcjEkxqqrIIacgePte33CEjekqsymMqWlXnO0ndRhLx19g=="

url = "http://51.83.36.122:8086/"

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

query_api = client.query_api()


sensorQuery = 'from(bucket: "' + bucket +'")\
    |> range(start:-2d)\
    |> filter(fn: (r) => r["_field"] == "value")\
    |> distinct(column: "entity_id")\
    |> group(columns: ["entity_id"], mode:"by")'

sensorResult = query_api.query(org=org, query=sensorQuery)

sensorResults = []
for table in sensorResult:
  for record in table.records:
    sensorResults.append(
        record.values.get("entity_id")
    )

i = 0
for s in sensorResults :
   print(str(i) + " => " + str(s))
   i += 1

entity = int(input("Capteur : "))

sensor = sensorResults[entity]
print(sensor)

query = 'from(bucket: "' + bucket +'")\
 |> range(start:-2d)\
 |> filter(fn: (r) => r["entity_id"] == "' + sensor + '")\
 |> filter(fn: (r) => r["_field"] == "value")\
 |> filter(fn: (r) => r["_measurement"] == "°C")'

result = query_api.query(org=org, query=query)

results = []
for table in result:
  for record in table.records:
    state = ""
    if record.get_value() < 18 :
       state = 'inconfortable'
    results.append((
       record.get_field(), 
       record.get_value(), 
       record.get_measurement(),
       record.get_time(),
       state
    ))

csv_file_path = 'exported_data.csv'

with open(csv_file_path, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['_field', '_value', '_measurement', '_time', '_state'])
    csv_writer.writerows(results)

print(f'Data exported to {csv_file_path}')