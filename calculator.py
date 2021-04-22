# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 14:40:03 2021

@author: Chunky (oray-byte)
"""

import tkinter as tkr
import tkinter.messagebox as tkrm # Using as a debug tool
import tkinter.font as tkrf
from typing import List
import ctypes

class Calculator(tkr.Frame):
    """Main frame that the calculator will be held in"""
    previous: str = ''
    current: str = ''
    operator: str = ''
    memoryWindowState: bool = False
    memory: List[str] = []

    def __init__(self, master=None) -> None:
        super().__init__(master)
        self.master = master
        self.menu = tkr.Menu(self.master, bg="gray25")
        self.master.config(menu=self.menu)
        tkr.Frame.pack(self)
        self.init_frame()

# ------Button Highlights------------------------------------------------------
    def _on_enter(self, widget) -> None:
        widget.widget["background"] = "DarkOrchid3"
    
    def _on_leave(self, widget) -> None:
        widget.widget["background"] = "gray19"
# -----------------------------------------------------------------------------

# ------Useful Functions-------------------------------------------------------
    def _update_state(self) -> None:
        if self.memoryWindowState: self.memoryWindowState = False
        else: self.memoryWindowState = True

    def _clear(self, *args) -> None:
        """
        Used for quickly clearing what is wanted
        """
        for arg in args:
            if arg == "p": self.previous = ''
            elif arg == "o": self.operator = ''
            elif arg == "c": self.current = ''
            else: arg.delete("all")

    def _format_string(self, temp) -> str:
        """
        Makes the number on screen look nice
        Adds commas to the number and limits the decimal place to 5 digits
        """
        # FIXME Replace this!
        if temp in ["-", ".", "-."]: # This works but I do not like it
            return temp
        temp = str(temp).replace(",", "")
        if temp.count(".") == 0:
            return "{:,.0f}".format(float(temp))
        else:
            number = len((str(temp).split(".")[1]))
            if number == 1 and str(temp).split(".")[1][0] == '0': number = 0
            elif number > 5: number = 5
            return "{:,.{number}f}".format(float(temp), number=number)

    def _operator_input(self, font, topCanvas, bottomCanvas, operator) -> None:
        if self.current != '':
            self.previous = self._format_string(self.current) + " {}".format(operator)
            self._clear(topCanvas, bottomCanvas, "c")
            # FIXME Do not like this
            topCanvas.create_text(390, 50, text= self.previous,
                                     fill="snow", font=font, anchor=tkr.E)
            self.operator = operator
        else:
            self._clear(topCanvas)
            self.previous = self._format_string(self.previous) + " {}".format(operator)
            # FIXME I also do not like this
            topCanvas.create_text(390, 50, text= self.previous,
                                     fill="snow", font=font, anchor=tkr.E)
            self.operator = operator
        
    def _do_math(self, function, topCanvas, bottomCanvas, operator=None):
        answer: float = 0.0
        temp: bool = True # Determines if previous or current format is used
        currentFormat: str = self.current
        previousFormat: str = self.previous

        # Takes commas out to convert into a float
        self.current = self.current.replace(",", "")
        self.previous = self.previous.replace(",", "")

        if operator == "x²":
            if self.current != '':
                answer = float(self.current) ** 2
                
            elif self.previous != '':
                answer = float(self.previous) ** 2
                temp = False
        else:
            if operator == "÷":
                operator = "/"
            elif operator == "x":
                operator = "*"

            expression: str = "{} {} {}".format(self.previous.split()[0],
                                                operator, self.current)
            answer = eval(expression)

        # Appends equations as strings to memory list for the show_memory function to handle          
        if operator == "x²" and temp:
            self.memory.append("{}² = {}".
                           format(currentFormat, self._format_string(answer)))
        elif operator == "x²" and not temp:
            self.memory.append("{}² = {}".
                           format(self._format_string(previousFormat),
                                  self._format_string(answer)))
        else:
            self.memory.append("{} {} = {}".
                           format(previousFormat, currentFormat, 
                                  self._format_string(answer)))

        # Assigns previous(current) to the answer, clears the screen, and appends the answer to top screen
        self.previous = str(answer)
        self._clear(topCanvas, bottomCanvas, "c", "o")
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

# ------Main Functions---------------------------------------------------------       
    def _append_to_frame(self, btn, topCanvas, bottomCanvas) -> None:
        """
        Takes the value of the pressed-button's text and appends it
        to the current text of the canvas.
        """
        canvasFont: tkrf.Font = tkrf.Font(self, family="Stencil", size="25")
        
        # Function used to append inputs and outputs to the screen
        c_text = (lambda text, canvas:
                  canvas.create_text(390, 50, text=self._format_string(text),
                                     fill="snow", font=canvasFont, anchor=tkr.E))

        if ((str(btn.cget("text")).isnumeric()) or ((str(btn.cget("text")) == ".") and (self.current.count(".") < 1))):
            self.current = self.current + str(btn.cget("text"))
            self._clear(bottomCanvas)
            c_text(self.current, bottomCanvas)
            return
            
        # Handles functionality when DEL button is pressed
        if btn.cget("text") == "DEL":
            self.current = self.current[:-1]
            self._clear(bottomCanvas)
            c_text(self.current, bottomCanvas) 
            return

        # Handles functionality when ± button is pressed
        if btn.cget("text") == "±":
            if (self.current != '-' or self.current == '') and self.current.count("-") < 1:
                self.current = '-' + self.current
                self._clear(bottomCanvas)
                c_text(self.current, bottomCanvas)
                return
            else:
                self.current = self.current[1:]
                self._clear(bottomCanvas)
                c_text(self.current, bottomCanvas)
                return
        
        # Handles functionality when AC button is pressed
        if btn.cget("text") == "AC":
            self._clear(bottomCanvas, topCanvas, "p", "o", "c")
            return
         
        # Handles functionality when = button is pressed
        if btn.cget("text") == "=" and self.current != '-':
            if self.operator == '': # This is if no operator has been choosen
                self.previous = self.current # Make current number the previous number
                self._clear(topCanvas, bottomCanvas, "c")
                c_text(self.previous, topCanvas) # Display previous number
                return
            else:
                self._do_math(c_text, topCanvas, bottomCanvas, self.operator) # Display the outcome
                return
        
        # Handles functionality when + button is pressed
        if btn.cget("text") == "+":
            if self.operator == '': # Checks to ensure only one operation is chosen (same for each operation function)
                self._operator_input(canvasFont, topCanvas, bottomCanvas, "+") # Handles operation input
                return
            else:
                self._do_math(c_text, topCanvas, bottomCanvas, self.operator)
                self._operator_input(canvasFont, topCanvas, bottomCanvas, "+")
                return
        
        # Handles functionality when - button is pressed
        if btn.cget("text") == "-":
            if self.operator == '':
                self._operator_input(canvasFont, topCanvas, bottomCanvas, "-")
                return
            else:
                self._do_math(c_text, topCanvas, bottomCanvas, self.operator)
                self._operator_input(canvasFont, topCanvas, bottomCanvas, "-")
                return
        
        # Handles functionality when - button is pressed
        if btn.cget("text") == "÷":
            if self.operator == '':
                self._operator_input(canvasFont, topCanvas, bottomCanvas, "÷")
                return
            else:
                self._do_math(c_text, topCanvas, bottomCanvas, self.operator)
                self._operator_input(canvasFont, topCanvas, bottomCanvas, "÷")
                return
        
        # Handles functionality when x button is pressed
        if btn.cget("text") == "x":
            if self.operator == '':
                self._operator_input(canvasFont, topCanvas, bottomCanvas, "x")
                return
            else:
                self._do_math(c_text, topCanvas, bottomCanvas, self.operator)
                self._operator_input(canvasFont, topCanvas, bottomCanvas, "x")
                return
        
        # Handles functionality when x² button is pressed
        if btn.cget("text") == "x²":
            if self.operator == '':
                self.operator = "x²"
                self._do_math(c_text, topCanvas, bottomCanvas, self.operator)
                return
            
    def show_memory(self):
        """
        Displays memory of recent equations
        """
        # Creates new window when 'Memory' is pressed under memory
        newWindow = tkr.Toplevel(self.master, bg="gray25")
        newWindow.title("Memory")
        newWindow.geometry("500x750")
        
        # Creating a canvas object to display previous equations
        displayFont: tkrf.Font = tkrf.Font(self, family="Stencil", size="20")
        display: tkr.Frame = tkr.Canvas(newWindow, height=400, width=400, bg=newWindow["bg"])
        display.pack(expand=tkr.YES, fill=tkr.BOTH)
        
        # Displaying previous equations
        for i in range(len(self.memory)):
            display.create_text(5, 25 + (i * 25), text=self.memory[i],
                                fill="snow", font=displayFont, anchor=tkr.W)
        newWindow.mainloop()
        newWindow.protocol("WM_DELETE_WINDOW", self._update_state())
            
        # FIXME: Add functionality to update it in real time
        # FIXME: Memory can only display 29 equations. So delete the top equation when another is added
    
    def init_frame(self) -> None:
        self.master.title("Calculator") # Sets title of the frame to "Calculator"
        
        # Adding Memory menu and commands
        memMenu = tkr.Menu(self.menu, tearoff=0, bg="white")
        memMenu.add_command(label="Show", command=self.show_memory)
        # Adding Mode menu and commands
        modeMenu = tkr.Menu(self.menu, tearoff=0, bg="white")
        modeMenu.add_command(label="Graphing", command=None)
        modeMenu.add_command(label="Arithmetic", command=None)

        self.menu.add_cascade(label="Memory", menu=memMenu)
        self.menu.add_cascade(label="Graph", menu=modeMenu)
        
        canvasFrame: tkr.Frame = tkr.Frame(self, height=200, width=200, bg="gray25", bd=5, relief=tkr.RIDGE) # Frame that holds the screen/canvas
        buttonFrame: tkr.Frame = tkr.Frame(self, height=100, width=200, bg="gray25", bd=0) # Frame that holds the buttons
        topCanvas: tkr.Frame = tkr.Canvas(canvasFrame, width=200, height=100, bg="gray25", highlightthickness=0) # Where inputed numbers and outputs will be displayed
        bottomCanvas: tkr.Frame = tkr.Canvas(canvasFrame, width=200, height=100, bg="gray25", highlightthickness=0)
        
        buttonFont: tkrf.Font = tkrf.Font(self, family="Century Gothic", size="11")
        buttonFrame.pack(side=tkr.BOTTOM, expand=tkr.TRUE, fill=tkr.X)
        canvasFrame.pack(side=tkr.TOP, expand=tkr.TRUE, fill=tkr.X)
        
        self.pack_numbers(buttonFrame, topCanvas, bottomCanvas, buttonFont)
        
       

        topCanvas.pack(side=tkr.TOP, expand=tkr.YES, fill=tkr.BOTH)
        bottomCanvas.pack(side=tkr.BOTTOM, expand=tkr.YES, fill=tkr.BOTH)
# -----------------------------------------------------------------------------        

calcRoot = tkr.Tk()
app = Calculator(calcRoot)
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6) # Minimizes Python Console
calcRoot.mainloop()