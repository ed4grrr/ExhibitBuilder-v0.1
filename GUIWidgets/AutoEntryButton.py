from tkinter import Entry

class AutoEntryButton(Entry):
    def __init__(self, root=None, **kwargs):
        # get valueToBeShown from kwargs and remove it from kwargs
        
        try:
            # get the valueToBeShown from kwargs and remove it from kwargs
            # this value is a callable function that will return a string to be shown in the entry. Lambdas should be provided in the form of lambda: stringReturningFunction(anyArgs). The lambda function is used to prevent the function from being called when the dictionary is created. Otherwise, the function would be called when the dictionary is created and the value would be the same for all the entries.
            valueToBeShown = kwargs.pop("valueToBeShown")
            if callable(valueToBeShown):
                valueToBeShown = valueToBeShown()
            else:
                valueToBeShown = valueToBeShown
        except KeyError:
            valueToBeShown = "NO STRING GIVEN"
        super().__init__(root, **kwargs)
        
        self.insert(0, valueToBeShown)
        self.config(state="readonly")
        self.pack()

    def get(self):
        """A function to get the value of the entry
        
        Args:
            self (AutoEntryButton): The AutoEntryButton object
        
        Returns:
            str: The value of the entry
        """
        return super().get()
    def insert(self, index, string):
        """A function to insert a string into the entry
        
        Args:
            self (AutoEntryButton): The AutoEntryButton object
            string (str): The string to be inserted into the entry
        """
        self.config(state="normal")
        super().delete(0, "end")
        super().insert(index, string)
        self.config(state="readonly")

    def delete(self, index1, index2):
        """A function to delete a string from the entry
        
        Args:
            self (AutoEntryButton): The AutoEntryButton object
            index1 (int): The index of the first character to be deleted
            index2 (int): The index of the last character to be deleted
        """
        self.config(state="normal")
        super().delete(index1, index2)
        self.config(state="readonly")
        