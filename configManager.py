from fileManager import FileManager

DEFAULT_STORAGE = {
    'savedRealms': [
        {
            'name': 'Warmane',
            'address': 'logon.warmane.com'
        }
    ],
    'gamePath': None
}

GAME_PATH = 'Z:\WOW'
STORAGE_PATH = 'data.json'


class ConfigManager(FileManager):
    def __init__(self):
        super().__init__(
            path=STORAGE_PATH,
            defaultContent=DEFAULT_STORAGE,
            isJson=True
        )
        self.config = self.load()

    def updateGameFolder(self, gameFolderPath):
        config = self.load()
        config['gamePath'] = gameFolderPath
        self.write(config)

    def hasGameFolder(self):
        config = self.load()

        if 'gamePath' not in self.config:
            config['gamePath'] = None
            self.write(config)

        if config['gamePath'] == '':
            return False

        return True

    def removeRealm(self, index):
        config = self.load()
        config['savedRealms'].pop(index)
        self.write(config)

    def addRealm(self, realm):
        config = self.load()
        config['savedRealms'].append(realm)
        self.write(config)

    def savedRealmsCount(self):
        config = self.load()
        return len(config['savedRealms'])

    def savedRealms(self):
        config = self.load()
        return config['savedRealms']
