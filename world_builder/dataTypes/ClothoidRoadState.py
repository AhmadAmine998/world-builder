from dataclasses import dataclass

@dataclass
class ClothoidRoadState:
    x: int = 0  # cartesian x-coordinate in meters
    y: int = 0  # cartesian y-coordinate in meters
    t: int = 0  # road tangent at position in radians
