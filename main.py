import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import csv

# Recommandation de l'ADEME
def getStatusComfort(value, measurement) :
    if measurement == "°C" and value < 18 : # température
        return 'inconfortable'
    elif measurement == "%" and value < 40 or record.get_value() > 60 : # humidité
        return 'inconfortable'
    elif measurement == "ppm" and value > 1000 : # CO2
        return 'inconfortable'
    elif measurement == "UV index" and value > 2 : # UV
        return 'inconfortable'
    elif measurement == "dBA" and value > 100 : # dBA
        return 'inconfortable'
    elif measurement == "µg/m³" and value > 10 : # µg/m³
        return 'inconfortable'
    else :  
        return ''

bucket = "IUT_BUCKET"
org = "INFO"
token = "q4jqYhdgRHuhGwldILZ2Ek1WzGPhyctQ3UgvOII-bcjEkxqqrIIacgePte33CEjekqsymMqWlXnO0ndRhLx19g=="

url = "http://51.83.36.122:8086/"

try:
    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

    query_api = client.query_api()

    sensors = [
        "d251_1",
        "d351_1",
        "d351_2",
        "d351_3",
        "d360_1"
    ]

    for index, sensor in enumerate(sensors):
        print(str(index) + " => " + str(sensor))

    print ('')
    entity = int(input("Capteur : "))
    print ('')

    measurementQuery = 'from(bucket: "' + bucket +'")\
        |> range(start:-2d)\
        |> filter(fn: (r) => r["_field"] == "value")\
        |> filter(fn: (r) => r["entity_id"] =~ /^' + sensors[entity] + '/)\
        |> group(columns: ["_measurement"], mode:"by")\
        |> distinct(column: "_measurement")'
    
    try:
        measurementResult = query_api.query(org=org, query=measurementQuery)

        measurementResults = []
        for table in measurementResult:
            for record in table.records:
                measurementResults.append(
                    record.values.get("_measurement")
                )

        for index, measurement in enumerate(measurementResults):
            print(str(index) + " => " + str(measurement))
    except:
        print("Erreur requête flux")
        

    print ('')
    measurement = int(input("Mesure : "))
    print ('')

    query = 'from(bucket: "' + bucket +'")\
    |> range(start:-2d)\
    |> filter(fn: (r) => r["entity_id"] =~ /^' + sensors[entity] + '/)\
    |> filter(fn: (r) => r["_field"] == "value")\
    |> filter(fn: (r) => r["_measurement"] == "' + measurementResults[measurement] +'")'

    try:
        result = query_api.query(org=org, query=query)

        results = []
        for table in result:
            for record in table.records:                
                results.append((
                    record.get_field(), 
                    record.get_value(), 
                    record.get_measurement(),
                    record.get_time(),
                    getStatusComfort(record.get_value(), record.get_measurement())
                ))

        csv_file_path = 'exported_data.csv'

        with open(csv_file_path, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['_field', '_value', '_measurement', '_time', '_state'])
            csv_writer.writerows(results)

        print(f'Data exported to {csv_file_path}')
    except:
        print("Erreur requête flux")
except:
    print("Erreur connexion à InfluxDB")


