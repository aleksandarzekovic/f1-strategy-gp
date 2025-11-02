"""
Race state data structure
"""

from dataclasses import dataclass
from .enums import TyreCompound


@dataclass
class RaceState:
    """Current state of the race"""
    current_lap: int              # Current lap (0-N)
    tyre_age: int                 # Tyre age in laps
    tyre_compound: TyreCompound   # Current tyre type
    position: int                 # Position in race (1-20)
    gap_to_leader: float          # Gap to leader in seconds
    gap_to_rival: float           # Gap to nearest rival (+ ahead, - behind)
    safety_car: bool              # Is safety car deployed
    rain_probability: float       # Rain probability (0-1)
    pit_stops_made: int           # Number of pit stops completed
    track_wetness: float = 0.0    # Track wetness level (0=dry, 1=soaking)

    def is_dry_tyres(self) -> bool:
        """Check if currently on dry tyres"""
        return self.tyre_compound in [TyreCompound.SOFT, TyreCompound.MEDIUM, TyreCompound.HARD]

    def is_wet_tyres(self) -> bool:
        """Check if currently on wet tyres"""
        return self.tyre_compound in [TyreCompound.INTERMEDIATE, TyreCompound.WET]
