import shutil
import os


class DirectoryBuilder:
    """A class to create, remove, and copy directories"""

    def __init__(self):
        """Creates a new DirectoryBuilder object"""
        self.directory = None


    def createDirectory(self, path: str) -> None:
        """Creates a directory at the given path
            path: str - the path to the directory"""        
        self.directory = path

        try:
            os.makedirs(self.directory)
        except FileExistsError:
            print(f"Directory {self.directory} already exists")

    def getDirectory(self):
        """Returns the path to the directory"""
        return self.directory

    def removeDirectory(self):
        """Removes the directory"""
        try:
            shutil.rmtree(self.directory)
        except FileNotFoundError:
            print(f"Directory {self.directory} does not exist")
        self.directory = None

    def copyDirectory(self, path: str):
        """Copies the directory at the given path to the directory"""
        try:
            shutil.copytree(path, self.directory)
        except FileNotFoundError:
            print(f"Directory {path} does not exist")
        except FileExistsError:
            print(f"Directory {self.directory} already exists in {path}")
        except OSError as e:
            print(f"OS Error: {e}")

    def copyFile(self, path: str):
        """Copies the file at the given path to the directory"""
        try:
            shutil.copy(path, self.directory)
        except FileNotFoundError:
            print(f"File {path} does not exist")
        except FileExistsError:
            print(f"File {self.directory} already exists in {path}")
        except OSError as e:
            print(f"OS Error: {e}")
    
    def moveFile(self, path: str):
        """Moves the file at the given path to the directory"""
        try:
            shutil.move(path, self.directory)
        except FileNotFoundError:
            print(f"File {path} does not exist")
        except FileExistsError:
            print(f"File {self.directory} already exists in {path}")
        except OSError as e:
            print(f"OS Error: {e}")

    def createfile(self, fileName: str, text: str):
        """Creates a file within the stored directory path"""
        try:
            with open(self.directory + f"/{fileName}.desktop", 'w') as f:
                f.write(text)
        except FileExistsError:
            print(f"File {fileName} already exists")
