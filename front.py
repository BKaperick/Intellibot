import math
import pickle
from base_functions import *

INTERESTING_LETTERS = ['b','g','j','k','l','m','p','q','u','v','w','x','z']
SIMILARITY_THRESHHOLD = 1.333
vocabulary = {"do you play any games": "i enjoy basketball",
              "who is sam": "sam is my favorite teacher",
              "hello": "hi how are you",
              "what is a good movie": "the big lebowski is good",
              "do you have a name": "my name is bryan"}


def addPodcastVocabulary(vocabulary):
    vocab = pickle.load(open("podcast_language.p", "rb"))
    vocabulary.update(vocab)
    return vocabulary

def prepareInput(inString):
    inString = clean(inString)
    words = inString.split(" ");
    return words

def scoreOne(word):
    score = len(word)
    for letter in word:
        if letter in INTERESTING_LETTERS:
            score += 1
    return score

def score(words):
    words_and_scores = []
    for word in words:
        score = scoreOne(word)
        words_and_scores.append((word, score));
    return dict(words_and_scores)

def retrieve_similar_statements(words):
    #print("retrieve similar statements")
    candidate_similar_statements = []
    for word in words:
        for key in vocabulary.keys():
            for keyword in key.split(" "):
                if compare(word, keyword):
                    if not key in candidate_similar_statements:
                        candidate_similar_statements.append(key)
                        break
    return candidate_similar_statements

def compare(word1, word2):
    phrase1 = list(word1)
    phrase2 = list(word2)
    score1 = score(phrase1)
    score2 = score(phrase2)
    total_vec = [word for word in phrase1] + [word for word in phrase2 if not word in phrase1]

    vec1 = [0 for i in range(0,len(total_vec))]
    vec2 = [0 for i in range(0,len(total_vec))]
    
    for i in range(0,len(total_vec)):
        try:
            vec1[i] += score1[total_vec[i]]
        except KeyError:
            pass

        try:
            vec2[i] += score2[total_vec[i]]
        except KeyError:
            pass
    #print("\n",distance(vec1,vec2),"\n",word1,"\n",word2)
    if distance(vec1, vec2) <= SIMILARITY_THRESHHOLD:
        return True
    else:
        
        return False
    
def vectorize(phrase1, phrase2):
    #print("vectorize")
    score1 = score(phrase1)
    score2 = score(phrase2)
    total_vec = [word for word in phrase1] + [word for word in phrase2 if not word in phrase1]
        
    vec1 = [0 for i in range(0,len(total_vec))]
    vec2 = [0 for i in range(0,len(total_vec))]
    
    for i in range(0,len(total_vec)):
        try:
            vec1[i] += score1[total_vec[i]]
        except KeyError:
            for word in score1.keys():
                if compare(word, total_vec[i]):
                    #print(word, total_vec[i], " MATCH!")
                    vec1[i] += scoreOne(total_vec[i])

        try:
            vec2[i] += score2[total_vec[i]]
        except KeyError:
            for word in score2.keys():
                if compare(word, total_vec[i]):
                    #print(word, total_vec[i], " MATCH!")
                    
                    vec2[i] += scoreOne(total_vec[i])
                
    return vec1, vec2
    

def distance(vec1, vec2):    
    distance = 0.0
    if len(vec1) != len(vec2):
        raise Exception
    for i in range(0,len(vec1)):
        distance += (vec1[i]-vec2[i])**2
    return math.sqrt(distance)

vocabulary = addPodcastVocabulary(vocabulary)

prompt = ""
person_speak = "Hello. What is your favorite game to play?"

while "bye" not in person_speak.lower():
    person_speak = input(prompt)
    words = prepareInput(person_speak)
    similar_statements = retrieve_similar_statements(words)

    statement_scores = []
    min_score = 1000000
    best_phrase = "I got nothing..."
    for statement in similar_statements:
        vec1, vec2 = vectorize(words, prepareInput(statement))
        distance_between = distance(vec1, vec2)

        #print("FINAL STATS", statement, vec1, vec2, distance_between)
        statement_scores.append((vocabulary[statement], distance_between))
        if distance_between < min_score:
            min_score = distance_between
            best_phrase = vocabulary[statement]
    print(best_phrase)
    #print(statement_scores)
    
