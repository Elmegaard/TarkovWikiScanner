# Python 3.9

import requests
import mwparserfromhell
import pywikibot
import setup_families
import re
import json
import os
import errno

site = pywikibot.Site("eft:en")
questPage = pywikibot.Page(site, u"Quests")
questText = questPage.text

hideoutPage = pywikibot.Page(site, u"Hideout")
hideoutText = hideoutPage.text

outputDir = os.path.dirname(os.path.abspath(__file__))+"/output"
questsOutput = outputDir + "/quest.json"
hideoutOutput = outputDir + "/hideout.json"

questItemList = []
hideoutItemList = []

# Create quest object
for line in questText.splitlines():
    findInRaid = False
    if ("raid" in line):
        findInRaid = True

    if ("Find " in line):
        match = re.match(r".*\[\[(.*?)\]\].*", line)
        if (match):
            matchSplit = match.groups()[0] .split('|')
            if (len(matchSplit) > 0):
                # If the item already exists, make sure findInRaid is set if it should be for any of them
                itemExists = False
                for obj in questItemList:
                    if obj["name"] == matchSplit[0]:
                        itemExists = True
                        if (item["findInRaid"] or findInRaid):
                            item["findInRaid"] = findInRaid

                # Only add items once
                if (not itemExists):
                    item = {}
                    item["wikilink"] = "https://escapefromtarkov.gamepedia.com/" + matchSplit[0]
                    item["name"] = matchSplit[0]

                    item["findInRaid"] = findInRaid
                    questItemList.append(item)

# Create hideout object
for line in hideoutText.splitlines():
    if (re.search(r"\*\s*\d+", line)):
        match = re.match(r".*\[\[(.*?)\]\].*", line)
        if (match):
            matchSplit = match.groups()[0] .split('|')
            if (len(matchSplit) > 0):
                if not any(x["name"] == matchSplit[0] for x in hideoutItemList):
                    item = {}
                    item["wikilink"] = "https://escapefromtarkov.gamepedia.com/" + matchSplit[0]
                    item["name"] = matchSplit[0]

                    hideoutItemList.append(item)


# Create quest.json
if not os.path.exists(os.path.dirname(questsOutput)):
    try:
        os.makedirs(os.path.dirname(questsOutput))
    except OSError as exc:  # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

# Create hideout.json
if not os.path.exists(os.path.dirname(questsOutput)):
    try:
        os.makedirs(os.path.dirname(questsOutput))
    except OSError as exc:  # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

# Write quest.json
with open(questsOutput, "w", encoding="utf-8") as f:
    json.dump(questItemList, f, ensure_ascii=False, indent=4)

# Write hideout.json
with open(hideoutOutput, "w", encoding="utf-8") as f:
    json.dump(hideoutItemList, f, ensure_ascii=False, indent=4)
