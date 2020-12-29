from pywikibot import family
from pywikibot.tools import deprecated


class Family(family.Family):

    name = 'eft'
    langs = {
        'en': 'escapefromtarkov.gamepedia.com',
    }

    def scriptpath(self, code):
        return ''

    @deprecated('APISite.version()')
    def version(self, code):
        return '1.31.2'

    def protocol(self, code):
        return 'HTTPS'
