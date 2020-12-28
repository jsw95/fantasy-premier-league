import os
from config import Config


def proportion_of_match_played(minutes):
    return minutes / Config.MINUTES_IN_A_FOOTBALL_MATCH


