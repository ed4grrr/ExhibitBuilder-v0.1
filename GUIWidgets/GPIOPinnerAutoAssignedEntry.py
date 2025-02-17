from tkinter import Entry
from GPIOPinner import GPIOPinner   

class GPIOPinnerAutoAssignedEntry(Entry):

    pinner = GPIOPinner()
    def __init__(self, root=None, **kwargs):
      
        valueToBeShown = GPIOPinnerAutoAssignedEntry.pinner.rentFirstAvailablePin()

        super().__init__(root, **kwargs)
        
        self.insert(0, valueToBeShown)
        self.config(state="readonly")
        self.pack()