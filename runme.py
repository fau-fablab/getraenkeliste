#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Skript für die FabLab Getränkeliste
"""

__author__ = 'Christopher Sauer, 2015'
__license__ = 'CC BY-SA 3.0'

# import-Anweisungen
import os
import codecs
import unicodedata  # TODO: unused?
import sys
import signal #  Fenstergroessenaenderung behandeln

if sys.version_info < (3, 4):
    input = raw_input

# Input
filename = str("getraenkeliste.tex")
lines = codecs.open(filename, 'r', encoding='utf-8').readlines()
# Output
outname = "auto_getraenkeliste.tex"
outFile = codecs.open(outname, 'w+', encoding='utf-8')

def colorize(color, message):
    """
    Adds ANSI colors to the message
    :type color: str
    :type message: str
    :param color: Colors to add to the message
    :param message: Message which should be displayed colored
    :return: the colored message
    """
    return "%s%s%s" % (color, message, Colors.RESET)


class Colors:
    """
    chosen ANSI colors
    """
    RESET = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    # normal colors have code \033[3x bold colors have code \033[9x and back colors have \033[4x or \033[10x
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

def int_input(promt, default):
    """
    Fetches an int value from stdin.
    If no input was made, default will be returned
    """
    input_text = ""
    while True:
        try:
            input_text = str(input("{promt} [{default}] ".format(promt=promt, default=default)))
            if len(input_text) == 0:
                return default
            else:
                return int(input_text)
        except ValueError:
            print(colorize(Colors.RED, "You must enter a number. Try again."))
            continue

# Terminalausgabe

def getsep(*egal):
    global WIDTH, HEIGHT, SEPERATOR
    HEIGHT, WIDTH = os.popen('stty size', 'r').read().split()
    SEPERATOR = "=" * int(WIDTH)

signal.signal(signal.SIGWINCH, getsep)

getsep()

print(SEPERATOR)
print(colorize(Colors.BOLD + Colors.WHITE, "Bearbeitung"))
print(SEPERATOR)
for line in lines:
    if ":={" in line:
        if "sum" not in line:
            lineTester = line
            print(colorize(Colors.UNDERLINE, lineTester[2:lineTester.index("&")].strip()))  # Name
            einzahlung = int_input(colorize(Colors.GREEN, "Einzahlung:"), 0)
            # Magie
            for j in range(4):
                # Einzahlung
                if j == 0:
                    begin = lineTester.index(":={") + len(":={")
                    outFile.write(lineTester[0:begin])
                    lineTester = lineTester[begin:-1]
                    end = lineTester.index("-")
                    # print lineTester[:end]
                    neuEingezahlt = int(float(lineTester[:end - 1])) + int(einzahlung)
                    outFile.write(str(neuEingezahlt))
                    outFile.write(lineTester[len(str(neuEingezahlt)):end])
                    # print neuEingezahlt
                # neue Getraenke
                else:
                    # abfragen für 50ct, 70ct und 80ct
                    if j == 1:
                        anzahl = int_input(colorize(Colors.BLUE, "#50ct:"), 0)
                    elif j == 2:
                        anzahl = int_input(colorize(Colors.CYAN, "#70ct:"), 0)
                    elif j == 3:
                        anzahl = int_input(colorize(Colors.MAGENTA, "#80ct:"), 0)
                    begin = lineTester.index(":={") + len(":={")
                    outFile.write(lineTester[end:begin])  # TODO: end can be undefined
                    lineTester = lineTester[begin:]
                    end = lineTester.index("}")
                    # print lineTester[:end]
                    neuAnzahl = int(lineTester[:end]) + int(anzahl)
                    outFile.write(str(neuAnzahl))
                    outFile.write(lineTester[len(str(neuAnzahl)):end])
                    if j == 3:
                        # print lineTester[len(str(neuAnzahl)):]
                        outFile.write(lineTester[len(str(neuAnzahl)):] + "\n")
        # trotzdem reinschreiebn
        else:
            outFile.write(line)
    else:
        outFile.write(line)

# Datei speichern
outFile.close()

print(SEPERATOR)
print(colorize(Colors.BOLD, "Work, work..."))
print(SEPERATOR)
# Kompilierem mit latexmk
os.system("latexmk -pdf {file} --quiet && latexmk -c --quiet".format(file=outname))
print(SEPERATOR)
print(colorize(Colors.BOLD, "DIFF"))
print(SEPERATOR)
os.system("diff -u {file1} {file2}".format(file1=filename, file2=outname))
# nur für OS X
# os.system("open " + outname[0:-4] + ".pdf")
