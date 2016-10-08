#!/usr/bin/env python
'''sudoku game based on wxpython
posibilities:
    - read a file
    - select a game
    - files are solved and results are checked

'''

import wx, wx.html, wx.grid
import os
import sys
from random import randint
from sudokusolver import solved
from os.path import expanduser


 

aboutText = """<p>This is a very basic Sudoku game based on Python and wx
running on version %(wxpy)s of <b>wxPython</b> and %(python)s of <b>Python</b>.
See <a href="https://github.com/todool/sudoku-wxpython">sudoku-wxpython on Github</a></p>""" 

class HtmlWindow(wx.html.HtmlWindow):
    def __init__(self, parent, id, size=(600,400)):
        wx.html.HtmlWindow.__init__(self,parent, id, size=size)
        if "gtk2" in wx.PlatformInfo:
            self.SetStandardFonts()

    def OnLinkClicked(self, link):
        wx.LaunchDefaultBrowser(link.GetHref())

class AboutBox(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "About sudoku-wxpython",
            style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|
                wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, -1, size=(400,200))
        vers = {}
        vers["python"] = sys.version.split()[0]
        vers["wxpy"] = wx.VERSION_STRING
        hwin.SetPage(aboutText % vers)
        btn = hwin.FindWindowById(wx.ID_OK)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth()+25, irep.GetHeight()+10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()


helpText = """<p>Help Sudoku function:</b> 
<p>Clear: Clear all entered values after confirmation</b>
<p>Solved?: Check if the game is solved correctly</b>
<p>Help: View this help screen</b>
<p>Load Game: Load a Sudoku Game from file, format??? TODO describe</b>
<p>Game Setup: Setup a new Game</b>
<p>Save Game: Save Current Game</b>
"""



class HelpBox(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self, None, -1, "Help sudoku-wxpython",
            style=wx.DEFAULT_DIALOG_STYLE|wx.THICK_FRAME|wx.RESIZE_BORDER|
                wx.TAB_TRAVERSAL)
        hwin = HtmlWindow(self, -1, size=(400,200))
        hwin.SetPage(helpText)
        irep = hwin.GetInternalRepresentation()
        hwin.SetSize((irep.GetWidth()+25, irep.GetHeight()+10))
        self.SetClientSize(hwin.GetSize())
        self.CentreOnParent(wx.BOTH)
        self.SetFocus()


   

