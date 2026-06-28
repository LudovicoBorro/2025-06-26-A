from dataclasses import dataclass

@dataclass
class Circuito:
    circuitId: int
    circuitRef: str
    name: str
    location: str
    country: str
    lat: float
    lng: float
    alt: int
    url: str
    piazzamenti = {}

    def __hash__(self):
        return hash(self.circuitId)

    def __eq__(self, other):
        return self.circuitId == other.circuitId

    def __str__(self):
        return f"{self.name}"