#! /usr/bin/env python3.11


from tkinter import *

class screen(Frame):
    """
    A screen is area
    for content in a program
    """
    def __init__(self,master,name):
        Frame.__init__(self,master)
        #Attributes
        self.master=master
        self.name=name
        #Initalise with master
        self.master.addScreen(self)
    def show(self):
        """
        Method will show screen
        """
        self.master.showScreen(self.name)

class screenController(Frame):
    """
    Screen Controller
    will manage screens 
    in the program
    """
    def __init__(self,parent):
        Frame.__init__(self,parent)
        #Configure
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        #Attributes
        self.allScreens={}
        self.currentScreen=None

    def addScreen(self,screenObject):
        """
        Adds a Screen object to the screenController
        """
        #Place the screen
        screenObject.grid(row=0, column=0, sticky="nsew")
        #Add to dictionary
        self.allScreens[screenObject.name]=screenObject

    def showScreen(self,screenName):
        if screenName in self.allScreens:
            #Display
            self.allScreens[screenName].tkraise()
            #Update variable
            self.currentScreen=screenName
            
    
#Create a Tkinter Window
window=Tk()
window.title("Multiple Screens")
window.geometry("400x300")
window.columnconfigure(0,weight=1)
window.rowconfigure(1,weight=1)


#Create a Controller for the screens
screenMaster=screenController(window)
screenMaster.grid(row=1,column=0,sticky="NSEW")

#Create SCREEN 1
screen1=screen(screenMaster, "S1")
Label(screen1,text="This is screen 1").grid(row=0,column=0) 
screen1.config()

#Create SCREEN 2
screen2=screen(screenMaster, "S2")
Label(screen2,text="This is screen 2").grid(row=0,column=0) 
screen2.config()

#Create SCREEN 3
screen3=screen(screenMaster, "S3")
Label(screen3,text="This is screen 3").grid(row=0,column=0) 
screen3.config()

#Create a navigation bar
navBar=Frame(window)
navBar.grid(row=0,column=0,sticky="EW")
navBar.config(bg="#F1F0F2")

b1=Button(navBar,text="Screen 1",command=lambda: screen1.show())
b1.grid(row=0,column=0)

b1=Button(navBar,text="Screen 2",command=lambda: screen2.show())
b1.grid(row=0,column=1)

b1=Button(navBar,text="Screen 3",command=lambda: screen3.show())
b1.grid(row=0,column=2)


#Show screen 1 by default
screen1.show()

window.mainloop()
