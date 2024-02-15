# "°C" -> returnMeasurement!! in 18.0..22.0
# "lx" -> returnMeasurement!! in 300.0..500.0
# "ppm" -> returnMeasurement?.let { it <= 1000 }
# "%" -> returnMeasurement!! in 40.0..60.0
# "µg/m³" -> returnMeasurement?.let { it <= 10 }
# "UV index" -> true

from controllers.measureController import MeasureController

measureController = MeasureController()

measureState = measureController.getState("d251")

for measureStateValue in measureState :
    print(measureStateValue.value)