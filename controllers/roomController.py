# Import models
from models.room import Room

class RoomController:
    def __init__(self):
        self.rooms = [
            "d251_1",
            "d351_1",
            "d351_2",
            "d351_3",
            "d360_1"
        ]

    def getRoomList(self):
        return [Room(room_label) for room_label in self.rooms]

    def getRoomById(self, room_label):
        for room in self.rooms:
            if room:
                return Room(room)
            else:
                return None