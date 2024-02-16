# -----=====|  |=====-----
# Create by Jules - 16/02/2024
# -----=====|  |=====-----

class Room:
    """
        Représente une pièce avec son nom et son emplacement.
    """
    def __init__(self, name, locate):
        """
            Initialise un objet Room avec le nom et l'emplacement spécifiés.

            Args:
                name (str): Nom de la pièce.
                locate (str): Emplacement de la pièce.

            Attributes:
                name (str): Nom de la pièce.
                locate (str): Emplacement de la pièce.
        """
        self.name = name
        self.locate = locate
