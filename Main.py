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

    gui =MainGui(root) # Create an instance of the MainGui class

    root.mainloop() # Start the Tkinter main event loop
