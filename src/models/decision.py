"""
Strategic decision data structure
"""

from dataclasses import dataclass
from .enums import TyreCompound


@dataclass
class Decision:
    """Strategic decision made by the strategy program"""
    pit_now: bool                      # Should pit stop now?
    target_compound: TyreCompound      # Which tyres to fit after pit
    aggressive_pace: bool              # Push hard or conserve tyres?

    def __str__(self):
        return (f"Pit: {'YES' if self.pit_now else 'NO'}, "
                f"Tyres: {self.target_compound.compound_name} {self.target_compound.color}, "
                f"Pace: {'Aggressive' if self.aggressive_pace else 'Conservative'}")
