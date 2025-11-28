from enum import StrEnum, unique


@unique
class FruitType(StrEnum):
    MAIZE = "MAIZE"
    SUGARBEET = "SUGARBEET"
    BEETROOT = "BEETROOT"
    PEA = "PEA"
    COTTON = "COTTON"
    PARSNIP = "PARSNIP"
    WHEAT = "WHEAT"
    UNKNOWN = "UNKNOWN"
    SUNFLOWER = "SUNFLOWER"
    SOYBEAN = "SOYBEAN"
    CARROT = "CARROT"
    SPINACH = "SPINACH"
    OAT = "OAT"
    GRASS = "GRASS"
    SORGHUM = "SORGHUM"
    POTATO = "POTATO"
    # TODO: Add all crop types


@unique
class GroundType(StrEnum):
    SOWN = "SOWN"
    HARVEST_READY = "HARVEST_READY"
    PLOWED = "PLOWED"
    GRASS = "GRASS"
    CULTIVATED = "CULTIVATED"


@unique
class SprayType(StrEnum):
    NONE = "NONE"
    MANURE = "MANURE"
    LIQUID_MANURE = "LIQUID_MANURE"
    LIQUID_FERTILIZER = "LIQUID_FERTILIZER"