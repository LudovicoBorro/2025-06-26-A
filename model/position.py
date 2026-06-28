from dataclasses import dataclass

@dataclass
class Position:
    driverId: int
    position: int

    def __hash__(self):
        return hash(self.driverId)

    def __eq__(self, other):
        return self.driverId == other.driverId

    def __str__(self):
        return f"{self.driverId} - {self.position}"