def clean(line):
    badChars = (',','.','?','-',"'",'"',"!")
    line = line.lower().replace("  "," ")
    for char in badChars:
        line = line.replace(char,"")
    return line
    
