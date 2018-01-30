import os.path
import json


class FileManager:
    def __init__(self, path, defaultContent, isJson):
        self.path = path
        self.defaultContent = defaultContent
        self.isJson = isJson

    def write(self, content):
        """Write to file

        Args:
            content (String|Object): Description
        """
        with open(self.path, 'w') as file:
            if file == '':
                raise Exception('')
            if self.isJson:
                json.dump(content, file)
            else:
                file.write(content)

    def _read(self):
        """Read file content, return object or array of lines
        depending on wether self.isJson is true

        Returns:
            (Object | Array)
        """
        with open(self.path) as file:
            if file == '':
                self.write({})

            if self.isJson:
                return json.load(file)
            else:
                return file.readlines()

    def load(self):
        """Load file creating with default content if it doesn't exist

        Returns:
            (Object | Array)
        """
        if not os.path.isfile(self.path) and self.defaultContent is not None:
            self.write(self.defaultContent)

        return self._read()
