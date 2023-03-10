# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 10:53:10 2022

@author: Tristian Stolte

Pinder - Tinder for scientific papers, specifically made to help out in systematic literature reviews.
"""
#%% Import modules

import tkinter as tk
from tkinter import ttk
import bibtexparser
import os

#%% Set up working directory

wd = os.path.dirname(os.path.realpath(__file__)) # Current working directory

#%% Set some parameters

# Decide if you want to start with an empty list of refs or not
# True means that you will start with empty lists for the refs2save and refs2remove
new_game = True
# Decide at which index (which paper) you want to start pindering
start_at = 0
#%% Define hazard name

# Choose between:
# "pluvial_flooding", "earthquakes", "heatwaves", "COVID-19", "landslides", "drought", "SLR"

hazard = "TESTING"

# Note that this is relevant when you research mulitple topics for one paper. It could be any topic 

#%% Load the data

# Load the bibtex references (all of them)
with open(os.path.join(wd, "Queries&Hits\\refs_all_{}.bib".format(hazard)), encoding = 'utf8') as bibtex_file:
    bib_database1 = bibtexparser.load(bibtex_file)
# Extract the references as a list of dictionaries
refs = bib_database1.entries

# Check if you want to append to an existing list or start a new list
if new_game == True:
    refs2save   = [] # Empty list
    refs2remove = [] # Emtpy list
else:
    with open(os.path.join(wd, "Queries&Hits\\refs2save_{}.bib".format(hazard)), encoding = 'utf8') as bibtex_file:
        bib_database2 = bibtexparser.load(bibtex_file)  # open bibtex file
    refs2save = bib_database2.entries                   # Convert to list of dicts

    with open(os.path.join(wd, "Queries&Hits\\refs2remove_{}.bib".format(hazard)), encoding = 'utf8') as bibtex_file:
        bib_database3 = bibtexparser.load(bibtex_file)  # open bibtex file
    refs2remove = bib_database3.entries                 # Convert to list of dicts

#%% GUI creation
 
# Class that creates the GUI for pinder
class MainWindow:
    def __init__(self, master, i):
        self.master = master # Define the self.master which will hold the root
        self.i = i           # define the self.i which will determine which paper (title) will be evaluated
                
        self.frame = tk.Frame(self.master, width = 800, height = 400)   # Sets the frame of the GUI
        self.frame.grid()                                               # Not sure what this does
  
        self.title = tk.Label(self.frame, text = refs[self.i]["title"])             # Set an initial paper title
        self.title.grid(row = 0, column = 1, columnspan = 3, pady = 20, padx = 10)  # Title location wihtin the frame
        
        self.counter = tk.Text(self.frame, width = 2, height = 2)   # Keeps track of the paper ID
        self.counter.insert('0.0', self.i)                          # initial value
        self.counter.grid(row = 0, column = 0)                      # Location of the counter
        
        self.abstract = tk.Text(self.frame)                                         # Displays the abstract of the paper
        self.abstract.insert('1.0', refs[self.i]["abstract"])                       # Initial text
        self.abstract['state'] = 'disabled'                                         # Disable the possibility to alter the abstract
        self.abstract.grid(row = 1, column=1, columnspan = 3, pady = 20, padx = 10) # Location of the abstract
        
        self.entry_left_right = tk.Entry(self.frame)                # Create a textbox in which the commands are given to decide if a paper needs to be saved or removed
        self.entry_left_right.grid(row = 2, column = 2, pady= 30)   # Textbox location within the frame
 
        self.scrollbar = ttk.Scrollbar(master, orient = 'vertical', command=self.abstract.yview)    # Adds a scrollbar to the abstract text widget
        self.scrollbar.grid(row=0, column = 1, sticky = tk.NS)                                      # Location of the scrollbar
        self.abstract['yscrollcommand'] = self.scrollbar.set                                        # Connect to the abstract widget
    
        self.instructions = tk.Label(self.frame, 
                                     text = "Start pindering by clicking in the white entry box at the bottom.\nPress <left arrow> to reject a paper.\nPress <right arrow> to accept a paper.\nThe number at the top left indicates the index of the paper to make it easier to keep track of your progress.\nIt is possible to close this screen and save your progress by running the next cell in Python.\n!!DOES NOT WORK YET!!: You can start at the index of choice by filling the number in the top left text box.",
                                     anchor = "e",
                                     justify = 'left')                          # Instructions on pinder  
        self.instructions.grid(row = 3, column = 0, columnspan = 4, padx=10)    # Location of the instructions
        
        self.bindings()     # Refers to the key bindings that the entry box widget (entry_left_right) holds

    def bindings(self):
        """Defines the key bindings"""
        self.entry_left_right.bind('s', lambda event: self.skipPaper())         # Press 's' to skip a paper (neither removed nor saved)
        self.entry_left_right.bind('<Left>', lambda event: self.removePaper())  # Press left arrow to remove a paper
        self.entry_left_right.bind('<Right>', lambda event: self.savePaper())   # Press right arrow to save a paper
        self.entry_left_right.bind('<FocusIn>',lambda event: print("You can now start pindering!"))     # Notify the user that they can start pindering (pressing left or right arrow keys)
        self.entry_left_right.bind('<FocusOut>',lambda event: print("You've just stopped pindering!"))  # Notify the user that they have just stopped pindering
                
    def savePaper(self):
        """Function to save the paper by putting it in a seperate list of dicts"""
        refs2save.append(refs[self.i])  # Append the paper to the list 
        self.i = self.i + 1             # Go to the next paper (title)
        # If the last paper has been reviewed, notify the user
        try:
            self.title.config(text = refs[self.i]['title'])         # Reset title to the next paper's title
            self.counter.delete('0.0', tk.END)                      # Remove all the text in the abstract text box
            self.counter.config()                                   # Reset the counter text box
            self.counter.insert('0.0', self.i)                      # Give the new index (of the next paper)
            self.abstract['state'] = 'normal'                       # Enable altering the abstract text box      
            self.abstract.config()                                  # Reset the abstract text box
            self.abstract.insert('1.0', refs[self.i]["abstract"])   # Place new text in the abstract text box (next paper's abstract)
            self.abstract['state'] = 'disabled'                     # Disable altering the abstract text box
        except:
            self.title.config(text = "DONE! KLAAR! FINITO!")        # Notify the user that they have checked the last paper in the list (the one with the last ID at least)
        print('Saved!') # notify the user what they have chosen
    
    def removePaper(self):
        """Function to remove the paper by putting it in a seperate list of dicts"""
        refs2remove.append(refs[self.i]) # Append the paper to the list
        self.i = self.i + 1              # Go to the next paper (title)
        # If the last paper has been reviewed, notify the user
        try:
            self.title.config(text = refs[self.i]['title'])         # Reset title to the next paper's title
            self.counter.delete('0.0', tk.END)                      # Remove all the text in the abstract text box
            self.counter.config()                                   # Reset the counter text box
            self.counter.insert('0.0', self.i)                      # Give the new index (of the next paper)
            self.abstract['state'] = 'normal'                       # Enable altering the abstract text box      
            self.abstract.config()                                  # Reset the abstract text box
            self.abstract.insert('1.0', refs[self.i]["abstract"])   # Place new text in the abstract text box (next paper's abstract)
            self.abstract['state'] = 'disabled'                     # Disable altering the abstract text box
        except:
            self.title.config(text = "DONE! KLAAR! FINITO!")
        print('Removed!') # notify the user what they have chosen        

    def skipPaper(self):
        "Function to skip a paper in case you are not pindering from the first paper"
        self.i = self.i + 1             # Go to the next paper (title)
        # If the last paper has been reviewed, notify the user
        try:
            self.title.config(text = refs[self.i]['title'])         # Reset title to the next paper's title
            self.counter.delete('0.0', tk.END)                      # Remove all the text in the abstract text box
            self.counter.config()                                   # Reset the counter text box
            self.counter.insert('0.0', self.i)                      # Give the new index (of the next paper)
            self.abstract['state'] = 'normal'                       # Enable altering the abstract text box      
            self.abstract.config()                                  # Reset the abstract text box
            self.abstract.insert('1.0', refs[self.i]["abstract"])   # Place new text in the abstract text box (next paper's abstract)
            self.abstract['state'] = 'disabled'                     # Disable altering the abstract text box
        except:
            self.title.config(text = "DONE! KLAAR! FINITO!")
        print('Skipped!') # notify the user what they have chosen


#%% Start the GUI and play pinder!
root = tk.Tk()
root.title("Pinder V1")
window = MainWindow(root, start_at)
root.mainloop()

#%% Save to bibtext again

# Papers to save
refs2save_bib           = bibtexparser.bibdatabase.BibDatabase() # Create a bibtex file
refs2save_bib.entries   = refs2save                              # Add refs2save to the bibtex file

# Papers to remove
refs2remove_bib         = bibtexparser.bibdatabase.BibDatabase() # Create a bibtex file
refs2remove_bib.entries = refs2remove                            # Add refs2remove to the bibtex file

writer = bibtexparser.bwriter.BibTexWriter()    # Create a writer

# Save the refs that need to be saved 
with open(os.path.join(wd, 'Queries&Hits\\refs2save_{}.bib'.format(hazard)), 'w', encoding = 'utf8') as bibfile:
    bibfile.write(writer.write(refs2save_bib))

# Save the refs that are irrelevant 
with open(os.path.join(wd, 'Queries&Hits\\refs2remove_{}.bib'.format(hazard)), 'w', encoding = 'utf8') as bibfile:
    bibfile.write(writer.write(refs2remove_bib))
