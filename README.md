# TarkovWikiScanner

Will scan the wiki for all quest and hideout requirements and put them in a json file.
Written in Python 3.9

The pages used to fetch the data are these:

- https://escapefromtarkov.gamepedia.com/Quests
- https://escapefromtarkov.gamepedia.com/Hideout

If they are not up to date the data will be wrong. Please either update the wiki if you find such a case or contact the wiki team on their [Discord](https://discord.gg/7ZeEyfU)

# How to run

- pip install -r requirements.txt
- python scanner.py
- JSON output will be in a new folder called output
