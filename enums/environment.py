from enum import IntEnum, StrEnum


class WeatherType(StrEnum):
    SUN = "SUN"
    CLOUDY = "CLOUDY"
    RAIN = "RAIN"
    SNOW = "SNOW"
    HAIL = "HAIL"


class Season(StrEnum):
    WINTER = "WINTER"
    SUMMER = "SUMMER"
    SPRING = "SPRING"
    FALL = "FALL"


class Month(IntEnum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12