import pickle
from base_functions import *

def getText(filename):
    with open(filename+'.txt') as file:
        lines = [line.strip() for line in file.readlines() if len(line.strip()) > 0]
    return lines

def getSpeakers(text):
    Speakers = list(set([line.rstrip() for line in text if (line.count(' ') < 2)
                         and (not '[' in line)
                         and (not '.' in line)
                         and (not '?' in line)
                         ]))
    Speakers.remove('Yup')
    return Speakers[1:]

Speakers = getSpeakers(getText('TAL'))

def formatString(line):
    badChars = (',','.','?','-',"'",'"')
    line = line.lower().replace("  "," ")
    for char in badChars:
        line = line.replace(char,"")
    return line

def getQuestionAnswer(text):
    QuestionAnswer = {}
    for line in range(0, len(text)):
        content = line
        if not text[line] in getSpeakers(text):
            if text[line][-1] == '?':
                QuestionAnswer[clean(text[line])] = clean(text[line+2])
            else:
                pass#print('<\line>',line.rstrip().rstrip(),'<line>')
    return QuestionAnswer

text = getText('TAL')
Answer = getQuestionAnswer(text)

pickle.dump(Answer, open("podcast_language.p", "wb") )
