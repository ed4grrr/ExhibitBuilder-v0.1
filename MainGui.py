import tkinter as tk
import re
from GUIWidgets.JSONListbox import JSONListbox
from GUIWidgets.FilePathEntry import FilePathEntry
from GUIWidgets.AutoEntryButton import AutoEntryButton
from GUIWidgets.MultipleAutoEntryButtons import MultipleAutoEntryButtons
from tkinter import messagebox, filedialog, Entry
from tkinter.ttk import Combobox
from ScriptBuilder.ScriptBuilder import ScriptBuilder
from GUIWidgets.GPIOPinner import GPIOPinner

class MainGui:

    def validate_float(self,stringToValidate) -> bool:
        """A function to validate a float value to assure it is between 0 and 1
        
        Args:
            stringToValidate (str): The string to validate
        Returns:
            bool: True if the string is a valid float value between 0 and 1, False otherwise
        """
        try:
            value = float(stringToValidate)
            if value < 0:
                return False
            if value > 1:
                return False
            return True
        except ValueError:
            return False            
        
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
     
        # Create a dictionary to store the fields for the JSONListbox widget.
        # The keys are the strings containing the names of the fields (and will be 
        # used to create a label for the corresponding entry widget). 
        # 
        # The values are lists with the first element being the widget to be used 
        # and the second element being a dictionary of keyword arguments to be 
        # passed to the widget's constructor.
        #
        # The widgets can be any built-in Tkinter widget OR a custom widget as seen 
        # with SoundFilePath and AutoEntryButton. Make sure the custom widgets
        # inherit from Tkinter's Widget class.
        JSONFields = {
            "Name": [tk.Entry, {}],
            "SoundFilePath": [FilePathEntry, {}],
            "During Push or After Push": [Combobox, {"values":["During Push", "After Push"], "state":"readonly"}],
            "Volume": [tk.Spinbox, {"values":tuple([floatValue/100 for floatValue in range(101)]), "validate":"all", "validatecommand":(self.root.register(self.validate_float), '%P')}],


            # The lambda functions below are used to call the 
            # assignPinAutomatically method with the argument "LED". This is done 
            # to prevent the method from being called when the dictionary is 
            # created. Otherwise, the method would be called when the dictionary is 
            # created and the value would be the same for all the entries.
            # In this case, only the values 2 and 3 would ever be shown within their
            # respective entry widgets.

            

            "LED Pin Numbers": [MultipleAutoEntryButtons, {"valuesToBeShown": lambda : self.pinner.rentFirstAvailablePin(), "numberOfEntries":2, "labels":["LED Physical Pin Number", "LED BCM Pin Number"]}], 

            "Button Pin Numbers": [MultipleAutoEntryButtons, {"valuesToBeShown": lambda : self.pinner.rentFirstAvailablePin(), "numberOfEntries":2, "labels":["Button Physical Pin Number", "Button BCM Pin Number"]}],


            
        }

        editJSONFields = {
            "Name": [tk.Entry, {}],
            "SoundFilePath": [FilePathEntry, {}],
            "During Push or After Push": [Combobox, {"values":["During Push", "After Push"], "state":"readonly"}],
            "Volume": [tk.Spinbox, {"values":tuple([floatValue/100 for floatValue in range(101)]), "validate":"all", "validatecommand":(self.root.register(self.validate_float), '%P')}],

            # The lambda functions below are used to call the 
            # assignPinAutomatically method with the argument "LED". This is done 
            # to prevent the method from being called when the dictionary is 
            # created. Otherwise, the method would be called when the dictionary is 
            # created and the value would be the same for all the entries.
            # In this case, only the values 2 and 3 would ever be shown within their
            # respective entry widgets.

            
            "LED Pin Numbers": [MultipleAutoEntryButtons, {"numberOfEntries":2, "labels":["LED Physical Pin Number", "LED BCM Pin Number"]}], 

            "Button Pin Numbers": [MultipleAutoEntryButtons, {"numberOfEntries":2, "labels":["Button Physical Pin Number", "Button BCM Pin Number"]}],


           


        }

    
        # create a JLB to store user defined settings and data
        self.listBox= JSONListbox(self.root, title='Interactive Units', button_placement= 'bottom', addFields=JSONFields, editFields=editJSONFields)
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
    
        # TODO: create functions for JSONListbox's create/edit/delete/copy/paste extra methods to handle pin rental and assignment in GPIOPinner.


# make the extra functions/closing functions for the JSONListbox widget with 
# the idea that they will be used to handle the creation, editing, deletion, 
# copying, and pasting of Interactive Units (IUs) within the JSONListbox widget.
#
# The key point to remember is that you, the programmer, are responsible for   # defining the JSON format of all elements within the JSONListbox. Therefore,
# you have defined the format of the JSON(s) that these functions will recieve # as input. These inputs will be either a dictionary or a list of dictionaries 
# representing the elements currently selected within the JSONListbox.
#
# 
    def addElementExtraFunctions(self,item:dict):
        """A function to create the extra functions for the JSONListbox widget. These functions are used to handle the creation, editing, deletion, copying, and pasting of Interactive Units (IUs) within the JSONListbox widget.
        """
        pinsToAssign = [item[key] for key in item.keys() if "Physical Pin Number" in key]

        for key in item.keys():

            if "Pin Number" in key:
                if "Physical" in key:
                    self.pinner.assignPinManually(item["Name"], item[key])

    def onClosingAdd(self):
        """A function to execute when the user clicks on the exit button on the window. This function is used to handle the closing of the add element window.
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.pinner.clearRentedPins() # clear the rented pins in the GPIOPinner class
            self.root.destroy()
    
 