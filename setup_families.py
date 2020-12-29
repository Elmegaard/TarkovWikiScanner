import os
import pywikibot  # no need to import in user_config.py
from pywikibot import config2  # no need to import in user_config.py

family = 'eft'
mylang = 'en'
familyfile = os.path.dirname(os.path.abspath(__file__))+"/families/"+family+"_family.py"

if not os.path.isfile(familyfile):
    print("family file %s is missing" % (familyfile))

config2.register_family_file(family, familyfile)
mysite = pywikibot.Site(mylang, family)
