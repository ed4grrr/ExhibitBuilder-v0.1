import tkinter as tk
import re
from GUIWidgets.JSONListbox import JSONListbox
from GUIWidgets.FilePathEntry import FilePathEntry
from GUIWidgets.AutoEntryButton import AutoEntryButton
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox
from ScriptBuilder.ScriptBuilder import ScriptBuilder
from GUIWidgets.GPIOPinner import GPIOPinner
from MainGui import MainGui






if __name__ == '__main__':





    root = tk.Tk() # Create a Tkinter root window




    def validate_float(stringToValidate) -> bool:
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


    gui =MainGui(root) # Create an instance of the MainGui class


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
        "Volume": [tk.Spinbox, {"values":tuple([floatValue/100 for floatValue in range(101)]), "validate":"all", "validatecommand":(root.register(validate_float), '%P')}],


        # The lambda functions below are used to call the 
        # assignPinAutomatically method with the argument "LED". This is done 
        # to prevent the method from being called when the dictionary is 
        # created. Otherwise, the method would be called when the dictionary is 
        # created and the value would be the same for all the entries.
        # In this case, only the values 2 and 3 would ever be shown within their
        # respective entry widgets.

        "LED GPIO Pin": [AutoEntryButton, {"valueToBeShown": lambda : gui.pinner.returnFirstAvailablePin()}], 


        "Button GPIO Pin": [AutoEntryButton, {"valueToBeShown": lambda : gui.pinner.returnFirstAvailablePin()}]
    }

    # Use the created fields dictionary to set the fields for the JSONListbox
    # This will automatically create the necessary entry widgets for the user to
    # enter data when creating/editing a new JSON object (in this case, an 
    # Interactive Unit). 
    gui.listBox.fields = JSONFields

    



    root.mainloop() # Start the Tkinter main event loop
