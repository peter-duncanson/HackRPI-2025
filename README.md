# Morse Code Terminal

# Team:
**Front End, API Integration, Middleware Logic** Peter Duncanson

**Harware and Middleware Logic** Muhammad Choudry

**Middleware Logic** Ziyad Hamed

# Project Description:
We have created a morse code typing aid, combining retro tech with modern software to allow users of all ability to type with ease. We've utilized Gemini API to interpret shortened text inputted from physical buttons on an arduino.

## Install Guide

**Prerequisites**

Ensure that **Git** is installed on your machine. For help, refer to the following documentation: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

```

## Launch Codes

**Prerequisites**

Ensure that **Git** and **Python** are installed. For help, refer to the following documentation:
   1. Installing Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
   2. Installing Python: https://www.python.org/downloads/
   3. Installing Ubuntu onto your droplet: https://www.digitalocean.com/community/tutorials/how-to-set-up-an-ubuntu-server-on-a-digitalocean-droplet

### How to run


1. Create Python virtual environment:

```
python3 -m PATH/TO/venv_name
```

2. Activate virtual environment

   - Linux: `. PATH/TO/venv_name/bin/activate`
   - Windows (PowerShell): `. .\PATH\TO\venv_name\Scripts\activate`
   - Windows (Command Prompt): `>PATH\TO\venv_name\Scripts\activate`
   - macOS: `source PATH/TO/venv_name/bin/activate`

   *Notes*

   - If successful, command line will display name of virtual environment: `(venv_name) `

   - Type `deactivate` in the terminal to close a virtual environment

3. Navigate to project app directory

```
cd PATH/TO/HackRPI-2025/
```

4. Run either gui.py, or arduino_py.py

```
 python3 __init__.py
```
5.

Interface with the keyboard if in gui.py, or the arduino if in arduino_py.py.

Unfortunately, we were unable to combine the gui and arduino hardware functionalities due to multiple loops, while this can be resolved using multithreading, we did not have enough time to resolve the issue.
Nonetheless, we hope you enjoy our segmented entries for RPIHACK25
```
* Running on http://127.0.0.1:5000
```
