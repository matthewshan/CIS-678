import matplotlib.pyplot as plot
from matplotlib.ticker import PercentFormatter
import numpy as np
import os, sys, traceback
debug = False
def main():
    print ("Program started")
   
    #What this loop basically does it gets all the txt files from the Input directory and sends each through our program
    if debug: 
        process_file("test.txt")
    else:
        for r, d, f in os.walk("Input/"):
            for file_path in f:
                if '.txt' in file_path:
                    process_file(file_path)    


def process_file(path):
    print("=================")
    print("Processing Input/" + path)

    syllables = 0
    words = 0
    sentences = 0
    words_in_sentence = 0

    # Open text document to read with str_tok
    file = open("Input/" + path, "r", encoding="utf-8")

    all_words = []
    data = [] #{}
    
    # Read file line by line
    for line in file:
        line_words = line.split(" ")
        # Append line word by word
        for word in line_words:
            all_words.append(word)

    #Process each word per iteration
    for nextWord in all_words:
        # Read another word, so increment words

        if (len(nextWord) > 0 and nextWord[-1] == "\n"):
            nextWord = nextWord[:-1]

        # If there is a period, exclamation, or a question mark, increment sentences
        if (len(nextWord) > 1 and ((nextWord[-1] == ".") or (nextWord[-1] == "!") or (nextWord[-1] == "?"))):
            if (words_in_sentence > 0):
                sentences = sentences + 1
                words_in_sentence = 0   

        # Trim any punctuation off the start of the word so it is just letters
        while (len(nextWord) > 0 and not nextWord[0].isalpha()):#not is_vowel(nextWord[0]) and not is_consonant(nextWord[0])):
            nextWord = nextWord[1:]

        # Trim any punctuation off the end of the word so it is just letters
        while (len(nextWord) > 0 and not nextWord[len(nextWord)-1].isalpha()):#not is_vowel(nextWord[len(nextWord)-1]) and not is_consonant(nextWord[len(nextWord)-1])):
            nextWord = nextWord[:-1]

        #If the word length is zero or if not a letter, don't count it as a word.
        if len(nextWord) > 0 and nextWord != " ":
            words = words + 1
            words_in_sentence += 1
            # Calculate the number of syllables and add them to syllables
            try:
                temp_syllables = calc_syllables(nextWord)
            except:
                print("[!!!] calc_syllables broke on word `" + nextWord + '`')
                traceback.print_exc(file=sys.stdout)
            data.append(temp_syllables)
            syllables = syllables + temp_syllables
    
    f_ind = calc_flesch(syllables, words, sentences)
    print("The total complexity of " + path + " with " + str(sentences) + " sentences, " + str(words) + " words, and " + str(syllables) + " syllables has a Flesch complexity of " + str(f_ind) + ".")

    #Creates the histogram
    #plot.hist(data, range=(2,3), bins=np.arange(longest_word)-0.5, weights=np.ones(len(data)) / len(data))
    #plot.hist(data, range=[1,max(data)], bins=np.arange((max(data)*1.5)+1)-0.5, weights=np.ones(len(data)) / len(data))
    plot.hist(data, bins=np.arange(1,max(data)+1.5)-0.5, weights=np.ones(len(data)) / len(data))
    plot.xticks(np.arange(min(data), max(data)+1, 1.0))
    plot.gca().yaxis.set_major_formatter(PercentFormatter(1))

    #Adds labels
    plot.xlabel("Syllables")
    plot.ylabel("Percents")
    plot.title("Percentage of words with n syllables in " + path)
    plot.show()

    # plot.plot(xvals, data_arr)
    # plot.show()

def calc_flesch(syllables, words, sentences):
    return 206.835 - (84.6 * (float(syllables) / float(words))) - (1.015 * (float(words) / float(sentences)))

def calc_syllables(word):
    total = 0
    curr_ind = 0

    # Update the word length
    word_len = len(word)

    if debug:
        print("Word: " + str(word))

    # If the word starts with a vowel, increase the number of syllables
    if (is_vowel(word[0])):
        total = total + 1
    elif (not is_consonant(word[0])):
        # If not consonant or a vowel, it must be a number or a non-letter, and it makes sense to return 1 syllable for that imo
        print("This shouldn't print (If not consonant or a vowel). The word was: " + word)
        return 1
    
    # If at least 2 letters
    while (curr_ind < word_len - 1):
        # Check if the current character is a consonant
        if (is_consonant(word[curr_ind])):
            # If it is, see if the next is a vowel
            if (is_vowel(word[curr_ind + 1])):
                # If it is, make sure it isn't the last character (ie. make sure the curr_ind isn't 2 less than the word length) and an 'e' at the same time
                if not (curr_ind == word_len - 2 and word[curr_ind + 1].lower() == 'e'):
                    # Then increment the number of syllables
                    #print("Found a consonant and vowel syllable")
                    total = total + 1
                else:
                    if (word[curr_ind].lower() == 'l'):
                        total += 1
        curr_ind += 1

    if (total < 1):
        total = 1

    if debug:
        print("Total syllables: " + str(total))

    return total

def is_consonant(c):
    c = c.lower()
    consonants = ['b' ,'c' ,'d' ,'f' ,'g' ,'h' ,'j' ,'k' ,'l' ,'m' ,'n' ,'p' ,'q' ,'r' ,'s' ,'t' ,'v' ,'w' ,'x' ,'z']
    return (c in consonants)

def is_vowel(c):
    c = c.lower()
    vowels = ['a' ,'e' ,'i' ,'o' ,'u', 'y']
    return (c in vowels)

main()
