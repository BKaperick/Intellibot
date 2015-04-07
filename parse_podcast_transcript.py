

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

def getQuestionAnswer(text):
    for line in text:
        content = line.rstrip()
        if not line in getSpeakers(text):
            if len(line) > 0:
                if line[-1] == '?':
                    print(line)
            else:
                pass#print('<\line>',line.rstrip().rstrip(),'<line>')

text = getText('TAL')
getQuestionAnswer(text)
