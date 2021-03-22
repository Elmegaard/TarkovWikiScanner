# Python 3.9

import requests
import mwparserfromhell
import pywikibot
import setup_families
import re
import json
import os
import errno


def Import():
    site = pywikibot.Site("eft:en")
    questPage = pywikibot.Page(site, u"Quests")
    questText = questPage.text

    hideoutPage = pywikibot.Page(site, u"Hideout")
    hideoutText = hideoutPage.text

    outputDir = os.path.dirname(os.path.abspath(__file__))+"/output"
    questsOutput = outputDir + "/quest.json"
    hideoutOutput = outputDir + "/hideout.json"

    questItemList = {}
    hideoutItemList = {}

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
                    name = matchSplit[0].lower()
                    if name in questItemList:
                        item = questItemList[name]
                    else:
                        item = {}
                        item["name"] = name
                        item["wiki"] = "https://escapefromtarkov.gamepedia.com/" + name
                        questItemList[name] = item
                    countKey = "fir_count" if findInRaid else "count"
                    item[countKey] = item.get(countKey) or 0 + GetAmount(line)

    # Create hideout object
    for line in hideoutText.splitlines():
        if (re.search(r"\*\s*\d+", line)):
            match = re.match(r".*\[\[(.*?)\]\].*", line)
            if (match):
                matchSplit = match.groups()[0] .split('|')
                if (len(matchSplit) > 0):
                    name = matchSplit[0].lower()
                    if name in hideoutItemList:
                        item = hideoutItemList[name]
                    else:
                        item = {}
                        hideoutItemList[name] = item
                        item["name"] = name
                        item["wiki"] = "https://escapefromtarkov.gamepedia.com/" + name
                    item["count"] = item.get("count") or 0 + GetAmount(line)

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


def GetAmount(line):
    if ("key " in line.lower()):
        return 1

    match = re.match(r".*?([\d|\.]+)[\w|\s]*?\[", line)

    if (not match):
        match = re.match(r".*?([\d|\.]+)[\s]*pcs", line)

    if (match):
        number = match.groups()[0]
        number = number.replace(".", "")

        if (number.isdigit()):
            return int(number)
        else:
            return 1
    else:
        return 1


Import()
