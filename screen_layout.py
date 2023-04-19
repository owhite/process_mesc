#! /usr/bin/env python3.11

# screen framework came from:
#  https://stackoverflow.com/questions/62484655/how-to-update-refresh-widgets-when-switching-frames-in-tkinter
# could be useful for threading so screen updates dont freeze
#  https://github.com/pratikguru/Instructables/blob/master/uart_visualizer.py

from tkinter import *

# the great big pile of screen layout
class screen(Frame):
    def __init__(self,master,name):
        Frame.__init__(self,master)
        self.master=master
        self.name=name
        # Initalise with master
        self.master.addScreen(self)

    # the one line function that could be replaced by one line
    def show(self):
        self.master.showScreen(self.name)

    def screen1_layout(s):
        Label(s,text="This is screen 1").grid(row=0,column=0) 
        s.config()

    def screen2_layout(s):
        Label(s,text="This is screen 2").grid(row=0,column=0) 
        s.config()

    def screen3_layout(s):
        Label(s,text="This is screen 3").grid(row=0,column=0) 
        s.config()

    def screen4_layout(s):
        Label(s,text="This is screen 4").grid(row=0,column=0) 
        s.config()

# manage screens
class screenController(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)
        #Configure
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        #Attributes
        self.allScreens={}
        self.currentScreen=None

    def addScreen(self,screenObject):
        #Place the screen
        screenObject.grid(row=0, column=0, sticky="nsew")
        #Add to dictionary
        self.allScreens[screenObject.name]=screenObject

    def showScreen(self,screenName):
        if screenName in self.allScreens:
            self.allScreens[screenName].tkraise() # display
            self.currentScreen=screenName # update variable
            

if __name__ == "__main__":
    #Create a Tkinter Window
    gui=Tk()
    gui.title("MESC display")
    gui.geometry("400x300")
    gui.columnconfigure(0,weight=1)
    gui.rowconfigure(1,weight=1)
    
    screenMaster=screenController(gui)
    screenMaster.grid(row=1,column=0,sticky="NSEW")
    
    # Create screens
    screen1 = screen(screenMaster, "S1")
    screen.screen1_layout(screen1)

    screen2 = screen(screenMaster, "S2")
    screen.screen2_layout(screen2)

    screen3 = screen(screenMaster, "S3")
    screen.screen3_layout(screen3)

    screen4 = screen(screenMaster, "S4")
    screen.screen4_layout(screen4)

    # put a navbar on the top
    navBar=Frame(gui)
    navBar.grid(row=0,column=0,sticky="EW")
    navBar.config(bg="#F1F0F2")
    
    keyboard = PhotoImage(file='icons/keyboard.png')
    connect = PhotoImage(file='icons/connect.png')
    settings = PhotoImage(file='icons/settings.png')
    data = PhotoImage(file='icons/view_data.png')

    b1=Button(navBar, image = connect, command=lambda: screen1.show())
    b1.grid(row=0,column=0)
    
    b2=Button(navBar, image = data,command=lambda: screen2.show())
    b2.grid(row=0,column=1)
    
    b3=Button(navBar, image = keyboard, command=lambda: screen3.show())
    b3.grid(row=0,column=3)
    
    b4=Button(navBar, image = settings,command=lambda: screen4.show())
    b4.grid(row=0,column=4)
    
    # let's start with screen1
    screen1.show()
    
    gui.mainloop()
