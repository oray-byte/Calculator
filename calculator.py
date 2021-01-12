# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 14:40:03 2021

@author: Chunky (oray-byte)
"""

import tkinter as tkr
import tkinter.messagebox as tkrm
from typing import List

class Calculator(tkr.Frame):
    """Main frame that the calculator will be held in"""
    
    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.master = master
        tkr.Frame.pack(self)
        self.init_frame()

    def append_to_frame(self, btn, canvas) -> None:
        """
        Takes the value of the pressed-button's text and appends it
        to the current text of the canvas.
        """
        canvas.delete("all")
        canvas.create_text(120, 50, text=btn.cget("text"))
    
            
    def init_button(self, btn, text, canvas) -> tkr.Button:
        """Initializes the buttons."""
        btn["width"] = 10
        btn["height"] = 5
        btn["text"] = text
        btn["command"] = (lambda btn=btn: self.append_to_frame(btn, canvas)) 
        return btn
        
    def reorder_array(self, array, row=0) -> List[tkr.Button]:
        """
        Reorders the numbers array where the buttons are
        similar to that of a number pad
        """
        start = row * 3 # Needs to be reordered in sets of three
        temp = array[start:(start + 3)]
        r_temp = temp[::-1] # Same as temp.reverse()
        array[start:(start + 3)] = r_temp # Replace the portion needed of reordered with the reordered portion
        return array

    def init_frame(self) -> None:
        self.master.title("Calculator") # Sets title of the frame to "Calculator"
        buttonFrame: tkr.Frame = tkr.Frame(self, height=100, width=200, bg="cyan") # Frame that holds the buttons
        canvasFrame: tkr.Frame = tkr.Frame(self, height=100, width=200, bd=5, ) # Frame that holds the screen/canvas
        canvas: tkr.Frame = tkr.Canvas(canvasFrame, width=200, height=100, bg="cyan") # Where inputed numbers and outputs will be displayed
        previous: str = '' # Contains previously entered number
        current: str = '' # Contains current number
        init_n_buttons = [tkr.Button(buttonFrame, text="{}".format(9-x)) for x in range(10)] # Basic buttons with no functionality. Used so I can use each button for arguements in next declaration
        numbers = [self.init_button(init_n_buttons[x], (9-x), canvas) for x in range(10)] # Added functionality and character to each button
        init_n_buttons = None # Free up memory
        index = 0; # Used to keep track of place in array
        
        buttonFrame.pack(side=tkr.BOTTOM, expand=tkr.TRUE, fill=tkr.X)
        canvasFrame.pack(side=tkr.TOP, expand=tkr.TRUE, fill=tkr.X)

        # |
        # V packs number buttons in an formation similar to a number pad
        for r in range(4): # 4 rows
            for c in range(3): # 3 columns
                if r == 3: # For the final row where 0 is in the middle
                    numbers[index].grid(row=r, column=(c+1))
                    index = None # Free up memory
                    break
                if c == 0:
                    numbers = self.reorder_array(numbers, r)
                numbers[index].grid(row=r, column=c)
                index += 1

        canvas.pack(expand=tkr.YES, fill=tkr.BOTH)
        
root = tkr.Tk()
app = Calculator(root)
root.mainloop()