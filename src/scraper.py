import requests
from bs4 import BeautifulSoup

months = ['october', 'november', 'december', 'january', 'february', 'march', 'april']
fields = ['visitor_team_name', 'visitor_pts','home_team_name', 'home_pts', 'box_score_link' ]


def scrape_season(season="2019"):
    file = open('data/{}_games.csv'.format(season), 'w')
    for field in fields:
        file.write(field)
        file.write(',')
    file.write('\n')
    for month in months:
        link = 'https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html'.format(season,month)
        print(link)
        r = requests.get(link)
        soup = BeautifulSoup(r.content, features='html.parser')
        rows = soup.find('tbody').find_all('tr')
        print(len(rows))
        for row in rows:
            if row.has_attr("class") and row.get("class") == "thead":
                continue
            file.write(row.find('td', {'data-stat': 'visitor_team_name'}).get_text())
            file.write(',')
            file.write(row.find('td', {'data-stat': 'visitor_pts'}).get_text())
            file.write(',')
            file.write(row.find('td', {'data-stat': 'home_team_name'}).get_text())
            file.write(',')
            file.write(row.find('td', {'data-stat': 'home_pts'}).get_text())
            file.write(',')
            file.write(row.find('a').get('href'))
            file.write('\n')
    file.close()






if __name__ == '__main__':
    scrape_season()

