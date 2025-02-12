import tkinter as tk
import re
from GUIWidgets.JSONListbox import JSONListbox
from GUIWidgets.FilePathEntry import FilePathEntry
from GUIWidgets.AutoEntryButton import AutoEntryButton
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox
from ScriptBuilder.ScriptBuilder import ScriptBuilder
from GUIWidgets.GPIOPinner import GPIOPinner

class MainGui:
    def __init__(self, root):
        """The constructor for the MainGui class
        
        Args:
            root (tk.Tk): The root window for the program
        """
        # store the root window for later use. The root is the main window of 
        # the program. To create a GUI in Tkinter, you must create a root 
        # window. This is acccomplished by creating an instance of the Tk class
        # as such: root = tk.Tk().
        self.root = root
        
        # Create an instance of the GPIOPinner class
        self.pinner = GPIOPinner()

        # used to store the current project name and destination out path
        self.currentProjectName = ""
        self.destinationOutPath = ""

        
        # configure the root window
        # create the menu bar to hold the file menu and other relevant menus
        self.mainmenu = tk.Menu(self.root) 
        self.root.config(menu=self.mainmenu) # Set the menu to the root window
        self.fileMenu = tk.Menu(self.mainmenu) # Create a menu within the menu bar for file options

        
        # notice that the fileMenu is a menu within the mainmenu. This is done
        # to create a cascade menu. The fileMenu will be a drop down menu within
        # the mainmenu. This is done by adding the fileMenu to the mainmenu as a
        # cascade.
        self.mainmenu.add_cascade(label='File', menu=self.fileMenu)
        
        # add options to File cascade
        self.fileMenu.add_command(label='Export JSON', command=self.
                                  buildProject)
     

    
        # create a JLB to store user defined settings and data
        self.listBox= JSONListbox(self.root, title='Interactive Units', button_placement= 'bottom')
        self.listBox.pack()

        # add a command to execute when user clicks on the exit button on the 
        # window
        # 
        # this can be used to clean up any resources or accomplish any other 
        # tasks that may be necessary before the program exits
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


    def on_closing(self):
        """A function to execute when the user clicks on the exit button on the window
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()


    def buildProject(self):
        """A function to build the project and export it to the specified directory"""
        # the user must enter at least one interactive unit before exporting
        if self.listBox.returnJSON() == []:
            messagebox.showerror("Error", "You must enter at least one interactive unit")
            return


        # open a windows that forces the user to enter a project name and the 
        # absolute outpath for the project
        self.projectName = tk.simpledialog.askstring("Project Name", "Enter the name of the project.", initialvalue=self.currentProjectName)


        # check if the user entered a project name and project name contains 
        # only valid characters
        if self.projectName == None or not self.isValidWindowsFilename(self.projectName):
            messagebox.showerror("Error", "You must enter a valid Windows project name.")
            return

        self.outPath = filedialog.askdirectory(title="Select the output directory for the project.")



        if self.outPath == "":
            messagebox.showerror("Error", "You must enter an output directory.")
            return
        #return
        
        # ScriptBuilder is a class that builds the script (and relevant 
        # directories/resource files/installation files needed) for the project
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

    def isValidWindowsFilename(self, filename:str)-> bool:
        """A function to check if a filename is valid for Windows
        
        Args:
            filename (str): The filename to check
        Returns:0
            bool: True if the filename is valid, False otherwise
        
        """
    
        if re.match(r'[\\/:*?"<>|]', filename) == None:
            return True
        return False
    
 