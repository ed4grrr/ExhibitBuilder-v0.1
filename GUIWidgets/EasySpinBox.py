import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Spinbox

class EasySpinBox(Spinbox):
    def __init__(self, root=None, **kwargs):
        super().__init__(root, **kwargs)
        self.values = kwargs.get("values", [])

    def get(self):
        return super().get()

    def insert(self, index, string):
        super().delete(index, "end")
        super().insert(index, string)    
