from enum import Enum
from dataclasses import dataclass

class RoadTypes(Enum):
    STRAIGHT = 1
    LEFT = 2
    RIGHT = 3
 
@dataclass
class ClothoidRoadState:
    x: int = 0  # cartesian x-coordinate in meters
    y: int = 0  # cartesian y-coordinate in meters
    t: int = 0  # road tangent at position in radians
