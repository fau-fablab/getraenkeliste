#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Skript für eine Getränkeliste
"""

# import-Anweisungen
import os
import codecs
import sys
import signal  # Fenstergroessenaenderung behandeln

__author__ = 'Christopher Sauer, 2015'
__license__ = 'CC BY-SA 3.0'

if sys.version_info < (3, 4):
    safe_input = raw_input
elif sys.version_info >= (3, 4):
    safe_input = input

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


class Colors(object):
    """
    chosen ANSI colors
    """
    RESET = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    # normal colors have code \033[3x bold colors have code \033[9x
    # and back colors have \033[4x or \033[10x
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'


def more_decimals_than(number, allowed_decimals_cnt):
    """
    returns true if the count of decimals (numbers after the dot) is more than decimals
    """
    # e.g. 5.67 - 5 = 0.67 -> '67' (round: because float is bitter)
    decimals = str(round(number-int(number), allowed_decimals_cnt+1))[2:]
    cnt = 0 if decimals == '0' else len(decimals)
    return False if cnt < 0 else cnt > allowed_decimals_cnt


def float_input(promt, default, decimals=0):
    """
    Fetches an float value from stdin.
    If no input was made, default will be returned
    """
    input_text = ""
    while True:
        try:
            input_text = str(safe_input("{promt} [{default}] ".
                                        format(promt=promt, default=default)))
            if len(input_text) == 0:
                return default
            elif more_decimals_than(float(input_text), decimals):
                print(more_decimals_than(float(input_text), decimals))
                print(colorize(Colors.RED,
                               "You must enter a number with at most %d decimals" % decimals))
                continue
            else:
                return float(input_text)
        except ValueError:
            print(colorize(Colors.RED, "You must enter a number. Try again."))
            continue


def getsep(*egal):
    """
    Terminalausgabe
    """
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
            einzahlung = float_input(colorize(Colors.GREEN, "Einzahlung:"), 0.0, 2)
            # Magie
            for j in range(4):
                # Einzahlung
                if j == 0:
                    begin = lineTester.index(":={") + len(":={")
                    outFile.write(lineTester[0:begin])
                    lineTester = lineTester[begin:-1]
                    end = lineTester.index("-")
                    # print lineTester[:end]
                    neuEingezahlt = float(lineTester[:end - 1]) + einzahlung
                    outFile.write(str(neuEingezahlt))
                    outFile.write(lineTester[len(str(neuEingezahlt)):end])
                    # print neuEingezahlt
                # neue Getraenke
                else:
                    # abfragen für 50ct, 70ct und 80ct
                    if j == 1:
                        anzahl = int(float_input(colorize(Colors.BLUE, "#50ct:"), 0))
                    elif j == 2:
                        anzahl = int(float_input(colorize(Colors.CYAN, "#70ct:"), 0))
                    elif j == 3:
                        anzahl = int(float_input(colorize(Colors.MAGENTA, "#80ct:"), 0))
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
