# pip install git+git://github.com/buluba89/football-data-api
from football_data_api import Team

t = Team(1)
print(t.name)

for player in t.players:
  print(player.name)

