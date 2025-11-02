"""
Enumerations for race elements
"""

from enum import Enum


class TyreCompound(Enum):
    """F1 tyre types with official color coding"""
    # Dry tyres
    SOFT = ("Soft", "Red")         # Fastest, highest wear
    MEDIUM = ("Medium", "Yellow")  # Balanced performance
    HARD = ("Hard", "White")       # Slowest, lowest wear

    # Wet tyres
    INTERMEDIATE = ("Intermediate", "Green")  # Light rain
    WET = ("Wet", "Blue")                     # Heavy rain

    def __init__(self, compound_name, color):
        self.compound_name = compound_name
        self.color = color

    def __str__(self):
        return f"{self.compound_name} ({self.color})"


class RaceEvent(Enum):
    """Events that can occur during race"""
    SAFETY_CAR = "Safety Car"
    VIRTUAL_SAFETY_CAR = "Virtual Safety Car"
    RIVAL_PITS = "Rival pitting"
    LIGHT_RAIN = "Light rain"
    HEAVY_RAIN = "Heavy rain"
    CLEAR = "Normal race"
