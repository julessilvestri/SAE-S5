# -----=====|  |=====-----
# Create by Jules - 15/02/2024
# -----=====|  |=====-----

class Measure:
    """
        Représente une mesure avec sa valeur, son type de mesure et sa recommandation associée.
    """
    def __init__(self, value, measurement, recommendation):
        """
            Initialise un objet Measure avec les valeurs spécifiées.

            Args:
                value (float): Valeur de la mesure.
                measurement (str): Type de mesure.
                recommendation (str): Recommandation associée à la mesure.

            Attributes:
                value (float): Valeur de la mesure.
                measurement (str): Type de mesure.
                recommendation (str): Recommandation associée à la mesure.
        """

        self.value = value
        self.measurement = measurement
        self.recommendation = recommendation
