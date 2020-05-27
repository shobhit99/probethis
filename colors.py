import sys
import os
import platform

colors = True  # Output should be colored
machine = sys.platform  # Detecting the os of current system
checkplatform = platform.platform() 
if machine.lower().startswith(('os', 'win', 'darwin', 'ios')):
    colors = False  # Colors shouldn't be displayed in mac & windows
if checkplatform.startswith("Windows-10") and int(platform.version().split(".")[2]) >= 10586:
    colors = True
    os.system('')
if not colors:
    end = green = yellow = red = white = cyan = bgreen = ''
else:
    lgreen = '\033[32m'
    lcyan = '\033[96m'
    lyellow = '\033[33m'
    lred = '\033[31m'
    white = '\033[97m'
    blue = '\033[94m'
    green = '\033[92m'
    red = '\033[91m'
    yellow = '\033[93m'
    cyan = '\033[36m'
    end = '\033[0m'

statuscolors = {1: cyan, 2: green, 3: lgreen, 4: yellow, 5: lred}
