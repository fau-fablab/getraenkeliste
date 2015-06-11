# by Christopher Sauer, 2015
# -*- coding: utf-8 -*-
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
print "Bearbeitung"
for i in range(len(lines)):
    if ":={" in lines[i]:
        if not "sum" in lines[i]:
            lineTester = lines[i]
            print lineTester[2:lineTester.index("&")]
            einzahlung = raw_input("Einzahlung: ")
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
                    #print lineTester[:end]
                    neuEingezahlt = int(float(lineTester[:end-1])) + int(einzahlung)
                    outFile.write(str(neuEingezahlt))
                    outFile.write(lineTester[len(str(neuEingezahlt)):end])
                    #print neuEingezahlt
                # neue Getränke
                else:
                    # abfragen für 50ct, 70ct und 80ct
                    if j == 1:
                        anzahl = raw_input("#50ct: ")
                    elif j == 2:
                        anzahl = raw_input("#70ct: ")
                    elif j == 3:
                        anzahl = raw_input("#80ct: ")
                    if len(anzahl) == 0:
                        anzahl = 0
                    begin = lineTester.index(":={") + len(":={")
                    outFile.write(lineTester[end:begin])
                    lineTester = lineTester[begin:]
                    end = lineTester.index("}")
                    #print lineTester[:end]
                    neuAnzahl = int(lineTester[:end]) + int(anzahl)
                    outFile.write(str(neuAnzahl))
                    outFile.write(lineTester[len(str(neuAnzahl)):end])
                    if j == 3:
                        #print lineTester[len(str(neuAnzahl)):]
                        outFile.write(lineTester[len(str(neuAnzahl)):] + "\n")
        # trotzdem reinschreiebn
        else:
            outFile.write(lines[i])
    else:
        outFile.write(lines[i])

# Datei speichern
outFile.close()

# Kompilierem mit latexmk
os.system("latexmk -pdf " + outname + " && latexmk -c")
os.system("echo ======================================================")
os.system("echo DIFF")
os.system("echo ======================================================")
os.system("diff -u " + filename + " " + outname)
# nur für OS X 
#os.system("open " + outname[0:-4] + ".pdf")
