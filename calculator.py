# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 14:40:03 2021

@author: Chunky (oray-byte)
"""

import tkinter as tkr
import tkinter.messagebox as tkrm # Using as a debug tool
import tkinter.font as tkrf
from typing import List

class Calculator(tkr.Frame):
    """Main frame that the calculator will be held in"""
    previous: str = ''
    current: str = ''
    operator: str = ''
    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.master = master
        tkr.Frame.pack(self)
        self.init_frame()

# ------Button Highlights------------------------------------------------------
    def _on_enter(self, widget) -> None:
        widget.widget["background"] = "DarkOrchid3"
    
    def _on_leave(self, widget) -> None:
        widget.widget["background"] = "gray19"
# -----------------------------------------------------------------------------

# ------Useful Functions-------------------------------------------------------
    def _clear(self, *args) -> None:
        for canvas in args:
            canvas.delete("all")

    def _format_string(self, temp) -> str:
        
        # FIXME Add functionality to chop off unnessessary zeros
        # FIXME Add functionality to add commas for each 3 digits before .
        return "{:.2f}".format(temp)

    def _operator_input(self, function, topCanvas, bottomCanvas, operator) -> None:
        if self.current != '':
            self._clear(topCanvas, bottomCanvas)
            self.previous = self.current + " {}".format(operator)
            self.current = ''
            function(self.previous, topCanvas)
            self.operator = operator
        else:
            self._clear(topCanvas)
            self.previous = self.previous + " {}".format(operator)
            function(self.previous, topCanvas)
            self.operator = operator
        
    def _do_math(self, function, topCanvas, bottomCanvas, operator=None):
        temp: float = 0
        if operator == "x²":
            if self.current != '':
                temp = float(self.current) ** 2
            else:
                temp = float(self.previous) ** 2
        if self.previous != '' and self.previous != 'x²':
            if operator == "+":
                temp = float(self.previous.split()[0]) + float(self.current)
            elif operator == "-":
                temp = float(self.previous.split()[0]) - float(self.current)
            elif operator == "x":
                temp = float(self.previous.split()[0]) * float(self.current)
            elif operator == "÷":
                if self.current == '0':
                    self._clear(topCanvas, bottomCanvas)
                    self.current = ''
                    self.previous = ''
                    self.operator = ''
                    tkrm.showinfo("Error", "Cannot divide by zero")
                    return
                else:
                    temp = float(self.previous.split()[0]) / float(self.current)

        self.previous = self._format_string(temp)
        self.current = ''
        self.operator = ''
        self._clear(topCanvas, bottomCanvas)
        function(self.previous, topCanvas)
        
    def init_button(self, btn, topCanvas, bottomCanvas) -> tkr.Button:
        """Initializes the buttons."""
        btn["width"] = 10
        btn["height"] = 5
        btn["bg"] = "gray19"
        btn["bd"] = 4
        btn["relief"] = tkr.RIDGE
        btn["fg"] = "snow"
        btn["activeforeground"] = "snow"
        btn["activebackground"] = "DarkOrchid1"
        btn.bind("<Enter>", self._on_enter)
        btn.bind("<Leave>", self._on_leave)
        btn["command"] = (lambda btn=btn: self._append_to_frame(btn, topCanvas, bottomCanvas)) 
        return btn
        
    def reorder_array(self, array, row=0) -> List[tkr.Button]: # Now Obsolete
        """
        Reorders the numbers array where the buttons are
        similar to that of a number pad
        """
        start = row * 3 # Needs to be reordered in sets of three
        temp = array[start:(start + 3)]
        r_temp = temp[::-1] # Same as temp.reverse()
        array[start:(start + 3)] = r_temp # Replace the portion needed of reordered with the reordered portion
        return array
    
    def pack_numbers(self, buttonFrame, topCanvas, bottomCanvas, buttonFont) -> None:
        buttonLabels = ["DEL", "AC", "x²", "+",
                        "7", "8", "9", "-",
                        "4", "5", "6", "÷",
                        "1", "2", "3", "x",
                        "±", "0", ".", "="]
        init_buttons: List[tkr.Button] = [tkr.Button(buttonFrame, 
                                                     text="{}".format(text), 
                                                     font=buttonFont) for text in buttonLabels] # Basic buttons with no functionality. Used so I can use each button for arguements in next declaration
        buttons: List[tkr.Button] = [self.init_button(button, topCanvas, bottomCanvas) for button in init_buttons] # Added functionality and character to each button
        index: int = 0 # Used to keep track of place in array
        # |
        # V packs number buttons in an formation similar to a number pad
        for r in range(5): # 5 rows
            for c in range(4): # 4 columns
                buttons[index].grid(row=r, column=c)
                index += 1
# -----------------------------------------------------------------------------        
    def _append_to_frame(self, btn, topCanvas, bottomCanvas) -> None:
        """
        Takes the value of the pressed-button's text and appends it
        to the current text of the canvas.
        """
        canvasFont: tkrf.Font = tkrf.Font(self, family="Stencil", size="25")

        c_text = (lambda text, canvas:
                  canvas.create_text(390, 50, text=text, fill="snow",
                                     font=canvasFont, anchor=tkr.E))

        if ((str(btn.cget("text")).isnumeric()) or ((str(btn.cget("text")) == ".") and (self.current.count(".") < 1))):
            self.current = self.current + str(btn.cget("text"))
            self._clear(bottomCanvas)
            c_text(self.current, bottomCanvas)
            
        # Handles functionality when DEL button is pressed
        if btn.cget("text") == "DEL":
            self.current = self.current[:-1]
            # bottomCanvas.delete("all")
            self._clear(bottomCanvas)
            c_text(self.current, bottomCanvas) 

        # Handles functionality when ± button is pressed
        if btn.cget("text") == "±":
            if (self.current != '-' or self.current == '') and self.current.count("-") < 1:
                self.current = '-' + self.current
                bottomCanvas.delete("all")
                c_text(self.current, bottomCanvas)
            else:
                self.current = self.current[1:]
                bottomCanvas.delete("all")
                c_text(self.current, bottomCanvas)
        
        # Handles functionality when AC button is pressed
        if btn.cget("text") == "AC":
            self.current = '' # Clears current number
            self.previous = ''
            self.operator = ''
            self._clear(bottomCanvas, topCanvas)
         
        # Handles functionality when = button is pressed
        if btn.cget("text") == "=":
            if self.operator == '': # This is if no operator has been choosen
                self._clear(topCanvas, bottomCanvas)
                # topCanvas.delete("all") # Delete top canvas
                self.previous = self.current # Make current number the previous number
                self.current = '' # Clear current number
                # bottomCanvas.delete("all") # Clear bottom screen
                c_text(self.previous, topCanvas) # Display previous number
            else:
                self._do_math(c_text, topCanvas, bottomCanvas, self.operator) # Display the outcome
        
        # Handles functionality when + button is pressed
        if btn.cget("text") == "+":
            if self.operator == '': # Checks to ensure only one operation is chosen (same for each operation function)
                self._operator_input(c_text, topCanvas, bottomCanvas, "+") # Handles operation input
            else:
                self._do_math(c_text, topCanvas, bottomCanvas, self.operator)
                self._operator_input(c_text, topCanvas, bottomCanvas, "+")
        
        # Handles functionality when - button is pressed
        if btn.cget("text") == "-":
            if self.operator == '':
                self._operator_input(c_text, topCanvas, bottomCanvas, "-")
            else:
                self._do_math(c_text, topCanvas, bottomCanvas, self.operator)
                self._operator_input(c_text, topCanvas, bottomCanvas, "-")
        
        # Handles functionality when - button is pressed
        if btn.cget("text") == "÷":
            if self.operator == '':
                self._operator_input(c_text, topCanvas, bottomCanvas, "÷")
            else:
                self._do_math(c_text, topCanvas, bottomCanvas, self.operator)
                self._operator_input(c_text, topCanvas, bottomCanvas, "÷")
        
        # Handles functionality when x button is pressed
        if btn.cget("text") == "x":
            if self.operator == '':
                self._operator_input(c_text, topCanvas, bottomCanvas, "x")
            else:
                self._do_math(c_text, topCanvas, bottomCanvas, self.operator)
                self._operator_input(c_text, topCanvas, bottomCanvas, "x")
        
        # Handles functionality when x² button is pressed
        if btn.cget("text") == "x²":
            if self.operator == '':
                self.operator = "x²"
                self._do_math(c_text, topCanvas, bottomCanvas, self.operator)
          
        
    def init_frame(self) -> None:
        self.master.title("Calculator") # Sets title of the frame to "Calculator"
        buttonFrame: tkr.Frame = tkr.Frame(self, height=100, width=200, bg="gray25", bd=0) # Frame that holds the buttons
        canvasFrame: tkr.Frame = tkr.Frame(self, height=200, width=200, bg="gray25", bd=5, relief=tkr.RIDGE) # Frame that holds the screen/canvas
        topCanvas: tkr.Frame = tkr.Canvas(canvasFrame, width=200, height=100, bg="gray25", highlightthickness=0) # Where inputed numbers and outputs will be displayed
        bottomCanvas: tkr.Frame = tkr.Canvas(canvasFrame, width=200, height=100, bg="gray25", highlightthickness=0)
        
        buttonFont: tkrf.Font = tkrf.Font(self, family="Century Gothic", size="11")
        buttonFrame.pack(side=tkr.BOTTOM, expand=tkr.TRUE, fill=tkr.X)
        canvasFrame.pack(side=tkr.TOP, expand=tkr.TRUE, fill=tkr.X)
        
        self.pack_numbers(buttonFrame, topCanvas, bottomCanvas, buttonFont)
        
       

        topCanvas.pack(side=tkr.TOP, expand=tkr.YES, fill=tkr.BOTH)
        bottomCanvas.pack(side=tkr.BOTTOM, expand=tkr.YES, fill=tkr.BOTH)
        
root = tkr.Tk()
app = Calculator(root)
root.mainloop()