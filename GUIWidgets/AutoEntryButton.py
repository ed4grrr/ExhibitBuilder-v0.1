from tkinter import Entry

class AutoEntryButton(Entry):
    def __init__(self, root=None, **kwargs):
        # get valueToBeShown from kwargs and remove it from kwargs
        
        try:
            # get the valueToBeShown from kwargs and remove it from kwargs
            # this value is a callable function that will return a string to be shown in the entry. Lambdas should be provided in the form of lambda: stringReturningFunction(anyArgs). The lambda function is used to prevent the function from being called when the dictionary is created. Otherwise, the function would be called when the dictionary is created and the value would be the same for all the entries.
            valueToBeShown = kwargs.pop("valueToBeShown")()
        except KeyError:
            valueToBeShown = "NO STRING GIVEN"
        super().__init__(root, **kwargs)
        
        self.insert(0, valueToBeShown)
        self.config(state="readonly")
        self.pack()
        