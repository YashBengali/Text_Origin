#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 19:19:42 2019

@author: yash
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 14:17:46 2019

@author: yash
"""

import math
import random


def create_dictionary(text):
    """Takes a string which represents the name of the file and splits that 
    file up into key-value pairs
    Input filename: the name of the file
    """
    
    
    #SPLITTING THE DATA
    words = text.split()
    
    #CREATE THE DICTIONARY
    d = {}
    currentWord = '$'
    
    for nextWord in words:
        if currentWord not in d:
            d[currentWord] = [nextWord]
        else:
            d[currentWord] += [nextWord]
        lastChar = nextWord[len(nextWord)-1]
        if lastChar in '!?.':
            currentWord = '$'
        else:
            currentWord = nextWord
    return d

def generate_text(word_dict, num_words):
    """Generates text using a markov model that has the length of num_words
    Input word_dict: the dictionary containing the words
    Input num_words: the desired length of the ouput
    """
    stringToReturn = ''
    currentWord = '$'
    for x in range(num_words):
        wordToPrint = random.choice(word_dict[currentWord])
        stringToReturn += wordToPrint + ' '
        lastChar = wordToPrint[len(wordToPrint)-1]
        if lastChar in '!?.':
            currentWord = '$'
        else:
            currentWord = wordToPrint
    return stringToReturn
        

def clean_text(txt):
    """Takes a string and cleans it by making it all lowercase with no punctuation
    """
    txt = txt.lower()
    words = txt.split()
    cleaned = ''
    for x in words:
        for y in x:
            if y in 'abcdefghijklmnopqrstuvwxyz123456789':
                cleaned += y
        cleaned += ' '
    #gets rid of extra space the line above put in on the last iteration
    cleaned = cleaned[:-1]
    answer = cleaned.split()
    
    return answer

def stem(s):
    """Given a word, it returns the stem of the word
    Input s: the word
    """
    if len(s)<=4:
        return s
    elif s[-3:] == 'ing':
        if s[-4] == s[-5]:
            s = s[:-4]
        else:
            s = s[:-3]
    elif s[-2:] == 'er':
        s = s[:-3]
    elif s[-1] == 's':
        s = s[:-1]
    elif s[-2:] == 'ed':
        s = s[:-2]
    elif s[-3:] == 'man':
        s = s[:-3]
    elif s[-2:] == 'ly':
        s = s[:-2]
    elif s[-1] == 'y':
        s = s[:-1]
    return s

def compare_dictionaries(d1, d2):
    """Compares two dictionaries and returns their similarity score
    """
    score = 0
    #total number of words in the first dictionary (counted by the values)
    total = sum(d1.values())
    temporary_score = 0
   
    for x in d2:
        if x in d1:
            temporary_score = d1[x] / total
            #FIGURE OUT HOW TO LOG SOMETHING
            temporary_score = d2[x] * math.log(temporary_score)
            score += temporary_score
            temporary_score = 0
        else:
            temporary_score = d2[x] * math.log(0.5 / total)
            score += temporary_score
            temporary_score = 0
    return score

class TextModel:
    """Class which will serve to help model any types of text encountered
    """
    
    def __init__(self, model_name):
        """Constructor for the TextModel class
        Input model_name: a string that is a label for this text model
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        #THE NEXT DICTIONARY IS THE ONE THAT WAS YOUR CHOICE. IT GETS THE 
        #NEXT WORD RIGHT AFTER THE CURRENT ONE. THIS LETS YOU BUILD A DICTIONARY
        #WHERE YOU CAN BASED ON ONE TEXT OF WHAT WORD WAS CHOSEN NEXT PREDICT
        #THE NEXT WORD AND SEE IF IT ENDS UP MATCHING 
        self.markov_model = {}
        
        
    def __repr__(self):
        """Properly prints the text model name, number of words, and number of word lengths
        """
        toReturn = ''
        toReturn = ("text model name: " + self.name + '\n')
        toReturn += ('  number of words: ' + str(len(self.words)) + '\n')
        toReturn += ('  number of word lengths: ' + str(len(self.word_lengths)) + '\n')
        toReturn += ('  number of stems: ' + str(len(self.stems)) + '\n')
        toReturn += ('  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n')
        toReturn += ('  number of model model length: ' + str(len(self.markov_model)))
        return toReturn
        
    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
           to all of the dictionaries in this text model.
        """
        
        #generating the markov model
        
       
        self.markov_model = create_dictionary(s)
    
        #UPDATING THE SENTENCE LENGTHS 
        numWordsCounter = 0
        tempWords = s.split()
        for w in tempWords:
            if '.' in w or '!' in w or '?' in w:
                numWordsCounter+=1
                if numWordsCounter not in self.sentence_lengths:
                    self.sentence_lengths[numWordsCounter] = 1
                else:
                    self.sentence_lengths[numWordsCounter] += 1
                numWordsCounter = 0
            else:
                numWordsCounter += 1
            
        # Add code to clean the text and split it into a list of words.
        # *Hint:* Call one of the functions you have already written!
        word_list = clean_text(s)
        wordLength = 0
        # Template for updating the words dictionary.
        previousWord = ''
        counter = 0
        stemWord = ''
        for w in word_list:
            # Update self.words to reflect w
            # either add a new key-value pair for w
            # or update the existing key-value pair.
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
                
            # Add code to update other feature dictionaries.
            wordLength = len(w)
            if wordLength not in self.word_lengths:
                self.word_lengths[wordLength] = 1
            else:
                self.word_lengths[wordLength] += 1
            
            #adding stem word to dictionary
            stemWord = stem(w)
            if stemWord not in self.stems:
                self.stems[stemWord] = 1
            else:
                self.stems[stemWord] += 1
            
            #adding nextWord to dictionary
           # if counter == 0:
           #     previousWord = w
          #      counter = 1
           # else:
           #     if previousWord not in self.adjacent_word:
          #          self.adjacent_word[previousWord] = [w]
          #          previousWord = w
            #    else:
            #        self.adjacent_word[previousWord] += [w]
            #        previousWord = w
        
                
                
            
    def add_file(self, filename):
        """adds all of the text in the file identified by filename to the model
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        s = f.read()
        self.add_string(s)
        
    def save_model(self):
        """writes the current dictionaries of the object to a file
        """
        f = open(self.name + '_words', 'w')      # Open file for writing.
        f.write(str(self.words))              # Writes the dictionary to the file.
        f.close()                    # Close the file.
        f = open(self.name +'_word_lengths', 'w')
        f.write(str(self.word_lengths))
        f.close()
        f = open(self.name +'_stems', 'w')
        f.write(str(self.stems))
        f.close()
        f = open(self.name +'_sentence_lengths', 'w')
        f.write(str(self.sentence_lengths))
        f.close()
        f = open(self.name +'_markov_model', 'w')
        f.write(str(self.markov_model))
        f.close()
        
    def read_model(self):
        """Reads previously stored dictionaries
        """
        f = open(self.name + '_words', 'r')    # Open for reading.
        d_str = f.read()           # Read in a string that represents a dict.
        f.close()
        self.words = dict(eval(d_str))      # Convert the string to a dictionary.
        
        
        f = open(self.name +'_word_lengths', 'r')    # Open for reading.
        d_str = f.read()           # Read in a string that represents a dict.
        f.close()
        self.word_lengths = dict(eval(d_str))
        
        f = open(self.name +'_stems', 'r')    # Open for reading.
        d_str = f.read()           # Read in a string that represents a dict.
        f.close()
        self.stems = dict(eval(d_str))
        
        f = open(self.name +'_sentence_lengths', 'r')    # Open for reading.
        d_str = f.read()           # Read in a string that represents a dict.
        f.close()
        self.sentence_lengths = dict(eval(d_str))
        
        f = open(self.name +'_markov_model', 'r')    # Open for reading.
        d_str = f.read()           # Read in a string that represents a dict.
        f.close()
        self.markov_model = dict(eval(d_str))
        
    def similarity_scores(self, other):
        """calls the compare_dictionaries function to compute the 
        similarity scores for two dictionaries for each type of feature
        """
        score1 = compare_dictionaries(other.words, self.words)
        score2 = compare_dictionaries(other.word_lengths, self.word_lengths)
        score3 = compare_dictionaries(other.stems, self.stems)
        score4 = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        #update this later once you figure out what you are going to do 
        #for your choice of feature
        #INCREASE IT FROM 10 SO IT IS WAY MORE ACCURATE
        s1 = generate_text(other.markov_model, len(other.words))
        s2 = generate_text(self.markov_model, len(self.words))
        test1 = TextModel('first Markov Model')
        test2 = TextModel('second Markov Model')
        test1.add_string(s1)
        test2.add_string(s2)
        #calculating scores for the markov model
        markov1 = compare_dictionaries(test2.words, test1.words)
        markov2 = compare_dictionaries(test2.word_lengths, test1.word_lengths)
        markov3 = compare_dictionaries(test2.stems, test1.stems)
        markov4 = compare_dictionaries(test2.sentence_lengths, test1.sentence_lengths)
        
        
        score5 = (markov1 + markov2 + markov3 + markov4)/4
        return [score1, score2, score3, score4, score5]
        
    def classify(self, source1, source2):
        """returns which source is closest to the original text model
        """
        #count for source 1 and 2 defined below. Goal is to see which one
        #is greater and return the appropriate source
        count1 = 0
        count2 = 0
        scores1 = self.similarity_scores(source1)
        
        scores2 = self.similarity_scores(source2)
     
        for x in range(len(scores1)):
            if scores1[x] > scores2[x]:
                count1 += 1
            else:
                count2 += 1
        
        print('scores for source1: ' + str(scores1))
        print('scores for source2: ' + str(scores2))
        if count1 > count2:
            print('mystery is more likely to have come from source1')
        else:
            print('mystery is more likely to have come from source2')
            


