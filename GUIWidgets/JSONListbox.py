import tkinter as tk
from tkinter import Listbox, messagebox, simpledialog
from tkinter.ttk import Combobox

import json
from typing import Callable as callableFunction


class JSONListbox(Listbox):
    """
    A custom Listbox widget with additional functionality such as right-click context menu,
    double-click event handling, and clipboard operations (copy, paste, delete, edit).
    Attributes:
        json_data (list): The data to populate the listbox with.
        copy_func (function): Function to handle copy operation.
        paste_func (function): Function to handle paste operation.
        delete_func (function): Function to handle delete operation.
        edit_func (function): Function to handle edit operation.
        copied_items (list): Items that have been copied for pasting.
    Methods:
        __init__(master, json_data, **kwargs): Initializes the CustomListbox with optional JSON data.
        add_scrollbar(): Adds a vertical scrollbar to the listbox.
        create_right_click_menu(copy_func, paste_func, delete_func, edit_func): Creates a right-click context menu.
        show_right_click_menu(event): Displays the right-click context menu at the cursor position.
        populate_listbox(): Populates the listbox with items from json_data.
        on_double_click(event): Handles double-click events on listbox items.
        copy_item(): Copies the selected items to the clipboard.
        paste_item(): Pastes the copied items into the listbox.
        delete_item(): Deletes the selected items from the listbox.
        edit_item(): Opens a window to edit the selected item.
    """

    def __init__(self, master=None, json_data=None, button_placement:str = "bottom", title="JSONListbox", addFields = {"name":[tk.Entry,{}]}, editFields = {str:[tk.Entry,{}]}, padX =0, padY =0, **kwargs):
        """Initialize the CustomListbox with optional JSON data.
        Args:
            fields (dict): A dictionary where the key is the label for the field and the value is a dict with the key being the type of tk input widget to be created and the value is a dict containing the kwargs that control the    properties of the input widget to be created.
            
            master (tk.Tk|tk.Frame): The parent widget.
            
            json_data (list): The data to populate the listbox with.
            
            button_placement (str): The placement of the buttons. Default is 
            
            "bottom". Other valid values are "top", "left", and "right".
            
            **kwargs: Additional keyword arguments for Listbox."""
        
        kwargs['selectmode'] = tk.EXTENDED  # Enable multiple item selection
        

###########################################################################
        # check if the user has provided the extra functions for adding, editing, and deleting items, if not, set them to None. These functions will be used to add extra functionality to the buttons. They will NOT be used to replace the default functionality of the buttons, only to add to them.
        try:
            self.addItemExtraFunctionList = kwargs["addItemsExtraFunctions"]
        except KeyError:
            self.addItemExtraFunctionList = None

        try:
            self.onEditClosingFunction = kwargs["onEditClosingFunction"]

        except KeyError:
            self.onEditClosingFunction = None

        try:
            self.onAddClosingFunction = kwargs["onAddClosingFunction"]
        except KeyError:
            self.onAddClosingFunction = None




        try:
            self.editItemsExtraFunctionList = kwargs["editItemsExtraFunctions"]
        except KeyError:
            self.editItemsExtraFunctionList = None

        try:    
            self.deleteItemsExtraFunctionList = kwargs["deleteItemsExtraFunctions"]
        except KeyError:
            self.deleteItemsExtraFunctionList = None   

        try:
            self.copyItemsExtraFunctionList = kwargs["copyItemsExtraFunctions"]
        except KeyError:
            self.copyItemsExtraFunctionList = None

        try:
            self.pasteItemsExtraFunctionList = kwargs["pasteItemsExtraFunctions"]
        except KeyError:
            self.pasteItemsExtraFunctionList = None 

###########################################################################

