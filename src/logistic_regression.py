from sklearn.datasets import make_classification
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
import seaborn as sns
sns.set()
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import pandas as pd
from src.utils import get_team_season

from src.constants import (
    game_fields,
    stats,
    teams
)
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

df = get_team_season('TOR', '2014')
opp_stats = ['Opp.{}'.format(stat) for stat in stats]
diff = ['differential_{}'.format(stat) for stat in stats]
features = [col for col in df.columns if (col not in opp_stats and col not in stats and col not in game_fields and col not in diff)]

TEAM = 'TOR'
season_2014 = {}
season_2017 = {}
x_train = pd.DataFrame()
x = pd.DataFrame()
for team in teams:
    df = get_team_season(team, '2014')
    df['Win'] = df.apply(lambda row: int(1) if row['WINorLOSS'] == 'W' else int(0), axis=1)
    x_train = x_train.append(df)
    season_2014[team] = df

for team in teams:
    df = get_team_season(team, '2017')
    df['Win'] = df.apply(lambda row: int(1) if row['WINorLOSS'] == 'W' else int(0), axis=1)
    x = x.append(df)
    season_2017[team] = df


for feature in features:
    x_train['Opp_{}'.format(feature)] = x_train.apply(lambda game: x_train[(x_train.Date == game.Date) & (x_train.Team == game.Opponent)].iloc[0][feature], axis=1)



y_train = x_train['Win'].as_matrix()
x_train = x_train[features].copy().as_matrix()




# df = get_team_season(TEAM, '2017')





# # x, y = make_classification(
# #     n_samples=100,
# #     n_features=2,
# #     n_classes=2,
# #     n_clusters_per_class=1,
# #     flip_y=0.03,
# #     n_informative=1,
# #     n_redundant=0,
# #     n_repeated=0
# # )

# lr = LogisticRegression()
#
#
#
#
#
# #
# lr.fit(x_train, y_train)
#
# print(lr.coef_)
# print(lr.intercept_)

# #
#
# # y_pred = lr.predict(x_test)
# # print(y_pred)
# # print(confusion_matrix(y_test, y_pred))
correct_predictions = 0
incorrect_predictions = 0
for team in teams:
    if team == TEAM:
        continue
    print(team)
    df_2 = get_team_season(team, '2017')
    new_x = df_2[features].copy().as_matrix()
    df_2['Win'] = df_2.apply(lambda row: int(1) if row['WINorLOSS'] == 'W' else int(0), axis=1)

    new_y = df_2['Win'].as_matrix()

    y_hat = lr.predict(new_x)
    k = confusion_matrix(new_y, y_hat)
    correct_predictions += k[0][0]
    correct_predictions += k[1][1]
    incorrect_predictions += k[0][1]
    incorrect_predictions += k[1][0]



print("Correct Predictions : {}".format(correct_predictions))
print ("Incorrect Predictions : {}".format(incorrect_predictions))

# df = pd.DataFrame({'x': x_test[:,0], 'y': y_test})
# df = df.sort_values(by='x')
# from scipy.special import expit
# sigmoid_function = expit(df['x'] * lr.coef_[0][0] + lr.intercept_[0]).ravel()
# plt.plot(df['x'], sigmoid_function)
# plt.scatter(df['x'], df['y'], c=df['y'], cmap='rainbow', edgecolors='b')
# plt.show()
