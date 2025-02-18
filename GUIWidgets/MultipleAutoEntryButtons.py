from GUIWidgets.AutoEntryButton import AutoEntryButton
from tkinter import Label, Widget, Frame
class MultipleAutoEntryButtons(Widget):
    def __init__(self,  root=None, valuesToBeShown = [], **kwargs):
        """A class to create multiple AutoEntryButtons in a grid layout
        
        Args:
            numberOfEntries (int): The number of entries to create
            valuesToBeShown (list): A list of strings to be shown in the entries. The length of this list must be equal to the numberOfEntries parameter.
            root (tk.Tk): The root window for the program. Defaults to None.
            **kwargs: Additional keyword arguments to be passed to the AutoEntryButton class.
        """

      
        
        if "numberOfEntries" not in kwargs:
            raise ValueError("The numberOfEntries parameter is required.")
        numberOfEntries = kwargs.pop("numberOfEntries")

        if "labels" not in kwargs:
            raise ValueError("The labels parameter is required.")
        labels = kwargs.pop("labels")
        
        try:
            self.valuesToBeShown = valuesToBeShown()
        except:
            self.valuesToBeShown = valuesToBeShown

        # check if the length of valuesToBeShown is equal to the numberOfEntries parameter
        if len(self.valuesToBeShown) != numberOfEntries:
            self.valuesToBeShown = [""] * numberOfEntries
        
        self.Boxes = []
        self.Labels = []
        self.frames = []

        for box in range(numberOfEntries):
            frame =Frame(root)
            self.frames.append(frame)
            label = Label(frame, text=labels[box])
            self.Labels.append(label)
            label.pack()    
            self.Boxes.append(AutoEntryButton(frame, valueToBeShown=self.valuesToBeShown[box],**kwargs))
   
            
            
    def pack(self):
        """A function to pack the AutoEntryButtons in a grid layout
        
        Args:
            self (MultipleAutoEntryButtons): The MultipleAutoEntryButtons object
        """
        for box in range(len(self.Boxes)):
            self.frames[box].pack()
            
    def get(self):
        """A function to get the values of the AutoEntryButtons
        
        Args:
            self (MultipleAutoEntryButtons): The MultipleAutoEntryButtons object
        """
        return {label["text"]:box.get() for box, label in zip(self.Boxes,self.Labels)}
    

    def insert(self, index, strings):
        """A function to insert a string into the AutoEntryButtons
        
        Args:
            self (MultipleAutoEntryButtons): The MultipleAutoEntryButtons object
            string (str): The string to be inserted into the AutoEntryButtons
        """
        if type(strings) == dict:
            strings = strings.values()
        for box, string in zip(self.Boxes,strings):
            box.config(state="normal")
            box.delete(index, "end")
            box.insert(index, string)
            box.config(state="readonly")

    def deleteAll(self,index1, index2):
        """A function to delete a string from the AutoEntryButtons
        
        Args:
            self (MultipleAutoEntryButtons): The MultipleAutoEntryButtons object
            index1 (int): The index of the first character to be deleted
            index2 (int): The index of the last character to be deleted
        """
        for box in self.Boxes:
            box.config(state="normal")
            box.delete(index1, index2)
            box.config(state="readonly")
