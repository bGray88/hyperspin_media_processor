'''
Created on November 12, 2016

@author: bgray
'''

import tkinter as tk    #Python 3
#import Tkinter as tk    #Python 2

import App
import os
import FileProcessor
import threading
import PIL

from tkinter.constants import DISABLED, NORMAL

# DO NOT DELETE
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from PIL import Image
from PIL import ImageTk
from PIL import PngImagePlugin

class FrontEnd(App.App):
    
    def __init__(self):
        super().__init__()
        
        self.fileProcessor = FileProcessor.FileProcessor()
        self.savedFilePaths = self.fileProcessor.getDataSavedPaths()
        if self.savedFilePaths is not -1 and len(self.savedFilePaths) > 0:
            self.mediaDirSelected = self.savedFilePaths[0].rstrip('\r\n')
            self.titleDirSelected = self.savedFilePaths[1].rstrip('\r\n')
            self.themeDirSelected = self.savedFilePaths[2].rstrip('\r\n')
            self.saveDirSelected = self.savedFilePaths[3].rstrip('\r\n')
        else:
            self.mediaDirSelected = 'Media Path'
            self.titleDirSelected = 'Titles Path'
            self.themeDirSelected = 'Themes Path'
            self.saveDirSelected = 'Save Path'
            
        self.checkMediaSet = tk.IntVar()
        self.checkTitleSet = tk.IntVar()
        self.checkThemeSet = tk.IntVar()
        self.checkPlaylistSet = tk.IntVar()
        self.checkDatabaseSet = tk.IntVar()
        
        self.startTimeSelected = '-1'
        self.durationTimeSelected = '-1'
        
        self.returnMsg = None
        
        self.container.setFrameIcon('hyperspin.ico')
        self.introWindow()
        self.setEntryText(self.entryMedia, self.mediaDirSelected)
        self.setEntryText(self.entryTitle, self.titleDirSelected)
        self.setEntryText(self.entryTheme, self.themeDirSelected)
        self.setEntryText(self.entrySave, self.saveDirSelected)
        self.btnWindow()
        self.statusBarWindow()
        
    def checkProcessThread(self):
        if self.processThread.is_alive():
            self.container.after(1, self.checkProcessThread)
        else:
            self.completeProcess()
            self.progressBar.stop()
        
    def runFileProcess(self):
        self.returnMsg = self.fileProcessor.processFiles()
        
    def startProcess(self):
        if self.saveDirSelected != 'Save Path' and self.saveDirSelected != '':
            startProcessClear = False
            if self.checkMediaSet.get() or self.checkTitleSet.get() or self.checkThemeSet.get() or self.checkPlaylistSet.get() or self.checkDatabaseSet.get():
                if self.checkMediaSet.get() and (self.mediaDirSelected != 'Media Path' and self.mediaDirSelected != ''):
                    startProcessClear = True
                if self.checkTitleSet.get() and (self.titleDirSelected != 'Titles Path' and self.titleDirSelected != '' and
												self.mediaDirSelected != 'Media Path' and self.mediaDirSelected != ''):
                    startProcessClear = True
                if self.checkThemeSet.get() and (self.themeDirSelected != 'Themes Path' and self.themeDirSelected != '' and
												self.mediaDirSelected != 'Media Path' and self.mediaDirSelected != ''):
                    startProcessClear = True
                if self.checkPlaylistSet.get() and (self.mediaDirSelected != 'Media Path' and self.mediaDirSelected != ''):
                    startProcessClear = True
                if self.checkDatabaseSet.get() and (self.mediaDirSelected != 'Media Path' and self.mediaDirSelected != ''):
                    startProcessClear = True
                if startProcessClear:
                    self.prepareProcess()
                    self.processWindow()
                    self.progressBar.start()
                    self.fileProcessor.setTaskProcess(self.checkMediaSet.get(),
                                                      self.checkTitleSet.get(),
                                                      self.checkThemeSet.get(),
													  self.checkPlaylistSet.get(),
                                                      self.checkDatabaseSet.get(),
                                                      self.startTimeSelected,
                                                      self.durationTimeSelected)
                    self.fileProcessor.setFilePaths(self.mediaDirSelected, 
                                                    self.titleDirSelected, 
                                                    self.themeDirSelected, 
                                                    self.saveDirSelected) 
                    self.processThread = threading.Thread(target=self.runFileProcess)
                    self.processThread.daemon = True
                    self.processThread.start()
                    self.container.after(1, self.checkProcessThread)
                else:
                    tk.messagebox.showwarning('Open file', 
                                              'Please select a valid task and directory')
            else:
                tk.messagebox.showwarning('Open file', 
                                          'Please select a task to process before starting')
        else:
            tk.messagebox.showwarning('Open file', 
                                      'Please select a valid save directory')
        
    def prepareProcess(self):
        self.checkMedia.config(state=DISABLED)
        self.checkTitle.config(state=DISABLED)
        self.checkTheme.config(state=DISABLED)
        self.checkPlaylist.config(state=DISABLED)
        self.checkDatabase.config(state=DISABLED)
        self.browseMediaButton.config(state=DISABLED)
        self.browseTitleButton.config(state=DISABLED)
        self.browseThemeButton.config(state=DISABLED)
        self.browseSaveButton.config(state=DISABLED)
        self.processButton.config(state=DISABLED)
        self.exitButton.config(state=DISABLED)
                
    def completeProcess(self):
        self.exitButton.config(state=NORMAL)
        unsuccessfulMsg = ('The process has finished unsuccessfully\n')
        successfulMsg = ('The process has finished successfully\n')
        suffixUnMsg = ('Please check your setup and attempt the process again\n')
        suffixMsg = ('Enjoy all of the newly created media\n')
        
        if self.returnMsg is 'EMPTY':
            completeMsg = (unsuccessfulMsg + 'NO_MESSAGE\n' + suffixUnMsg)
        elif self.returnMsg is 'EMPTY':
            completeMsg = (unsuccessfulMsg + 'NO_MESSAGE\n' + suffixUnMsg)
        else:
            completeMsg = (successfulMsg + suffixMsg)
            
        self.procMessage.config(text=completeMsg)
        
    def setMediaDir(self):
        rootDir = self.getRootDir()
        self.container.withdraw()
        self.mediaDirSelected = self.browseForFolder('Select the Media Directory', True, 
                                                    os.path.normpath(rootDir))
        self.setEntryText(self.entryMedia, self.mediaDirSelected)
        self.container.deiconify()
    
    def setTitleDir(self):
        rootDir = self.getRootDir()
        self.container.withdraw()
        self.titleDirSelected = self.browseForFolder('Select the Titles Directory', True, 
                                                    os.path.normpath(rootDir))
        self.setEntryText(self.entryTitle, self.titleDirSelected)
        self.container.deiconify()
        
    def setThemeDir(self):
        rootDir = self.getRootDir()
        self.container.withdraw()
        self.themeDirSelected = self.browseForFolder('Select the Theme Directory', True, 
                                                    os.path.normpath(rootDir))
        self.setEntryText(self.entryTheme, self.themeDirSelected)
        self.container.deiconify()
        
    def setSaveDir(self):
        rootDir = self.getRootDir()
        self.container.withdraw()
        self.saveDirSelected = self.browseForFolder('Select the File Save Directory', True, 
                                                    os.path.normpath(rootDir))
        self.setEntryText(self.entrySave, self.saveDirSelected)
        self.container.deiconify()
        
    def setEntryText(self, entryObject, msgContents):
        entryObject.config(state=NORMAL)
        entryObject.delete(0, tk.END)
        entryObject.insert(0, msgContents)
        entryObject.config(state=DISABLED)
        
    def createTopLevel(self):
        self.container.withdraw()
        self.top = tk.Toplevel()
        self.top.config(background='GRAY')
        self.top.protocol('WM_DELETE_WINDOW', self.removeTopLevel)
        self.top.lift()
        self.top.attributes('-topmost', True)
        
    def removeTopLevel(self):
        self.setMediaTime()
        self.top.destroy()
        self.container.deiconify()
        
    def selectMediaTime(self):
        if self.checkMediaSet.get():
            self.labelFont = ('sans', 12, 'bold')
            self.createTopLevel()
            selectButton = tk.Button(self.top, text="Finish", command=self.setMediaTime, 
                                     background='GRAY')
            
            self.top.title('Input Time for Conversion')
            self.startTimeLabel = tk.Label(self.top, width=0, height=0, padx=12, pady=12,
                                       background='GRAY', foreground='WHITE', font=self.labelFont,
                                       text='\nInput Start Time In Seconds\n')
            self.startTime = tk.StringVar()
            entryStartBox = tk.Entry(self.top, textvariable=self.startTime, background='WHITE')
            self.endTimeLabel = tk.Label(self.top, width=0, height=0, padx=12, pady=12,
                                       background='GRAY', foreground='WHITE', font=self.labelFont,
                                       text='\nInput Duration In Seconds\n')
            self.durationTime = tk.StringVar()
            entryDurBox = tk.Entry(self.top, textvariable=self.durationTime, background='WHITE')
            
            self.startTimeLabel.pack()
            entryStartBox.pack(anchor='center')
            self.endTimeLabel.pack()
            entryDurBox.pack(anchor='center')
            selectButton.pack(anchor='n', fill='both')
        
        
    def setMediaTime(self):
        if self.startTime.get() == '' or self.startTime.get() == '-1':
            self.startTimeSelected = '300'
        else:
            self.startTimeSelected = self.startTime.get()
        if self.durationTime.get() == '' or self.startTime.get() == '-1':
            self.durationTimeSelected = '30'
        else:
            self.durationTimeSelected = self.durationTime.get()
        self.top.destroy()
        self.container.deiconify()
        
    def browseForFolder(self, title, mustexist, initialdir):
        return tk.filedialog.askdirectory(title=title, 
                                          mustexist=mustexist, 
                                          initialdir=initialdir)
        
    def getFolderSelected(self):
        return self.fileDirSelected
    
    def getRootDir(self):
        rootDir = os.path.expanduser("~")
        rootIdx = rootDir.find(os.path.normpath('/'))
        while rootDir.find(os.path.normpath('/'), (rootIdx + 1)) is not -1:
            rootDir = os.path.dirname(rootDir)
        return (os.path.dirname(rootDir))
        
    def configWindows(self, window, *args):
        for coords in args:
            for rx, rw, cx, cw in coords:    
                window.gridConfig(rx, rw, cx, cw)
                
    def introWindow(self):
        self.labelFont = ('bodoni', 14, 'bold')
        self.introMessage = tk.Label(self.msgWindow, width=0, height=0, 
                                   background='GOLDENROD', foreground='BLACK', font=self.labelFont,
                                   text='\nWelcome to the HyperSpin Media Processor\n')
        self.fileLogo = PIL.ImageTk.PhotoImage(PIL.Image.open('imgs/floppy.png'))
        self.logoPanel = tk.Label(self.msgWindow, background='GOLDENROD', image=self.fileLogo)
        self.checkMedia = tk.Checkbutton(self.msgWindow, bg='GOLDENROD', activebackground='GOLDENROD',
                                         variable=self.checkMediaSet, command=self.selectMediaTime)
        self.entryMedia = tk.Entry(self.msgWindow)
        self.entryMedia.config(state=DISABLED)
        self.checkTitle = tk.Checkbutton(self.msgWindow, bg='GOLDENROD', activebackground='GOLDENROD',
                                         variable=self.checkTitleSet)
        self.entryTitle = tk.Entry(self.msgWindow)
        self.entryTitle.config(state=DISABLED)
        self.checkTheme = tk.Checkbutton(self.msgWindow, bg='GOLDENROD', activebackground='GOLDENROD',
                                         variable=self.checkThemeSet)
        self.entryTheme = tk.Entry(self.msgWindow)
        self.entryTheme.config(state=DISABLED)
        self.entrySave = tk.Entry(self.msgWindow)
        self.entrySave.config(state=DISABLED)
        BROWSE_MEDIA_CMD = self.setMediaDir
        self.browseMediaButton = self.msgWindow.createButton('...', 'BLACK', 
                                                   'WHITE', BROWSE_MEDIA_CMD, '1', '4')
        BROWSE_TITLE_CMD = self.setTitleDir
        self.browseTitleButton = self.msgWindow.createButton('...', 'BLACK', 
                                                   'WHITE', BROWSE_TITLE_CMD, '1', '4')
        BROWSE_THEME_CMD = self.setThemeDir
        self.browseThemeButton = self.msgWindow.createButton('...', 'BLACK', 
                                                   'WHITE', BROWSE_THEME_CMD, '1', '4')
        BROWSE_SAVE_CMD = self.setSaveDir
        self.browseSaveButton = self.msgWindow.createButton('...', 'BLACK', 
                                                   'WHITE', BROWSE_SAVE_CMD, '1', '4')
        self.msgGridConfig = [[0,1,None,None], [1,1,None,None], 
                              [2,1,None,None], [3,1,None,None],
                              [4,1,0,1]]
        self.configWindows(self.msgWindow, self.msgGridConfig)
        self.msgWindow.addWindow(self.introMessage, 1, 1, 'nsew')
        self.msgWindow.addWindow(self.logoPanel, 1, 2, 'nsew')
        self.msgWindow.addWindow(self.checkMedia, 2, 0, '')
        self.msgWindow.addWindow(self.entryMedia, 2, 1, 'ew')
        self.msgWindow.addWindow(self.checkTitle, 3, 0, '')
        self.msgWindow.addWindow(self.entryTitle, 3, 1, 'ew')
        self.msgWindow.addWindow(self.checkTheme, 4, 0, '')
        self.msgWindow.addWindow(self.entryTheme, 4, 1, 'ew')
        self.msgWindow.addWindow(self.entrySave, 5, 1, 'ew')
        self.msgWindow.placeButton(self.browseMediaButton, 2, 2, '')
        self.msgWindow.placeButton(self.browseTitleButton, 3, 2, '')
        self.msgWindow.placeButton(self.browseThemeButton, 4, 2, '')
        self.msgWindow.placeButton(self.browseSaveButton, 5, 2, '')
        self.bgdWindow.addWindow(self.msgWindow, 0, 0, 'nsew', 2)
        
    def processWindow(self):
        self.labelFont = ('sans', 12, 'bold')
        self.procMessage = tk.Label(self.procWindow, width=0, height=0, 
                                   background='RED', foreground='WHITE', font=self.labelFont,
                                   text='\nThe program will now copy media based\n'
                                   'on the paths selected\n')
        self.progressBar = tk.ttk.Progressbar(self.procWindow, orient="horizontal",
                                        length=(int(self.windowedWidth / 2)), 
                                        mode="indeterminate")
        self.procGridConfig = [[0,1,None,None], [1,1,None,None], 
                              [2,1,None,None], [3,1,None,None],
                              [4,1,0,1]]
        self.configWindows(self.procWindow, self.procGridConfig)
        self.procWindow.addWindow(self.procMessage, 1, 0, 'nsew')
        self.procWindow.addWindow(self.progressBar, 3, 0)
        self.bgdWindow.addWindow(self.procWindow, 0, 0, 'nsew', 2)
        
    def btnWindow(self):
        self.checkPlaylist = tk.Checkbutton(self.btmWindow, bg='BLACK', activebackground='BLACK',
                                         fg='WHITE', activeforeground='WHITE',
                                         selectcolor='BLACK',
                                         text="Create Playlists",
                                         variable=self.checkPlaylistSet)
        self.checkDatabase = tk.Checkbutton(self.btmWindow, bg='BLACK', activebackground='BLACK',
                                         fg='WHITE', activeforeground='WHITE',
                                         selectcolor='BLACK',
                                         text="Create Databases",
                                         variable=self.checkDatabaseSet)
        PROCESS_COMMAND = self.startProcess
        self.processButton = self.btmWindow.createButton('Process', 'GRAY', 
                                                 'WHITE', PROCESS_COMMAND, '2', '15')
        EXIT_COMMAND = self.endApp
        self.exitButton = self.btmWindow.createButton('Exit', 'GRAY', 
                                                 'WHITE', EXIT_COMMAND, '2', '15')
        self.btmGridConfig = [[0,1,0,1], [1,1,1,1], [2,1,2,1], [3,1,3,1]]
        self.configWindows(self.btmWindow, self.btmGridConfig)
        self.btmWindow.addWindow(self.checkPlaylist, 1, 1, 'w')
        self.btmWindow.addWindow(self.checkDatabase, 2, 1, 'w')
        self.btmWindow.placeButton(self.processButton, 1, 2, 'nsew')
        self.btmWindow.placeButton(self.exitButton, 2, 2, 'nsew')
        self.container.addWindow(self.btmWindow, 1, 0, 'nsew', 2)
        
    def statusBarWindow(self):
        self.statusBar.setTitle('HyperSpin Media Processor')
        self.statusBar.setScreen('Menu')
        self.statusBar.padConfig(1, 1)
        self.statGridConfig = [[None,None,0,5], [None,None,1,5], 
                              [None,None,2,5], [None,None,3,5],
                              [0,1,4,3]]
        self.configWindows(self.statusBar, self.statGridConfig)
        self.container.addWindow(self.statusBar, 2, 0, 'nsew', 2)
        