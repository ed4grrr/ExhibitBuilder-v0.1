
from ScriptBuilder.FileBuilder.Functions import SLBComboCreatorFunctionString

class FileBuilder:
    """This class is used to write python scripts."""

    def __init__(self, path):
        """Creates a new ScriptWriter object
        path: str - the path to the file that the script will be written to"""
        self.path = path
        self.text = ""

    def write(self, text):
        """Writes the given text to the script without a newline character.
        text: str - the text to be written"""
        self.text += text

    def writeLine(self, text):
        """Writes the given text to the script with a newline character.
        text: str - the text to be written"""
        self.text += text + "\n"

    def writeNewLine(self):
        """Writes a newline character to the script"""
        self.text += "\n"

    def writeImport(self, module):
        """Writes an import statement to the script
        module: str - the module to be imported"""
        self.writeLine(f"import {module}")

    def writeMain(self):
        """Writes the main function to the script"""    
        self.writeLine("if __name__ == '__main__':")

    def writeTab(self, numTabs=1):
        """Writes a tab character to the script
        numTabs: int - the number of tabs to be written"""
        for i in range(numTabs):
            self.write("\t")

    def writeShebang(self):
        """Writes a shebang line to the script
        This is added as the script should be run on a Raspberry Pi"""
        self.writeLine("#!/usr/bin/env python3")

    def createImports(self, imports):
        """Creates import statements for the given modules
        imports: list[str] - a list of modules to be imported"""
        for i in imports:
            self.writeImport(i)

    
    def createFunctions(self, functionName:str, FunctionBody:str, numTabs:int=1):
        """Creates a function with the given name and body
        functionName: str - the name of the function
        FunctionBody: str - the body of the function
        """
        self.writeLine(f"def {functionName}():")
        for line in FunctionBody.split("\n"):
            self.writeTab(numTabs)
            self.writeLine(line)

    def writeSLBCScript(self, imports: list[str], listOfJSONS: list[dict]):
        """Writes the entire script to the file
        imports: list[str] - a list of modules to be imported"""
        self.writeShebang()
        self.createImports(imports)
        self.writeNewLine()
        self.writeLine(SLBComboCreatorFunctionString)

       

        # add any helper functions here
        self.writeMain()
        
        listOfNames, listofButtonGPIO, listofLEDGPIO, listofAudioFiles, volume, isDuringPress = self.createUserEnteredValues(listOfJSONS)
        self.writeLine("    listOfNames = " + str(listOfNames))
        self.writeLine("    listofButtonGPIO = " + str(listofButtonGPIO))
        self.writeLine("    listofLEDGPIO = " + str(listofLEDGPIO))
        self.writeLine("    listofAudioFiles = " + str(listofAudioFiles))
        self.writeLine("    volume = " + str(volume))
        self.writeLine("    isDuringPress = " + str(isDuringPress))
        self.writeNewLine()

        self.writeLine("    pygame.mixer.init()")
        self.writeLine("    listOfSLDBCombos = createSLDBCombos(listOfNames, listofButtonGPIO, listofLEDGPIO, listofAudioFiles, volume, isDuringPress)")
        self.writeLine("    signal.pause()")
        with open(self.path, "w") as file:
            file.write(self.text)

    def createUserEnteredValues(self, listOfJSONS: list[dict]):
        """Writes the user entered values to the script
        listOfJSONS: list[dict] - a list of JSON dictionaries
        
        
        imports, listOfNames, listofButtonGPIO, listofLEDGPIO, listofAudioFiles, volume, isDuringPress
        """
        
        listOfNames = []
        listofButtonGPIO = []
        listofLEDGPIO = []
        listofAudioFiles =[]
        listOfVolume = []
        isDuringPress = []
        for JSON in listOfJSONS:
            
            listOfNames.append(JSON["listOfNames"])
            listofButtonGPIO.append(JSON["listofButtonGPIO"])
            listofLEDGPIO.append(JSON["listofLEDGPIO"])
            listofAudioFiles.append(JSON["SoundFilePath"])
            listOfVolume.append(JSON["volume"])
            isDuringPress.append(JSON["isDuringPress"])

        return listOfNames, listofButtonGPIO, listofLEDGPIO, listofAudioFiles, listOfVolume, isDuringPress
 
        
