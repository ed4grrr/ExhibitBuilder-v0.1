import os
import tkinter as tk
from ttkwidgets import TimeLine
from Action import Action
class EasyTimeline:
    
    """TODO adapt marker's dictionary to contain a new dictionary with application relevant key value pairs
    
    Find ways to user events to change the user's cursor to a hand when hovering over a marker"""
    
    
    def __init__(self, root: tk.Tk, categoriesDict: dict[str: dict[str, str]], extendTimeline: bool = False, height :int = 100):


        # glossary
        # root: tk.Tk - the root window
        # Category: this works like an audio/video channel within a video editing timeline, markers can be placed in different "channels" or categories.
        # tag: str - a tag that can be applied to markers that changes their properties

        self.root = root # tk.Tk()
        self.timeline = TimeLine( 
            self.root,
            categories=categoriesDict,
            height=height, extend=extendTimeline
        ) 

    
    def getActiveMarkerMetadata(self, *args):
        """Print the metadata of the active marker
        parameters: *args - the arguments passed from the assigned callback"""
        print(self.timeline._markers[args[0]]) # this index is the iid of the active marker in all ttkwidgets.TimeLine callbacks.
        
        # Print the current marker that is active

    def changeActiveMarkerMetadata(self, iid: str, **kwargs):
        """Change the metadata of the active marker
        parameters: iid: str - the iid of the active marker
                    **kwargs - the key value pairs to change in the marker's dictionary"""
        for key, value in kwargs.items():
            self.timeline._markers[iid][key] = value
            

    def getMarkerStartAndEndTimes(self, iid: str):
        """Get the start and end times of a marker
        parameters: iid: str - the iid of the marker"""
        return [self.timeline._markers[iid]["start"], self.timeline._markers[iid]["finish"]]
    
    def returnMarkerRectangle(self, iid: str):
        """Return the rectangle of a marker
        parameters: iid: str - the iid of the marker"""
        print(self.timeline._canvas_markers)
        for key, value in self.timeline._canvas_markers.items():
            print(f"**********{key}**********{value}")
            if value == iid:
                return key

        

    
 
    def createTag(self, tag: str, **kwargs):
        self.timeline.tag_configure(tag, **kwargs)

    def createMarker(self, category: str, start: float, end: float, iid:str, **kwargs):
        # TODO: link the usuable keywords to the ones in the ttkwidgets.TimeLine.create_marker method
        self.timeline.create_marker(category, start, end, iid=iid, **kwargs)
        markerRectangle =self.returnMarkerRectangle(iid)
        print(markerRectangle)


        self.timeline._timeline.tag_bind(markerRectangle,"<Enter>", lambda event: print("mouse entered!") )
        """self.timeline._timeline.itemconfig(markerRectangle, cursor="hand2")"""
        #markerRectangle.bind("<Leave>", lambda event: markerRectangle.config(cursor="arrow"))

    def addTimeline(self):
        self.timeline.draw_timeline()
        self.timeline.grid()

   
        

"""        self.root.after(2500, lambda: self.timeline.configure(marker_background="cyan")) # Change the background color of all markers to cyan after 2.5 seconds

        self.root.after(5000, lambda: self.timeline.update_marker("1", background="red")) # Change the background color of the marker with the id "1" to red after 5 seconds

        self.root.after(5000, lambda: print(self.timeline.time)) # Print the current time of the timeline after 5 seconds"""
        
        





def saveDocumentation(testGPIOButton: TimeLine, testaction: Action):
    
    # Check if the "deviceDocs" directory exists, if not, create it
    device_docs_folder = "./deviceDocs"
    if not os.path.exists(device_docs_folder):
        os.makedirs(device_docs_folder)

    with open("./deviceDocs/" + str(type(testGPIOButton)).split(".")[-1].strip("'>")+".md","w") as file:
        file.write("# "+str(type(testGPIOButton)).split(".")[-1].strip("'>") + "\n\n")
        for element in testaction.actions:
            file.write("*"*10 + "\n")
            
            file.write("**"+ element[0]+ "**\n")
            file.write(str(element[1])+ "\n")
            file.write("*"*10+ "\n\n\n")

if __name__ == "__main__":
    root = tk.Tk() # Create a new Tkinter window


    test ={str(key): {"text": "Category {}".format(key)} for key in range(0, 5)}
    app = EasyTimeline(root,test) # Create a new TimelineDemo object
    

    app.createTag("1", left_callback=app.getActiveMarkerMetadata, foreground="green", 
                                active_background="yellow", hover_border=2, move_callback=lambda *args: print(args)) # Configure the tag "1" to have a right_callback that prints the arguments, a foreground color of green, an active background color of yellow, a hover border of 2, and a move_callback that prints the arguments.
    



    # no marker in category 0, i.e. the first category
    
    app.createMarker("1", 1.0, 2.0, "1",background="white", text="Change Color", tags=("1",)) # Create a new marker in the second category, a start time of 1.0, an end time of 2.0, a background color of white, a text of "Change Color", tags of "1", and an iid of "1". This marker will have the properties of the tag "1".

    
    app.createMarker("2", 2.0, 3.0,"2" , background="green", text="Change Category", foreground="white", 
                                change_category=True) # Create a new marker ins the third category, a start time of 2.0, an end time of 3.0, a background color of green, a text of "Change Category", a foreground color of white, and an iid  of "2". This marker will change category when moved.
    
    
    app.createMarker("3", 1.0, 2.0, "3", text="Show Menu", tags=("1",)) # Create a new marker in the 4th category, a start time of 1.0, an end time of 2.0, a text of "Show Menu", and tags of "1". This marker will have the same properties as the marker with the id "1". However, it will not have a right_callback or move_callback.


    app.createMarker("4", 4.0, 5.0, "4", text="Do nothing", move=False)  # Create a new marker in the fifth category, a start time of 4.0, an end time of 5.0, a text of "Do nothing", and move set to False. This marker cannot be moved.
        
    app.addTimeline() # Add the timeline to the window


    testGPIOButton =app.timeline

    testaction = Action(testGPIOButton)

    root.mainloop() # Start the main loop