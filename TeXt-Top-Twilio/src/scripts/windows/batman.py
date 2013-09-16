import os
import ctypes
from win32com.shell import shell, shellcon
import pythoncom

def batman():
    print " ._M_.\n(     )\n `'V`'"

    iad = pythoncom.CoCreateInstance(shell.CLSID_ActiveDesktop, None,
          pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IActiveDesktop)
    iad.SetWallpaper(os.path.abspath(os.path.join(os.path.dirname(__file__),'asciibatman.bmp')), 0)
    iad.ApplyChanges(shellcon.AD_APPLY_ALL)

if __name__ == '__main__':
    batman()