class Sudoku(wx.Frame):
    '''main sudoku class'''
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Sudoku")    
        
        # Setting up the menu.
        toolsmenu= wx.Menu()
        menuOpen = toolsmenu.Append(wx.ID_OPEN, "&Open"," Open")
        menuSave = toolsmenu.Append(wx.ID_SAVE, "&Save"," Save Game")
        menuHelp = toolsmenu.Append(wx.ID_HELP, "&Help"," Help")
        menuAbout = toolsmenu.Append(wx.ID_ABOUT, "&About", "Information about this program")
        menuExit = toolsmenu.Append(wx.ID_EXIT, "E&xit"," Exit")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(toolsmenu,"&Tools") # Adding the "toolsmenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.


        #Create an integer cell editor with range 1-9 
        sizer = wx.BoxSizer(wx.VERTICAL) # Main vertical sizer
        self.SudokuGrid = wx.grid.Grid(self,-1)
        self.Editor = wx.grid.GridCellNumberEditor(1, 9) 

        #default Data
        self.StartGrid = \
        '000000000000000000000000000000000000000000000000000000000000000000000000000000000'

        numRows = numCols = 9
        cellSize = 50
        self.SudokuGrid.CreateGrid(numRows, numCols)      
        self.SudokuGrid.SetRowLabelSize(0);
        self.SudokuGrid.SetColLabelSize(0);
        self.SudokuGrid.SetDefaultColSize(cellSize, resizeExistingCols=True)
        self.SudokuGrid.SetDefaultRowSize(cellSize, resizeExistingRows=True)
        self.SudokuGrid.SetDefaultCellAlignment(wx.ALIGN_CENTRE,
            wx.ALIGN_CENTRE)
        self.SudokuGrid.SetDefaultEditor(self.Editor)

        self.sizer2 = wx.GridSizer(2, 3, 10, 10)
        #self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []
        self.buttons.append(wx.Button(self, -1, "Clear"))
        self.sizer2.Add(self.buttons[0], 1, wx.EXPAND)
        self.buttons.append(wx.Button(self, -1, "Solved?"))
        self.sizer2.Add(self.buttons[1], 1, wx.EXPAND)
        self.buttons.append(wx.Button(self, -1, "Help"))
        self.sizer2.Add(self.buttons[2], 1, wx.EXPAND)
        self.buttons.append(wx.Button(self, -1, "Load Game"))
        self.sizer2.Add(self.buttons[3], 1, wx.EXPAND)
        self.buttons.append(wx.Button(self, -1, "Game Setup"))
        self.sizer2.Add(self.buttons[4], 1, wx.EXPAND)
        self.buttons.append(wx.Button(self, -1, "Save Game"))
        self.sizer2.Add(self.buttons[5], 1, wx.EXPAND)
        
        #add SudokuGrid to vertical sizer
        sizer.Add(self.SudokuGrid, 0, wx.EXPAND) # Add to main sizer
        sizer.Add(self.sizer2, 0, wx.EXPAND) # Add to main sizer


        # Events.
        self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
        self.Bind(wx.EVT_MENU, self.SaveGame, menuSave)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnHelp, menuHelp)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        self.Bind(wx.EVT_BUTTON, self.clear, self.buttons[0])
        self.Bind(wx.EVT_BUTTON, self.checkSolved, self.buttons[1])
        self.Bind(wx.EVT_BUTTON, self.OnHelp, self.buttons[2])
        self.Bind(wx.EVT_BUTTON, self.OnOpen, self.buttons[3])
        self.Bind(wx.EVT_BUTTON, self.gameSetup, self.buttons[4])
        self.Bind(wx.EVT_BUTTON, self.SaveGame, self.buttons[5])

        #draw grid background
        self.set_background()
        #fill game data in table
        self.fill_grid(self.StartGrid)

        # Set sizer and center
        self.SetSizer(sizer)
        sizer.Fit(self)
        self.CenterOnScreen()
        self.Show()

    def set_background(self):
        '''fill grid background color'''
        for row in range (9):
            for column in range (9):
                #unlock cells
                self.SudokuGrid.SetReadOnly(row,column, isReadOnly=False)
                #align values 
                #make sudoku 3*3 squares visible by backgroundcolour (RGB value)
                self.SetSquareBackgroundColour(0,0,3,3,230,230,250)
                self.SetSquareBackgroundColour(0,6,3,9,230,230,250)
                self.SetSquareBackgroundColour(3,3,6,6,230,230,250)
                self.SetSquareBackgroundColour(6,0,9,3,230,230,250)
                self.SetSquareBackgroundColour(6,6,9,9,230,230,250)

    def SetSquareBackgroundColour(self, x1, y1, x2, y2, R, G, B):
        '''set background colour of a square of given coordinates'''
        for row in range (x1, x2):
            for column in range(y1,y2):
                self.SudokuGrid.SetCellBackgroundColour(row, column, (R,G,B)) 

       


    def OnOpen(self, event):
        ''' select sudoku file'''
        #set path to stored games
        userpath = expanduser("~")
        GameFilesPath = os.path.join(userpath,".config/sudoku-wxpython")
        dlg = wx.FileDialog(self, "Open Sudokufile...",
            style=wx.OPEN, defaultDir=GameFilesPath )
            #wildcard = self.wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.ReadFile()
        dlg.Destroy()

    def ReadFile(self):
        #first define if this is a 'new' game or a 'saved' game
        with open(self.filename) as file:
            Firstline = file.readline()
        if Firstline == '[savedsudoku]\n':
            with open(self.filename) as file:
                SavedGameContent = file.readlines()
            self.StartGrid = SavedGameContent[1]
            self.fill_grid(self.StartGrid)
            #SavedGameContent[2] - [1] is delta -> set in file as values
            for input in range(81):
                column = input % 9
                row = abs(input / 9)
                if (SavedGameContent[2][input] <> '.')  and \
                  (self.SudokuGrid.GetCellValue(row, column)==''):
                    self.SudokuGrid.SetCellValue(row, column, SavedGameContent[2][input]) 
        else:
            '''open sudoku file and select random game'''
            with open(self.filename) as file:
                sudokus = file.readlines()
            #select a random sudoku from file
            self.StartGrid = sudokus[randint(1, len(sudokus))]
            self.fill_grid(self.StartGrid)
  
    def SaveGame(self, event):
        ''' Create sudoku file'''
        #set path to stored games
        userpath = expanduser("~")
        GameFilesPath = os.path.join(userpath,".config/sudoku-wxpython")
        dlg = wx.FileDialog(self, "Save Sudoku...",
            defaultDir=GameFilesPath, defaultFile='SavedSudoku.txt',
            style=wx.SAVE)
            #wildcard = self.wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetPath()
            self.WriteFile()
        dlg.Destroy()

    def WriteFile(self):
        '''write current game to file'''
        self.SudokuResult = ""
        for i in range(81):
            column = i % 9
            row = abs(i / 9)
            if self.SudokuGrid.GetCellValue(row, column) == '':
                self.SudokuResult += '.'
            else:
                self.SudokuResult += self.SudokuGrid.GetCellValue(row, column) 

        with open(self.filename,'w') as file:
            #add [savedsudoku] to file to make a difference with new games    
            file.write("[savedsudoku]\n")
            file.write(self.StartGrid)
            file.write(self.SudokuResult)

    def gameSetup(self, event):
        '''setup new game'''
        if self.buttons[4].GetLabel() == 'Game Setup':
            " message dialog" 
            dlg = wx.MessageDialog(None, 'are you sure to setup a new game?',
            'MessageDialog', wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                for row in range (9):
                    for column in range (9):
                        self.SudokuGrid.SetReadOnly(row,column, isReadOnly=False)
                        self.SudokuGrid.SetCellFont(row,column,
                        wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
                self.SudokuGrid.ClearGrid()
                self.buttons[4].SetLabel('Setup Ready?') 
        else:
                'lock entered game values and make bold'
                for row in range (9):
                    for column in range (9):
                       if self.SudokuGrid.GetCellValue(row, column) <> '':
                            self.SudokuGrid.SetReadOnly(row,column, isReadOnly=True)
                            self.SudokuGrid.SetCellFont(row,column,
                            wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD))
                       else:
                            self.SudokuGrid.SetReadOnly(row,column, isReadOnly=False)
                            self.SudokuGrid.SetCellFont(row,column,
                            wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL))
         
                self.buttons[4].SetLabel('Game Setup') 
        

    def fill_grid(self, sudoku):
        '''fill Grid on basis input sudoku'''
        self.SudokuGrid.ClearGrid()
        self.SudokuGrid.SetDefaultCellFont(wx.Font(16, wx.SWISS,
        wx.NORMAL, wx.BOLD))
        for input in range(81):
                column = input % 9
                row = abs(input / 9)
                #unlock cells
                self.SudokuGrid.SetReadOnly(row,column, isReadOnly=False)
                #align values 
                self.SudokuGrid.SetDefaultCellFont(wx.Font(16, wx.SWISS,
                wx.NORMAL, wx.NORMAL))
                # '0' and '.' inputs will be cleared  
                if sudoku[input] in '.0':
                    self.SudokuGrid.SetCellValue(row, column,'')

                #     self.SudokuGrid.SetCellBackgroundColour(row, column, "white") 
                #     self.SudokuGrid.SetCellEditor(row, column, self.Editor)
                    self.SudokuGrid.SetDefaultCellFont(wx.Font(14, wx.SWISS,
                        wx.NORMAL, wx.NORMAL))
                else:
                #fill data from input and lock cells    
                    self.SudokuGrid.SetCellValue(row, column,
                        str(sudoku[input]))
                    self.SudokuGrid.SetReadOnly(row,column, isReadOnly=True)
                    self.SudokuGrid.SetCellFont(row,column, wx.Font(16, wx.SWISS,
                        wx.NORMAL, wx.BOLD))
             

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
                if self.StartGrid[input] == '.':
                    self.SudokuGrid.SetCellValue(row, column,"")
        dlg.Destroy

    def checkSolved(self, evt):
        '''Check if the sudoku correctly solved'''
        #convert filled in sudoku to sudokuResult string
        self.SudokuResult = ""
        for i in range(81):
            column = i % 9
            row = abs(i / 9)
            if self.SudokuGrid.GetCellValue(row, column) == '':
                self.SudokuResult += '.'
            else:
                self.SudokuResult += self.SudokuGrid.GetCellValue(row, column) 

        #calculate correct solution
        if self.SudokuResult == solved(self.StartGrid):
            self.message("Congratulations Well done!!")
        else:
            self.message("Wrong result, Try again!!")

        
    def OnAbout(self, event):
        dlg = AboutBox()
        dlg.ShowModal()
        dlg.Destroy() 
     
    def OnHelp(self, event):
        dlg = HelpBox()
        dlg.ShowModal()
        dlg.Destroy() 

    def message(self, messageText):
        '''message dialog'''
        dlg = wx.MessageDialog(None, messageText,
        'MessageDialog', wx.OK | wx.ICON_HAND)
        result = dlg.ShowModal()
        dlg.Destroy()

    def OnExit(self, event):
        self.SaveGame(event)
        self.Destroy()
 

if  __name__ == "__main__":
    # Run the application
    app = wx.App(False)
    frame = Sudoku()
    app.MainLoop()
