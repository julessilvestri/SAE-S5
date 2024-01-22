# Import models
from models.room import Room

class RoomController:
    def __init__(self):
        self.rooms = [
            {'name': "d251", 'locate': "IUT"},
            {'name': "d351", 'locate': "IUT"},
            {'name': "d360", 'locate': "IUT"}
        ]

    def getAll(self):
        return [Room(room['name'], room['locate']) for room in self.rooms]

    def getByName(self, roomName):
        for room in self.rooms:
            if room['name'] == roomName:
                return Room(room['name'], room['locate'])
        return None
