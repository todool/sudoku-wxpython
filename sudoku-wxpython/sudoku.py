#!/usr/bin/env python
'''sudoku game based on wxpython
posibilities:
    - read a file
    - select a game
    - files are solved and results are checked

future wishes:
    user recording
    presetting of values with small values 1- 9
    hints
    make install file
    windows / ubuntu versions


TODO:

create some files with the right format, search the internet

import file ability based on 81 char string
after file import, select games based on number or random

update check mechanism with sudokusolver

indicate squares 3*3 with thick lines

future actions

optimalisation. Clean coding.

'''
import wx 
import os
from random import randint
from sudokusolver import solved
import wx.grid

class Sudoku(wx.Frame):
    '''main sudoku class'''
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Sudoku")    
        
        # Setting up the menu.
        toolsmenu= wx.Menu()
        menuOpen = toolsmenu.Append(wx.ID_OPEN, "&Open"," Open")
        menuView = toolsmenu.Append(wx.ID_VIEW_DETAILS, "&View"," View ???")
        menuHelp = toolsmenu.Append(wx.ID_HELP, "&About"," About ???")
        menuExit = toolsmenu.Append(wx.ID_EXIT, "E&xit"," Exit ???")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(toolsmenu,"&Tools") # Adding the "toolsmenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.


        #Create the GridCellChoiceEditor with valid values 1-9 list. 
        self.Editor = wx.grid.GridCellChoiceEditor(
        [" ","1","2","3","4","5","6","7","8","9"], allowOthers=False) 

        sizer = wx.BoxSizer(wx.VERTICAL) # Main vertical sizer
        self.sudokuGrid = wx.grid.Grid(self,-1)

        #default Data
        self.startGrid = '000000000000000000000000000000000000000000000000000000000000000000000000000000000'

        numRows = numCols = 9
        cellSize = 50
        self.sudokuGrid.CreateGrid(numRows, numCols)      
        self.sudokuGrid.SetRowLabelSize(0);
        self.sudokuGrid.SetColLabelSize(0);
        self.sudokuGrid.SetDefaultColSize(cellSize, resizeExistingCols=True)
        self.sudokuGrid.SetDefaultRowSize(cellSize, resizeExistingRows=True)


        self.sizer2 = wx.GridSizer(2, 3, 10, 10)
        #self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []
        self.buttons.append(wx.Button(self, -1, "Clear"))
        self.sizer2.Add(self.buttons[0], 1, wx.EXPAND)
        self.buttons.append(wx.Button(self, -1, "Solved?"))
        self.sizer2.Add(self.buttons[1], 1, wx.EXPAND)
        self.buttons.append(wx.Button(self, -1, "Help"))
        self.sizer2.Add(self.buttons[2], 1, wx.EXPAND)
        self.buttons.append(wx.Button(self, -1, "Extra1"))
        self.sizer2.Add(self.buttons[3], 1, wx.EXPAND)
        self.buttons.append(wx.Button(self, -1, "Extra2"))
        self.sizer2.Add(self.buttons[4], 1, wx.EXPAND)
        self.buttons.append(wx.Button(self, -1, "Extra3"))
        self.sizer2.Add(self.buttons[5], 1, wx.EXPAND)
        
        #add sudokugrid to vertical sizer
        sizer.Add(self.sudokuGrid, 0, wx.EXPAND) # Add to main sizer
        sizer.Add(self.sizer2, 0, wx.EXPAND) # Add to main sizer



        # Events.
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        #self.Bind(wx.EVT_MENU, self.OnSave, menuSave)
        #self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        #self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        self.Bind(wx.EVT_BUTTON, self.clear, self.buttons[0])
        self.Bind(wx.EVT_BUTTON, self.checkSolved, self.buttons[1])

        #fill given data in table
        self.fillGrid(self.startGrid)

        # Set sizer and center
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.CenterOnScreen()
        self.Show()

    def OnOpen(self, event):
        ''' select sudoku file'''
        dlg = wx.FileDialog(self, "Open Sudokufile...",
            os.getcwd(), style=wx.OPEN)
            #wildcard = self.wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.ReadFile()
        dlg.Destroy()

    def ReadFile(self):
        '''open sudoku file and select random game'''
        with open(self.filename) as file:
            sudokus = file.readlines()
        #select a random sudoku from file
        self.sudoku = sudokus[randint(1, len(sudokus))]
        self.fillGrid(self.sudoku)
 

    def fillGrid(self, sudoku):
        '''fill Grid on basis input sudoku'''
        self.sudokuGrid.ClearGrid()
        self.sudokuGrid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
        self.sudokuGrid.SetDefaultCellFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
        for input in range(81):
                column = input % 9
                row = abs(input / 9)
                #unlock cells
                self.sudokuGrid.SetReadOnly(row,column, isReadOnly=False)
                #align values 
                self.sudokuGrid.SetDefaultCellAlignment(wx.ALIGN_CENTRE, wx.ALIGN_CENTRE)
                self.sudokuGrid.SetDefaultCellFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.NORMAL))
                #make sudoku 3*3 squares visible by backgroundcolour (RGB value)
                self.SetSquareBackgroundColour(0,0,3,3,230,230,250)
                self.SetSquareBackgroundColour(0,6,3,9,230,230,250)
                self.SetSquareBackgroundColour(3,3,6,6,230,230,250)
                self.SetSquareBackgroundColour(6,0,9,3,230,230,250)
                self.SetSquareBackgroundColour(6,6,9,9,230,230,250)


                # '0' and '.' inputs will be cleared  
                if sudoku[input] in '.0':
                    self.sudokuGrid.SetCellValue(row, column,'')
               #     self.sudokuGrid.SetCellBackgroundColour(row, column, "white") 
               #     self.sudokuGrid.SetCellEditor(row, column, self.Editor)
                else:
                #fill data from input and lock cells    
                    self.sudokuGrid.SetCellValue(row, column,
                    str(sudoku[input]))
                    self.sudokuGrid.SetReadOnly(row,column, isReadOnly=True)
                    self.sudokuGrid.SetCellFont(row,column, wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD))
             
    def SetSquareBackgroundColour(self, x1, y1, x2, y2, R, G, B):
        '''set background colour of a square of given coordinates'''
        for row in range (x1, x2):
            for column in range(y1,y2):
                self.sudokuGrid.SetCellBackgroundColour(row, column, (R,G,B)) 


    def clear(self, evt):
        '''Handle Clear event'''
        " message dialog" 
        dlg = wx.MessageDialog(None, 'are you sure to delete entered values?',
        'MessageDialog', wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            for input in range(81):
                column = input % 9
                row = abs(input / 9)
                # 0 values will be cleared    
                if self.sudoku[input] == '.':
                    self.sudokuGrid.SetCellValue(row, column,"")
        dlg.Destroy

    def checkSolved(self, evt):
        '''Check if the sudoku correctly solved'''
        #convert filled in sudoku to sudokuResult string
        self.sudokuResult = ""
        for i in range(81):
            column = i % 9
            row = abs(i / 9)
            if self.sudokuGrid.GetCellValue(row, column) == '':
                self.sudokuResult += '.'
            else:
                self.sudokuResult += self.sudokuGrid.GetCellValue(row, column) 
        print(self.sudokuResult)

        #calculate correct solution
        print(solved(self.sudoku))

        if self.sudokuResult == solved(self.sudoku):
            self.message("Congratulations Well done!!")
        else:
            self.message("Wrong result, Try again!!")

        




    def message(self, messageText):
        '''message dialog'''
        dlg = wx.MessageDialog(None, messageText,
        'MessageDialog', wx.OK | wx.ICON_HAND)
        result = dlg.ShowModal()
        dlg.Destroy()

 

if  __name__ == "__main__":
    # Run the application
    app = wx.App(False)
    frame = Sudoku()
    app.MainLoop()
