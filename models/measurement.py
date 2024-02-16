# -----=====|  |=====-----
# Create by Jules - 12/2023
# -----=====|  |=====-----

class Measurement:
    """
        Représente une mesure avec son nom.
    """
    def __init__(self, name):
        """
            Initialise un objet Measurement avec le nom spécifié.

            Args:
                name (str): Nom de la mesure.

            Attributes:
                name (str): Nom de la mesure.
        """
        
        self.name = name