# Copy and paste the following function into finalproject.py
# at the bottom of the file, *outside* of the TextModel class.
def test():
    """ Compares two source models to a mystery text to see which piece
    of text the mystery text is most similar to"""
    source1 = TextModel('source1')
    source1.add_string('I am testing this. I am reking this. I want to make sure that is a longer piece of text with no extra stuff in it because it does keep destroying my code and I am not a fan of it.')



    source2 = TextModel('source2')
    source2.add_string('chandler, monica, and phoebe are the girls from friends. while you may enjoy watching the show, and i do too, it can sometimes be a little bad sad when a good show like friends finally comes to an end.')

    mystery = TextModel('mystery')
    mystery.add_string('Chandler said I love friends friends frineds! no one told you life was gonna be this way, your job is a joke. you are broke. your love life is doa.')
    mystery.classify(source1, source2)
    
def run_tests():
    """ Runs the comparison tests for my chosen texts """
    source1 = TextModel('shakesphere_alls_well_that_ends_well_act1')
    #source1.save_model()
    #source1.add_file('shakesphere.txt')
    source1.add_file('wr120paper.txt')

    source2 = TextModel('huckleberry_finn_chapter1')
    #source2.save_model()
    source2.add_file('huckfinn_chapter1.txt')

    new1 = TextModel('shakesphere_romeo_and_juliet_act1')
    new1.add_file('romeo_and_juliet_act1.txt')
    #new1.save_model()
    new1.classify(source1, source2)
    
    # Add code for three other new models below.
    new2 = TextModel('huckleberry_finn_chapter2')
    new2.add_file('huckfinn_chapter2.txt')
    new2.classify(source1, source2)
    
    new3 = TextModel('wr120paper')
    new3.add_file('wr120paper.txt')
    new3.classify(source1, source2)
    
    new4 = TextModel('greatgatsby_chapter1')
    new4.add_file('greatgatsby_chapter1.txt')
    new4.classify(source1, source2)
    
    
    
    
                    
                
            
            
        
        
    
        
        
    
        
        
        
        
    
