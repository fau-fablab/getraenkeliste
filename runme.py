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
import unicodedata

# Input
filename = str("getraenkeliste.tex")
lines = codecs.open(filename, 'r', encoding='utf-8').readlines()
# Output
outname = "auto_getraenkeliste.tex"
outFile = codecs.open(outname, 'w+', encoding='utf-8')

# Terminalausgabe
print("Bearbeitung")
for line in lines:
    if ":={" in line:
        if "sum" not in line:
            lineTester = line
            print(lineTester[2:lineTester.index("&")])
            einzahlung = input("Einzahlung: ")
            if len(einzahlung) == 0:
                einzahlung = 0
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
                        anzahl = input("#50ct: ")
                    elif j == 2:
                        anzahl = input("#70ct: ")
                    elif j == 3:
                        anzahl = input("#80ct: ")
                    if len(anzahl) == 0:
                        anzahl = 0
                    begin = lineTester.index(":={") + len(":={")
                    outFile.write(lineTester[end:begin])
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

# Kompilierem mit latexmk
os.system("latexmk -pdf {file} --quiet && latexmk -c --quiet".format(file=outname))
print("======================================================")
print("DIFF")
print("======================================================")
os.system("diff -u {file1} {file2}".format(file1=filename, file2=outname))
# nur für OS X
# os.system("open " + outname[0:-4] + ".pdf")