###########################################################################
        #general TKinter + custom widgets setup
        self.addFields = addFields
        self.editFields = editFields
        self.masterFrame = tk.Frame(master, highlightbackground="black", 
        highlightthickness=1) # Create a frame to contain the Listbox
        self.titleLabel = tk.Label(self.masterFrame, text=title)
        super().__init__(self.masterFrame, **kwargs) # Initialize the Listbox
        self.JSONData = json_data if json_data else [] # Initialize JSON data
        self.add_scrollbar() # Add a vertical scrollbar
        self.bind('<Double-1>', self.on_double_click) # Bind double-click event
        self.create_right_click_menu() # Create right-click context menu
        self.bind('<Button-3>', self.show_right_click_menu)  # Bind right-click to show menu
        self.populate_listbox() # Populate the listbox
        # Create buttons
        button_frame = tk.Frame(self.masterFrame)
       
        
        # allows the user to place the buttons on any side of the listbox
        button_side = "top" if button_placement.lower() in ["left","right"] else "left"

        # Button creation

        create_button = tk.Button(button_frame, text="Create Element", command=self.add_item)
        

        edit_button = tk.Button(button_frame, text="Edit Element", command=self.edit_item)
        

        copy_button = tk.Button(button_frame, text="Copy Element(s)", command=self.copy_item)
        

        paste_button = tk.Button(button_frame, text="Paste Element(s)", command=self.paste_item)
        

        delete_button = tk.Button(button_frame, text="Delete Element(s)", command=self.delete_item)
        
        self.titleLabel.pack(side="top" if button_placement.lower() in ["left","right", "bottom"] else "bottom")
        create_button.pack(side=button_side, padx=5, pady=5)
        edit_button.pack(side=button_side, padx=5, pady=5)
        copy_button.pack(side=button_side, padx=5, pady=5)
        paste_button.pack(side=button_side, padx=5, pady=5)
        delete_button.pack(side=button_side, padx=5, pady=5)
        button_frame.pack(side=button_placement.lower(), fill="x")
        self.pack(fill="both", expand=True) # Pack the listbox to fill the parent widget
        self.masterFrame.pack(fill="both", expand=True, pady = padY, padx =padX)


    def add_scrollbar(self):
        """Add a vertical scrollbar to the listbox."""
        scrollbar = tk.Scrollbar(self.master, orient="vertical", command=self.yview)   # Create a vertical scrollbar
        self.config(yscrollcommand=scrollbar.set) # Configure the listbox to use the scrollbar
        scrollbar.pack(side="right", fill="y") # Pack the scrollbar to the right of the listbox

    def create_right_click_menu(self, copy_func:callableFunction=None, paste_func:callableFunction=None, delete_func:callableFunction=None, edit_func:callableFunction=None):
        """Create a right-click context menu with copy, paste, delete, and edit options.
        Args:
            copy_func (function): Function to handle copy operation.
            paste_func (function): Function to handle paste operation.
            delete_func (function): Function to handle delete operation.
            edit_func (function): Function to handle edit operation
            
        The provided functions should be useful for most applications, but can be overridden by the programmer if necessary"""
        

        # Default functions for copy, paste, delete, and edit operations if not provided by user
        copy_func = copy_func if copy_func is not None else self.copy_item
        paste_func = paste_func if paste_func is not None else self.paste_item
        delete_func = delete_func if delete_func is not None else self.delete_item
        edit_func = edit_func if edit_func is not None else self.edit_item
        
        

        self.menu = tk.Menu(self, tearoff=0) # Create a right-click context menu
        
        self.menu.add_command(label="Copy", command=copy_func)  # Add a "Copy" option to the menu
        self.bind('<Control-c>', lambda event: copy_func()) # Bind Ctrl+C to copy function
       
        
        self.menu.add_command(label="Paste", command=paste_func) # Add a "Paste" option to the menu
        self.bind('<Control-v>', lambda event: paste_func())# Bind Ctrl+V to paste function
      

        self.menu.add_command(label="Delete", command=delete_func) # Add a "Delete" option to the menu
        self.bind('<Delete>', lambda event: delete_func()) # Bind Delete key to delete function
      

        self.menu.add_command(label="Edit", command= edit_func)# Add an "Edit" option to the menu
        self.bind('<Control-e>', lambda event: edit_func())# Bind Ctrl+E to edit function

    def show_right_click_menu(self, event:tk.Event):
        """Display the right-click context menu at the cursor position.
        Args:
            event (tk.Event): The right-click event."""
        self.menu.post(event.x_root, event.y_root) # Display the menu at the cursor position

    def populate_listbox(self):
        """Populate the listbox with items from json_data.
        
        This method clears the listbox and inserts formatted items from the JSON data. Use this method every time the JSON data is updated."""
        
        self.delete(0, tk.END) # Clear the listbox
        for item in self.JSONData: # Iterate over each item in the JSON data

            formatted_item = [f"{key} : {value}" for key, value in item.items()] # Format the item as key-value pairs
            insertableString = "" # Initialize an empty string for inserting into the listbox

            for item in formatted_item:     # Iterate over each key-value pair
                insertableString += item + " | " 
            insertableString = insertableString.strip(" | ") # Remove trailing separator
            self.insert(tk.END, insertableString) # Insert the formatted item into the listbox


    def on_double_click(self):
        """Handle double-click events on listbox items.
        Args:
            event (tk.Event): The double-click event."""
        selection = self.curselection() # Get the selected item(s)
        if selection: # If an item is selected
            for index in selection: # Iterate over each selected item
                value = self.get(index) # Get the value of the selected item
                print(f"Selected item: {value}") # Print the selected item

    def _executeExtraFunction(self, functionList, *args, **kwargs):
        """execute given extra functions given the selection(s) as an argument

        This method is used to execute the extra functions provided by the programmer. The functionList is a list of functions that will be called with the selection as an argument. The selection is JSON of the selected item(s) in the listbox. This method is used to add extra functionality to the buttons. It will not replace the default functionality of the buttons, only add to them.

        Args:
            functionList (list): A list of functions to be executed
            selection (list): The selected item(s) in the listbox

        """
        if functionList != None:
            for function in functionList:
                # call the function and provide the current selection for use by the programmer
                function(*args, **kwargs)

    def copy_item(self):
        """Copy the selected items to the clipboard.
        
        This method stores the selected items in the copied_items attribute for pasting. Can be used to a single item or multiple items. The items will be inserted at the selected index. No items will be copied if no items are selected."""
        selection = self.curselection() # Get the selected item(s)
        if selection: # If an item is selected
            
            # This is placed here to do anything the programmer wants to do with the copied items before they are copied
            self._executeExtraFunction(self.copyItemsExtraFunctionList, selection)
            
            self.copied_items = [self.JSONData[i] for i in selection]  # Copy the selected item(s)

        

    def paste_item(self):
        """Paste the copied items into the listbox.
        
        This method inserts the copied items at the selected index in the listbox. If no item is selected, no items are copied to the listbox."""
        if hasattr(self, 'copied_items'): # If items have been copied
            selection = self.curselection()     # Get the selected item(s)
            if selection:   # If an item is selected
                # This is placed here to do anything the programmer wants to do with the copied items before they are pasted
                self._executeExtraFunction(self.pasteItemsExtraFunctionList, self.copied_items)
                for i, item in enumerate(self.copied_items):    # Iterate over each copied item
                    self.JSONData.insert(selection[0] + i, item)   # Insert the copied item at the selected index
                self.populate_listbox()     # Repopulate the listbox

        

    def delete_item(self):
        """Delete the selected items from the listbox.
        
        This method deletes the selected items from the listbox. A confirmation dialog is displayed before deletion. This method can delete either a single item or multiple items and will not delete any items if no items are selected."""
        selection = self.curselection()     # Get the selected item(s)
        if selection:  # If an item is selected
            if messagebox.askyesno("Delete", "Are you sure you want to delete the selected items?"): # Confirm deletion
                # Call the extra functions if they are provided
                self._executeExtraFunction(self.deleteItemsExtraFunctionList, selection)
                for index in reversed(selection):   # Iterate over each selected item in reverse order
                    del self.JSONData[index]  # Delete the item from the JSON data
                self.populate_listbox()    # Repopulate the listbox
        


    def edit_item(self):
        """Open a window to edit the selected item.
        
        This method opens a window to edit the selected item. The window displays the key-value pairs of the item, allowing the user to modify the values. The edited item is saved back to the JSON data. This method can edit only edit a single item at a time and will not open the edit window if no items are selected."""
        selections = self.curselection() # Get the selected item(s)
        if selections: # If an item is selected
            index = selections[0] # Get the index of the selected item
            item = self.JSONData[index] # Get the selected item
            
            # Call the extra functions if they are provided to edit/react to the edited item
            self._executeExtraFunction(self.editItemsExtraFunctionList, item)
            
            entries, edit_window = self.openEditElementWindow(selection = selections)

            def save_edit():   # Define a function to save the edited item
                
                for key, entry in entries.items():  # Iterate over each key-entry pair
                    item[key] = entry.get() # Update the item with the entry value
                self.JSONData[index] = item # Update the JSON data with the edited item

                

                self.populate_listbox() # Repopulate the listbox

                edit_window.destroy()  # Close the edit window
            edit_window.protocol("WM_DELETE_WINDOW", self.onEditClosingFunction) # Add a protocol to the window to call the onClosingFunction when the window is closed

            tk.Button(edit_window, text="Save", command=save_edit).pack(pady=10) # Create a "Save" button


        

    def add_item(self):
        """Open a window to add a new item.
        Args:
            fields (dict): A dictionary where the key is the label for the field and the value is a dict with the key being the type of tk input widget to be created and the value is a dict containing the kwargs that control the properties of the input widget to be created.
            
            This method opens a window to add a new item to the listbox. The window displays entry fields for the keys provided. The new item is saved back to the JSON data. The fields parameter is used to specify the labels and input widgets for the new item. The new item is added to the end of the listbox by default, but the user can select an index to insert the item at a specific position."""
        selection = self.curselection() # Get the selected item(s)
        index = selection[0] if selection else tk.END # Get the index of the selected item or set to end

        window,entries= self.openCreateEditWindow("Add Item") # Call the extra functions if they are provided

        def save_add(): # Define a function to save the new item
            new_item = {label: widget.get() for label, widget in entries.items()} # Create a new item from the entries
            
            # Call the extra functions if they are provided to edit/react to the new item
            self._executeExtraFunction(self.addItemExtraFunctionList, new_item)            
            
            
            if index == tk.END:
                self.JSONData.append(new_item) # Append the new item to the JSON data
            else:
                self.JSONData.insert(index, new_item) # Insert the new item at the selected index
        
          
            self.populate_listbox() # Repopulate the listbox
            window.destroy() # Close the add window

        window.protocol("WM_DELETE_WINDOW", self.onAddClosingFunction) # Add a protocol to the window to call the onClosingFunction when the window is closed

        tk.Button(window, text="Save", command=save_add).pack(pady=10) # Create a "Save" button






    def openCreateEditWindow(self, title, selection = None):
        window = tk.Toplevel(self) # Create a new window for adding
        window.grab_set() # Prevent interaction with the main window
        window.title(title) # Set the window title
        entries = {} # Initialize a dictionary to store entry widgets
        for label, widget_info in self.addFields.items(): # Iterate over each field
            tk.Label(window, text=label).pack() # Create a label for the field
            widget_type = widget_info[0] # Get the type of the widget
            widget_kwargs = widget_info[1] # Get the kwargs for the widget
            widget = widget_type(window, **widget_kwargs) # Create the widget
            widget.pack() # Pack the widget
            entries[label] = widget # Store the widget in the dictionary

        return window, entries
        
    def returnJSON(self):
        print(self.JSONData)
        return self.JSONData
    

    def openEditElementWindow(self, selection):
        window = tk.Toplevel(self)
        window.grab_set()
        window.title("Edit Element")
        entries = {}

        for label, widget_info in self.editFields.items():
            # create a label and the prescribed widget for each field
            # however, make the values in each field the values of the selected item
            tk.Label(window, text=label).pack()
            widget_type = widget_info[0]
            widget_kwargs = widget_info[1]
            print(str(list(widget_kwargs.items())) + "\n" + str(widget_type))
            widget = widget_type(window, **widget_kwargs)
            widget.pack()
            entries[label] = widget
            # set the value of the widget to the value of the selected item
            print(self.JSONData[selection[0]][label])

            if hasattr(widget, "current"): # deals with comboboxes
                    index = widget_kwargs["values"].index(self.JSONData[selection[0]][label])
                    widget.current(index)
            
            if hasattr(widget, "insert"):
                    
                widget.insert(0, self.JSONData[selection[0]][label])
                
            elif hasattr(widget, "set"):
                
                widget.set(self.JSONData[selection[0]][label])
            


        return entries, window
    
    def get(self, first, last = None):
        return super().get(first, last)


# Example usage
if __name__ == "__main__":
    root = tk.Tk() # Create a Tkinter root window
    json_data = [
        {f"name": f"Item {x}", "value": x} for x in range(1, 112)
    ] # Sample JSON data

    JSONFields = {
        "SoundFilePath": [tk.Entry, {}],
        "During Push or After Push": [Combobox, {"values":["During Push", "After Push", ], "state":"readonly"}],
    }
    listbox = JSONListbox(root, json_data=json_data, fields =JSONFields) # Create a CustomListbox with JSON data
    listbox.pack(fill="both", expand=True) # Pack the listbox to fill the window
    print(listbox.JSONData) # use this member to get the JSON list for further processing by the programmer
    root.mainloop() # Start the Tkinter main event loop
    