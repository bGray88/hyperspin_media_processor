'''
Created on November 12, 2016

@author: bgray
'''

import sys
from cx_Freeze import setup,Executable

base = None
if sys.platform == 'win32':
	base = 'Win32GUI'
	
exe = Executable(
        script  = 'Main.py',
        icon    = 'icns\\hyperspin.ico',
		base = base
        )
includefiles    = ['docs\\',
                   'fnts\\',
                   'icns',
                   'imgs\\',
				   'snd\\',
                   'prgms\\',
				   'App.py',
				   'Container.py',
				   'Database.py',
				   'FileProcessor.py',
				   'FrontEnd.py',
				   'LogFile.py',
                   'StatusBar.py',
				   'Window.py']
excludes = []
packages = ['os', 'site', 're', 'requests', 'sys', 'win32com', 'shutil', 'PIL', 'datetime', 'threading',
		'ctypes', 'subprocess']

setup(
    name        = 'HyperSpin Media Processor',
    version     = '0.1',
    description = 'null',
    options     = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}},
    executables = [exe]
)
