import os
from utils.errors.error import ErrorCodes
from utils.errors.error import exitHandler


class FileManager():

    def __init__(self, log) -> None:
        self.log = log
        pass

    def createFolder(self, path: str):
        """Creates a folder of the given path, creates all intermediate
        folders if they do not exist.

        Args:
            path (_type_): Full path of the folder.
        """
        if not path:
            exitHandler(ErrorCodes.emptyPath, self.log)

        if not os.path.exists(path):
            os.makedirs(path)

        if not os.path.exists(path):
            exitHandler(ErrorCodes.fileNotFound, self.log)

        return

    def renameFile(self, currPath: str, newPath: str):
        """Renames a file.

        Args:
            currPath (str): Full path of the current file.
            newPath (str): Full path of the new file.
        """

        if not currPath or not newPath:
            exitHandler(ErrorCodes.emptyPath, self.log)

        os.rename(currPath, newPath)

        if not os.path.exists(newPath):
            exitHandler(ErrorCodes.fileNotFound, self.log)

        return
