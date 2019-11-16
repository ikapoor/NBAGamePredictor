import pandas as pd

from src.constants import (
	teams,
	seasons,
	stats,
	game_fields

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
	return pd.read_csv('../data/{}_{}.csv'.format(team, start_year))

def add_average_and_differential_stats(team, year):
	df = get_team_season(team, year)
	keep = stats + ['Opp.{}'.format(stat) for stat in stats]
	keep = keep + game_fields
	drop = [stat for stat in list(df.columns) if stat not in keep]
	df.drop(drop, axis=1, inplace=True)
	for stat in stats:
		df['differential_{}'.format(stat)] = df.apply(lambda row: row[stat] - row['Opp.{}'.format(stat)], axis=1)
		df['cumalitive_differential_{}'.format(stat)] = df['differential_{}'.format(stat)].cumsum().shift(1)
		df['cumalitive_{}'.format(stat)] = df[stat].cumsum().shift()
		df['cumalitive_Opp.{}'.format(stat)] = df['Opp.{}'.format(stat)].cumsum().shift()
		df['average_{}'.format(stat)] = df.apply(lambda row: (row['cumalitive_{}'.format(stat)]/(row['Game']-1)) if row['Game'] !=1 else 0, axis=1)
		df['average_Opp.{}'.format(stat)] = df.apply(lambda row: (row['cumalitive_Opp.{}'.format(stat)]/(row['Game']-1))if row['Game'] !=1 else 0, axis=1)
		df['average_differential_{}'.format(stat)] = df.apply(lambda row: (row['cumalitive_differential_{}'.format(stat)]/(row['Game']-1)) if row['Game'] !=1 else 0, axis=1)
	drop = ['cumalitive_differential_{}'.format(stat) for stat in stats] + ['cumalitive_{}'.format(stat)for stat in stats] + ['cumalitive_Opp.{}'.format(stat) for stat in stats]
	df.drop(drop, axis=1, inplace=True)
	return df




