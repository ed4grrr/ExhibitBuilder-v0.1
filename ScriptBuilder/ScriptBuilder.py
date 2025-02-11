import ScriptBuilder.DirectoryBuilder.DirectoryBuilder as DirectoryBuilder
import ScriptBuilder.FileBuilder.FileBuilder as FileBuilder

class ScriptBuilder:
    """This class is used to build an Exhibit Control Script. It will write the script to a file and copy the necessary resources to the output directory. This class is to be used AFTER the user has input all necessary information for the script."""
    def __init__(self,outputPath: str, projectName: str):
        
        # create a directory builder object
        self.directoryBuilder = DirectoryBuilder.DirectoryBuilder()
        
        # create an output directory for the completed project
        self.directoryBuilder.createDirectory(outputPath)

        # create a file builder object, given the output path plus project name
        self.fileBuilder = FileBuilder.FileBuilder(outputPath + "/" + 
        projectName + ".py")




        # TODO - how to account for username for pi? force user to specfiy username? force them to stay pi?

        # TODO - look into multiple language support for the .desktop file?
        
        self.desktopFileText = """
        [Desktop Entry]
        Type=Application
        Name={projectName}
        Exec={pythonExecutableAddress} {ScriptAddress}}
        Name[en_US]={projectEnglishName}
                                """


        
    def writeSLBCScript(self, imports: list[str], listOfJSONS: list[dict]):
        self.fileBuilder.writeSLBCScript(imports, listOfJSONS)

    def copyResourcesDirectories(self, resourcesDirectories: list[str]):
        for directory in resourcesDirectories:
            self.directoryBuilder.copyDirectory(directory)




    def buildOutput(self, path,imports: list[str], listOfJSONS: list[dict], resourcesList: list[str], projectName: str):


        # write the script to the file
        self.writeSLBCScript(imports, listOfJSONS)

        # copy the resources directories to the output directory
        self.copyResourcesDirectories(resourcesList)

        # edit the .desktop file text to accomodate the new project
        textForDesktopFile = self.desktopFileText.format(projectName = projectName, pythonExecutableAddress = "/usr/bin/python3", ScriptAddress = path + "/" + projectName + ".py", projectEnglishName = projectName)
        
        # create the .desktop file with its text in the output directory
        self.directoryBuilder.createfile(path + "/" + projectName + ".desktop", textForDesktopFile)

        # create the resources directory in the output directory
        self.directoryBuilder.createDirectory(path + "/resources")

        # create the sounds directory in the resources directory
        self.directoryBuilder.createDirectory(path + "/resources/sounds")


        # copy the sound resources to the sounds directory
        for resource in resourcesList:
            self.directoryBuilder.copyFile(resource, path + "/resources/sounds")

        # create and store BASH script that places the .desktop file in the auto start directory
        self.directoryBuilder.copyFile("ScriptBuilder\FileBuilder\Installation.sh")

        
        # GuiController must be in the top level of the output directory 