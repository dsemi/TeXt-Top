#!/usr/bin/python2
import os

current_dir = os.path.dirname(__file__)
if current_dir:
    os.chdir(current_dir)

os.system('python "C:\\Users\\Owner\\Documents\\School Stuff\\CSC 470\\pyinstaller-1.5.1\\pyinstaller-1.5.1\\MakeSpec.py" --onefile --tk --icon="pics\\TeXt-Top.ico" Client.py')
with open('Client.spec') as f:
    file_contents = f.read().split('\n')
file_contents.insert(4, "a.datas += [('pics/TeXt-Top.ico','pics\\TeXt-Top.ico','DATA'),('pics/TeXtTopLogo2.png','pics\\TeXtTopLogo2.png','DATA'),('pics/TeXtTopLogo2Smaller.png','pics\\TeXtTopLogo2Smaller.png','DATA')]")
with open('Client.spec', 'w') as f:
    f.write('\n'.join(file_contents))
os.system('python "C:\\Users\\Owner\\Documents\\School Stuff\\CSC 470\\pyinstaller-1.5.1\\pyinstaller-1.5.1\\Build.py" Client.spec')
