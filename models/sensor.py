# -----=====|  |=====-----
# Create by Jules - 16/02/2024
# -----=====|  |=====-----

class Sensor:
    """
        Représente un capteur avec son nom, ses mesures et la pièce où il est situé.
    """
    def __init__(self, name, measurements, room):
        """
            Initialise un objet Sensor avec le nom, les mesures et la pièce spécifiés.

            Args:
                name (str): Nom du capteur.
                measurements (str): Mesures du capteur.
                room (str): Nom de la pièce où se trouve le capteur.

            Attributes:
                name (str): Nom du capteur.
                measurements (str): Mesures du capteur.
                room (str): Nom de la pièce où se trouve le capteur.
        """
        self.name = name
        self.measurements = measurements
        self.room = room
