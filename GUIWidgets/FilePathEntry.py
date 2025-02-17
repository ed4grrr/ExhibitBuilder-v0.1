from tkinter import Entry, filedialog

class FilePathEntry(Entry):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.filepath = ""
        self.insert(0, "Click to select a file")
        self.config(state="readonly")
        self.bind("<Button-1>", self.openFileDialog)
    
    def openFileDialog(self, event):
        self.filepath = filedialog.askopenfilename(title="Select a Sound File", )
        self.config(state="normal")
        if self.filepath != "":
            self.delete(0, "end")
            self.insert(0, self.filepath)
            self.config(state="readonly")
    
    def get(self):
        return super().get()
    
    def insert(self, index, string):
        self.config(state="normal")
        super().delete(index, "end")
        super().insert(index, string)
        self.config(state="readonly")

    def delete(self, index1, index2):
        self.config(state="normal")
        super().delete(index1, index2)
        self.config(state="readonly")