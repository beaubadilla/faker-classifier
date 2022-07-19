"""
"""
import csv
import time
import urllib.parse
from datetime import datetime

import requests
from bs4 import BeautifulSoup

# tournaments = ['2021 Season World Championship/Main Event', '2021 Season World Championship/Main Event']
T1_YEARS = ['2022', '2021', '2020']
SKT_YEARS = ['2019', '2018', '2017', '2016', '2015', '2014', '2013', 'Season 10', 'Season 3']
tournaments = [
       # 'Korea,LCK 2022 Spring',
       # 'International,Worlds 2021 Main Event',
       # 'Korea,LCK 2021 Regional Finals',
       # 'Korea,LCK 2021 Summer Playoffs',
       # 'Korea,LCK 2021 Summer',
       # 'Korea,LCK 2021 Spring Playoffs',
       # 'Korea,LCK 2021 Spring',
       # 'Korea,LCK 2020 Regional Finals',
       # 'Korea,LCK 2020 Summer Playoffs',
       # 'Korea,LCK 2020 Summer',
       # 'International,Mid-Season Cup 2020',
       # 'Korea,LCK 2020 Spring Playoffs',
       # 'Korea,LCK 2020 Spring',
       # 'Korea,KeSPA Cup 2019',
       # 'International,Worlds 2019 Main Event',
       # 'Korea,LCK 2019 Summer Playoffs',
       # 'Korea,LCK 2019 Summer',
       # 'International,Rift Rivals 2019 LCK-LPL-LMS-VCS',
       # 'International,MSI 2019 Main Event',
       # 'Korea,LCK 2019 Spring Playoffs',
       # 'Korea,LCK 2019 Spring',
       # 'Korea,KeSPA Cup 2018',
       # 'Korea,Korea Regional Finals 2018',
       # 'Korea,LCK 2018 Summer',
       # 'International,Rift Rivals 2018 LCK-LPL-LMS',
       # 'Asia,Asian Games 2018 Q - East',
       # 'Korea,LCK 2018 Spring Playoffs',
       # 'Korea,LCK 2018 Spring',
       # 'International,All-Star 2017 Los Angeles',
       # 'Korea,KeSPA Cup 2017',
       # 'International,Worlds 2017 Main Event',
       # 'Korea,LCK 2017 Summer Playoffs',
       # 'Korea,LCK 2017 Summer',
       # 'International,Rift Rivals 2017 LCK-LPL-LMS',
       # 'International,MSI 2017 Main Event',
       # 'Korea,LCK 2017 Spring Playoffs',
       # 'Korea,LCK 2017 Spring',
       # 'International,All-Star 2016 Barcelona',
       # 'Korea,KeSPA Cup 2016',
       # 'International,Worlds 2016',
       # 'Korea,LCK 2016 Summer Playoffs',
       # 'Korea,LCK 2016 Summer',
       # 'International,MSI 2016',
       # 'Korea,LCK 2016 Spring Playoffs',
       # 'Korea,LCK 2016 Spring',

       # 'International,IEM Season 10 World Championship',
       # 'International,All-Star 2015 Los Angeles',
       # 'Korea,KeSPA Cup 2015',
       # 'International,Worlds 2015',
       # 'Korea,Champions 2015 Summer Playoffs',
       # 'Korea,Champions 2015 Summer',
       # 'International,MSI 2015',
       # 'Korea,Champions 2015 Spring Playoffs',
       # 'Korea,Champions 2015 Spring',
       # 'Korea,Champions 2015 Spring Preseason',
       # 'Korea,Korea Regional Finals 2014', # !skt
       # 'Korea,NLB 2014 Summer', # !skt
       # 'Korea,Champions 2014 Summer', # !skt
       'Korea,LoL Masters 2014', # skt
       # 'International,All-Star 2014 Paris', # !skt
       # 'Korea,Champions 2014 Spring', # !skt
       # 'Korea,Champions 2014 Winter', # !skt
       # 'International,Worlds Season 3', # skt
       # 'Korea,Korea Regional Finals Season 3', # skt
       # 'Korea,Champions 2013 Summer', # skt
       # 'Korea,Champions 2013 Spring', # !skt
]
SKTT1K = ['Korea,Korea Regional Finals 2014', 'Korea,NLB 2014 Summer', 'Korea,Champions 2014 Summer', 'International,All-Star 2014 Paris', 'Korea,Champions 2014 Spring', 'Korea,Champions 2014 Winter', 'Korea,LoL Masters 2014']
SKTT1_2 = ['Korea,Champions 2013 Spring', 'Korea,Champions 2013 Summer']
TIME_BETWEEN_QUERIES = 20
num_tournys = len(tournaments)
time_to_complete = (num_tournys * TIME_BETWEEN_QUERIES) / 60
print(f"Data retrieval will finish in {time_to_complete} minutes.")
print(f"Now={datetime.now().strftime('%H:%M:%S')}\n")
for tournament in tournaments:
       records = []

       url, url2  = '', ''
       # url = "https://lol.fandom.com/wiki/Special:RunQuery/MatchHistoryGame?pfRunQueryFormName=MatchHistoryGame&MHG%5Bpreload%5D=Tournament&MHG%5Btournament%5D=2021+Season+World+Championship%2FMain+Event&MHG%5Bteam%5D=t1&MHG%5Bteam1%5D=&MHG%5Bteam2%5D=&MHG%5Bban%5D=&MHG%5Brecord%5D=&MHG%5Bascending%5D%5Bis_checkbox%5D=true&MHG%5Blimit%5D=&MHG%5Boffset%5D=&MHG%5Bregion%5D=&MHG%5Byear%5D=&MHG%5Bstartdate%5D=&MHG%5Benddate%5D=&MHG%5Bwhere%5D=&MHG%5Btextonly%5D%5Bis_checkbox%5D=true&MHG%5Btextonly%5D%5Bvalue%5D=1&wpRunQuery=Run+query&pf_free_text="
       for year in T1_YEARS:
              if year in tournament or tournament == 'Korea,KeSPA Cup 2019':
                     tournament_encoded = urllib.parse.quote_plus(tournament)
                     url = f"https://lol.fandom.com/wiki/Special:RunQuery/MatchHistoryGame?pfRunQueryFormName=MatchHistoryGame&MHG%5Bpreload%5D=Tournament&MHG%5Btournament%5D={tournament_encoded}&MHG%5Bteam%5D=t1&MHG%5Bteam1%5D=&MHG%5Bteam2%5D=&MHG%5Bban%5D=&MHG%5Brecord%5D=&MHG%5Bascending%5D%5Bis_checkbox%5D=true&MHG%5Blimit%5D=&MHG%5Boffset%5D=&MHG%5Bregion%5D=&MHG%5Byear%5D=&MHG%5Bstartdate%5D=&MHG%5Benddate%5D=&MHG%5Bwhere%5D=&MHG%5Btextonly%5D%5Bis_checkbox%5D=true&MHG%5Btextonly%5D%5Bvalue%5D=1&wpRunQuery=Run+query&pf_free_text="
                     break
                     # continue
       for year in SKT_YEARS:
              if year in tournament:
                     tournament_encoded = urllib.parse.quote_plus(tournament)
                     url = f"https://lol.fandom.com/wiki/Special:RunQuery/MatchHistoryGame?pfRunQueryFormName=MatchHistoryGame&MHG%5Bpreload%5D=Tournament&MHG%5Btournament%5D={tournament_encoded}&MHG%5Bteam%5D=skt&MHG%5Bteam1%5D=&MHG%5Bteam2%5D=&MHG%5Bban%5D=&MHG%5Brecord%5D=&MHG%5Bascending%5D%5Bis_checkbox%5D=true&MHG%5Blimit%5D=&MHG%5Boffset%5D=&MHG%5Bregion%5D=&MHG%5Byear%5D=&MHG%5Bstartdate%5D=&MHG%5Benddate%5D=&MHG%5Bwhere%5D=&MHG%5Btextonly%5D%5Bis_checkbox%5D=true&MHG%5Btextonly%5D%5Bvalue%5D=1&wpRunQuery=Run+query&pf_free_text="
                     if tournament in SKTT1K:
                            url = f"https://lol.fandom.com/wiki/Special:RunQuery/MatchHistoryGame?pfRunQueryFormName=MatchHistoryGame&MHG%5Bpreload%5D=Tournament&MHG%5Btournament%5D={tournament_encoded}&MHG%5Bteam%5D=sk+telecom+t1+k&MHG%5Bteam1%5D=&MHG%5Bteam2%5D=&MHG%5Bban%5D=&MHG%5Brecord%5D=&MHG%5Bascending%5D%5Bis_checkbox%5D=true&MHG%5Blimit%5D=&MHG%5Boffset%5D=&MHG%5Bregion%5D=&MHG%5Byear%5D=&MHG%5Bstartdate%5D=&MHG%5Benddate%5D=&MHG%5Bwhere%5D=&MHG%5Btextonly%5D%5Bis_checkbox%5D=true&MHG%5Btextonly%5D%5Bvalue%5D=1&wpRunQuery=Run+query&pf_free_text="
                     elif tournament in SKTT1_2:
                            url = f"https://lol.fandom.com/wiki/Special:RunQuery/MatchHistoryGame?pfRunQueryFormName=MatchHistoryGame&MHG%5Bpreload%5D=Tournament&MHG%5Btournament%5D={tournament_encoded}&MHG%5Bteam%5D=sk+telecom+t1+2&MHG%5Bteam1%5D=&MHG%5Bteam2%5D=&MHG%5Bban%5D=&MHG%5Brecord%5D=&MHG%5Bascending%5D%5Bis_checkbox%5D=true&MHG%5Blimit%5D=&MHG%5Boffset%5D=&MHG%5Bregion%5D=&MHG%5Byear%5D=&MHG%5Bstartdate%5D=&MHG%5Benddate%5D=&MHG%5Bwhere%5D=&MHG%5Btextonly%5D%5Bis_checkbox%5D=true&MHG%5Btextonly%5D%5Bvalue%5D=1&wpRunQuery=Run+query&pf_free_text="
                     
                     break
       if 'All-Star' in tournament:  # url does not include team because of Team Fire and Team Ice
              tournament_encoded = urllib.parse.quote_plus(tournament)
              url = f"https://lol.fandom.com/wiki/Special:RunQuery/MatchHistoryGame?pfRunQueryFormName=MatchHistoryGame&MHG%5Bpreload%5D=Tournament&MHG%5Btournament%5D={tournament_encoded}&MHG%5Bteam%5D=&MHG%5Bteam1%5D=&MHG%5Bteam2%5D=&MHG%5Bban%5D=&MHG%5Brecord%5D=&MHG%5Bascending%5D%5Bis_checkbox%5D=true&MHG%5Blimit%5D=&MHG%5Boffset%5D=&MHG%5Bregion%5D=&MHG%5Byear%5D=&MHG%5Bstartdate%5D=&MHG%5Benddate%5D=&MHG%5Bwhere%5D=&MHG%5Btextonly%5D%5Bis_checkbox%5D=true&MHG%5Btextonly%5D%5Bvalue%5D=1&wpRunQuery=Run+query&pf_free_text="
       elif 'Asia,Asian Games 2018 Q - East' == tournament:  # url does not include team because of Team Fire and Team Ice
              tournament_encoded = urllib.parse.quote_plus(tournament)
              url = f"https://lol.fandom.com/wiki/Special:RunQuery/MatchHistoryGame?pfRunQueryFormName=MatchHistoryGame&MHG%5Bpreload%5D=Tournament&MHG%5Btournament%5D={tournament_encoded}&MHG%5Bteam%5D=south+korea&MHG%5Bteam1%5D=&MHG%5Bteam2%5D=&MHG%5Bban%5D=&MHG%5Brecord%5D=&MHG%5Bascending%5D%5Bis_checkbox%5D=true&MHG%5Blimit%5D=&MHG%5Boffset%5D=&MHG%5Bregion%5D=&MHG%5Byear%5D=&MHG%5Bstartdate%5D=&MHG%5Benddate%5D=&MHG%5Bwhere%5D=&MHG%5Btextonly%5D%5Bis_checkbox%5D=true&MHG%5Btextonly%5D%5Bvalue%5D=1&wpRunQuery=Run+query&pf_free_text="

       if len(url) == 0:
              print(f"Empty URL? {tournament_encoded}")
              continue
       try:
              print(f"Querying {url}")
              page = requests.get(url)
       except Exception as e:
              print(f"Request failed - {e}")
              continue

       soup = BeautifulSoup(page.content, "html.parser")

       rows = soup.find_all("tr", class_="multirow-highlighter")
       for row in rows:
              columns = row.find_all("td")
              date = columns[0].text.encode('ascii', 'ignore').decode()
              patch = columns[1].text.encode('ascii', 'ignore').decode()
              blue_side_team = columns[2].text.encode('ascii', 'ignore').decode()
              red_side_team = columns[3].text.encode('ascii', 'ignore').decode()
              winner = columns[4].text.encode('ascii', 'ignore').decode()
              blue_side_bans = columns[5].text.encode('ascii', 'ignore').decode()
              red_side_bans = columns[6].text.encode('ascii', 'ignore').decode()
              blue_side_picks = columns[7].text.encode('ascii', 'ignore').decode()
              red_side_picks = columns[8].text.encode('ascii', 'ignore').decode()
              blue_side_roster = columns[9].text.encode('ascii', 'ignore').decode()
              red_side_roster = columns[10].text.encode('ascii', 'ignore').decode()

              if 'Faker' in blue_side_roster or 'Faker' in red_side_roster:  # Because of All Stars >:(
                     records.append([date, patch, blue_side_team, red_side_team, winner, blue_side_bans, red_side_bans, blue_side_picks, red_side_picks, blue_side_roster, red_side_roster])

       features = ['date', 'patch', 'blue_side_team', 'red_side_team', 'winner', 'blue_side_bans', 'red_side_bans', 'blue_side_picks', 'red_side_picks', 'blue_side_roster', 'red_side_roster']
       filename = "db3-next.csv"
       with open(filename, 'a') as csv_file:
              csvwriter = csv.writer(csv_file)
              # csvwriter.writerow(features)
              print(f"Writing {records}")
              if not len(records): print(f"Could not find data for {tournament_encoded} - {url}")
              csvwriter.writerows(records)

       print(f"Now={datetime.now().strftime('%H:%M:%S')}. Sleeping for {TIME_BETWEEN_QUERIES} seconds\n")
       time.sleep(20)
