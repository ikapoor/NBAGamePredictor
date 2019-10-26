import pandas as pd

from src.constants import (
	teams,
	seasons,
	stats

)


def get_season(start_year):
	if not start_year in seasons.keys():
		print("data not available")
		return None
	return pd.read_csv('data/{}'.format(seasons[start_year]))


def get_team_season(team, start_year):
	if team not in teams:
		print("Invalid Team name")
		return None
	if start_year not in seasons.keys():
		print("data not available")
		return None
	return pd.read_csv('data/{}_{}.csv'.format(team, start_year))

