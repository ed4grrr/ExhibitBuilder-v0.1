import tkinter as tk
import re
from GUIWidgets.JSONListbox import JSONListbox
from GUIWidgets.FilePathEntry import FilePathEntry
from GUIWidgets.AutoEntryButton import AutoEntryButton
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox
from ScriptBuilder.ScriptBuilder import ScriptBuilder
from GPIOPinner import GPIOPinner


class MainGui:
    def __init__(self, root):

        self.pinner = GPIOPinner() # Create an instance of the GPIOPinner class
        
        self.root = root
        # configure the root window
        self.mainmenu = tk.Menu(self.root) # Create a menu
        self.root.config(menu=self.mainmenu) # Set the menu to the root window
        self.fileMenu = tk.Menu(self.mainmenu) # Create a menu
        self.currentProjectName = ""
        self.destinationOutPath = ""
        
        self.mainmenu.add_cascade(label='File', menu=self.fileMenu) # Add a cascade to the menu
        # add options to File cascade

        self.fileMenu.add_command(label='Export JSON', command=self.buildProject)
     

    
        # create a JLB to store user defined settings and data
        self.listBox= JSONListbox(self.root, title='Interactive Units', button_placement= 'bottom')
        self.listBox.pack()

        # add a command to execute when user clicks on the exit button on the window
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()


    def buildProject(self):
        # opens a window that forces the user to enter a project name and the absolute outpath for the project
      
        if self.listBox.returnJSON() == []:
            messagebox.showerror("Error", "You must enter at least one interactive unit")
            return
        
        self.projectName = tk.simpledialog.askstring("Project Name", "Enter the name of the project.", initialvalue=self.currentProjectName)


        # check if the user entered a project name and project name contains only valid characters


        if self.projectName == None or not self.isValidWindowsFilename(self.projectName):
            messagebox.showerror("Error", "You must enter a valid Windows project name.")
            return

        self.outPath = filedialog.askdirectory(title="Select the output directory for the project.")

        if self.outPath == "":
            messagebox.showerror("Error", "You must enter an output directory.")
            return
        #return
        
        
        self.scriptBuilder = ScriptBuilder(self.outPath, self.projectName)
        currentJSONS =self.listBox.returnJSON()


        # get file paths for all the sound files to copy them
        listOfResources = [ currentJSON["SoundFilePath"] for currentJSON in currentJSONS]


        # make the sound file paths relative to the resources directory for use in the script
        for currentJSON in currentJSONS:
            currentJSON["SoundFilePath"] = "./resources"+currentJSON["SoundFilePath"].split("/")[-1]

        # build the script, including necessary directories and other files
        self.scriptBuilder.buildOutput(self.outPath, ["import ComponentBuilder.SoundLEDButtonCombo as SoundLEDButtonCombo"
        ,"import signal"], currentJSONS, listOfResources, self.projectName)

    def isValidWindowsFilename(self, filename):
        """A function to check if a filename is valid for Windows"""
        if re.match(r'[\\/:*?"<>|]', filename) == None:
            return True
        return False




if __name__ == '__main__':





    root = tk.Tk() # Create a Tkinter root window




    def validate_float(P):
        """A function to validate a float value to assure it is between 0 and 1"""
        try:
            value = float(P)
            if value < 0:
                return False
            if value > 1:
                return False
            return True
        except ValueError:
            return False


    gui =MainGui(root) # Create an instance of the MainGui class

    JSONFields = {
        "Name": [tk.Entry, {}],
        "SoundFilePath": [FilePathEntry, {}],
        "During Push or After Push": [Combobox, {"values":["During Push", "After Push"], "state":"readonly"}],
        "Volume": [tk.Spinbox, {"values":tuple([floatValue/100 for floatValue in range(101)]), "validate":"all", "validatecommand":(root.register(validate_float), '%P')}],


        # The lambda functions below are used to call the assignPinAutomatically method with the argument "LED". This is done to prevent the method from being called when the dictionary is created. Otherwise, the method would be called when the dictionary is created and the value would be the same for all the entries.

        "LED GPIO Pin": [AutoEntryButton, {"valueToBeShown": lambda : gui.pinner.assignPinAutomatically("LED")}], 


        "Button GPIO Pin": [AutoEntryButton, {"valueToBeShown": lambda : gui.pinner.assignPinAutomatically("Button")}]
    }
    gui.listBox.fields = JSONFields

    



    root.mainloop() # Start the Tkinter main event loop
