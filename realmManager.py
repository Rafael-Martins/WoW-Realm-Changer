from fileManager import FileManager
from configManager import GAME_PATH

DEFAULT_REALMS = [{
    'name': 'Warmane',
    'address': 'logon.warmane.com'
}]

REALM_PATH = GAME_PATH + '\\Data\\enUS\\realmlist.wtf'

REALM_TEXT = 'Current realm is: '
REALM_PREFIX = 'set realmlist '


class RealmManager(FileManager):
    def __init__(self):
        super().__init__(path=REALM_PATH, defaultContent='', isJson=False)
        self.realmFile = REALM_PATH

    def writeRealmFile(self, realmAddress):
        self.write('set realmlist ' + realmAddress)

    def currentRealm(self):
        fullRealm = self.load()

        if fullRealm is '' or len(fullRealm) <= 0:
            return REALM_TEXT + 'null'

        realmArray = fullRealm[0].split('set realmlist ')

        if len(realmArray) <= 1:
            return REALM_TEXT + 'null'

        realmAddress = realmArray[1]

        return REALM_TEXT + realmAddress

    def changeActiveRealm(self, realm):
        self.write(REALM_PREFIX + realm['address'])
