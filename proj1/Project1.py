import matplotlib.pyplot as plot
from matplotlib.ticker import PercentFormatter
import numpy as np
import os, sys, traceback, shutil
from sklearn.linear_model import LinearRegression

debug = False
"""
Entry point of the program
"""
def main():
    print ("Program started")

    for r, d, f in os.walk("Output/"):
            for file_path in f:
                os.remove("Output/" + file_path)

    summary_file = open("Output/summary.txt", "w", encoding="utf-8")
   
    file_results = []

    #What this loop does is it gets all the txt files from the Input directory and sends each through our program
    if debug: 
        process_file("test.txt", summary_file)
    else:
        for r, d, f in os.walk("Input/"):
            for file_path in f:
                if '.txt' in file_path:
                    f_ind = process_file(file_path, summary_file)
                    file_results.append(f_ind)

    # Print another graph comparing the Flesch indices along with their average sentence length
    file_names = []
    f_indexs = []
    avg_words_per_sent = []
    avg_sylla_per_sent = []
    
    for tup in file_results:
        file_names.append(tup[0])
        f_indexs.append(tup[1])
        avg_words_per_sent.append(tup[2])
        avg_sylla_per_sent.append(tup[3])
    
    """
        Flecsh Index vs Average words per Sentence
    """
    #Histogram on average words per Sentence
    plot.clf()
    file_names = tuple(file_names)
    ind = np.arange(len(avg_words_per_sent))
    width = 0.25
    fig = plot.figure()
    ax = fig.add_subplot(111)
    ax.bar(ind, f_indexs, width, color='r')
    ax.bar(ind, avg_words_per_sent, width, color='b')
    ax.set_ylabel("Flesch Index vs. Average Words Per Sentence")
    ax.legend((f_indexs, avg_words_per_sent), ("Flesch Index", "Avg. Words/Sentence"))
    plot.show()

    #Fits our linear regression model
    X = np.array(avg_words_per_sent).reshape(-1, 1)
    Y = np.array(f_indexs).reshape(-1, 1)
    linear_regressor = LinearRegression()
    linear_regressor.fit(X, Y)
    Y_pred = linear_regressor.predict(X)

    #Visualizes the data for our linear regression model
    result = "\n\nFlesch Index vs Avg. Words Per Sentence\nR^2:" + str(linear_regressor.score(X, Y)) + "\n" + "Slope (M):" + str(linear_regressor.coef_) + "Y-intercept:" + str(linear_regressor.intercept_) + "\n"
    print(result)
    summary_file.write(result)
    plot.clf()
    plot.scatter(X, Y)
    plot.plot(X, Y_pred, color='red')
    plot.xlabel("Average Words Per Sentence")
    plot.ylabel("Flesch Index")
    plot.title("Relation of Flesch Index vs Avg. Words Per Sentence")
    plot.savefig("Output/Flesch Index vs Avg. Words Per Sentence.png")
    plot.show()

    """
       Flecsh Index vs Average Syllables Per Sentence
    """
    #Fits our linear regression model
    X = np.array(avg_sylla_per_sent).reshape(-1, 1)
    Y = np.array(f_indexs).reshape(-1, 1)
    linear_regressor = LinearRegression()
    linear_regressor.fit(X, Y)
    Y_pred = linear_regressor.predict(X)

    #Visualizes the data for our linear regression model
    result = "\n\nFlesch Index vs Avg. Syllables Per Sentence\nR^2:" + str(linear_regressor.score(X, Y)) + "\n" + "Slope (M):" + str(linear_regressor.coef_) + "Y-intercept:" + str(linear_regressor.intercept_) + "\n"
    print(result)
    summary_file.write(result)
    plot.clf()
    plot.scatter(X, Y)
    plot.plot(X, Y_pred, color='red')
    plot.xlabel("Average Syllables Per Sentence")
    plot.ylabel("Flesch Index")
    plot.title("Relation of Flesch Index vs Avg. Syllables Per Sentence")
    plot.savefig("Output/Flesch Index vs Avg. Syllables Per Sentence.png")
    plot.show()

    """
       Average Words per Sentence vs Average Syllables Per Sentence
    """
    #Fits our linear regression model
    X = np.array(avg_sylla_per_sent).reshape(-1, 1)
    Y = np.array(avg_words_per_sent).reshape(-1, 1)
    linear_regressor = LinearRegression()
    linear_regressor.fit(X, Y)
    Y_pred = linear_regressor.predict(X)

    #Visualizes the data for our linear regression model
    result = "\n\nAvg. Words per Sentence vs Avg. Syllables Per Sentence\nR^2:" + str(linear_regressor.score(X, Y)) + "\n" + "Slope (M):" + str(linear_regressor.coef_) + "Y-intercept:" + str(linear_regressor.intercept_) + "\n"
    print(result)
    summary_file.write(result)
    plot.clf()
    plot.scatter(X, Y)
    plot.plot(X, Y_pred, color='red')
    plot.xlabel("Average Syllables Per Sentence")
    plot.ylabel("Average Words Per Sentence")
    plot.title("Relation of Avg. Words Per Sentence vs Avg. Syllables Per Sentence")
    plot.savefig("Output/Avg. Words Per Sentence vs Avg. Syllables Per Sentence.png")
    plot.show()

    summary_file.close()

"""
This method processes the file and extracts required data
Returns (path, f_index, words/sentences, syllables/sentences)
"""
def process_file(path, out_file):
    print("=================")
    print("Processing Input/" + path)

    syllables = 0
    words = 0
    sentences = 0
    words_in_sentence = 0

    # Open text document to read with str_tok
    in_file = open("Input/" + path, "r", encoding="utf-8")

    all_words = []
    data = []
    
    # Read file line by line
    for line in in_file:
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
    
    f_index = calc_flesch(syllables, words, sentences)

    file_report = "The total complexity of " + path + " with " + str(sentences) + " sentences, " + str(words) + " words, and " + str(syllables) + " syllables has a Flesch complexity of " + str(f_index) + "."
    file_report += " " + calc_grade(f_index)
    file_report += " Words/Sentences: " +  str(words/sentences) + ". Syllables/Sentences: " + str(syllables/sentences) + "."
    print(file_report)
    out_file.write(file_report+'\n')

    #Creates the histogram of distribution of word syllable count.
    plot.clf()
    plot.hist(data, bins=np.arange(1,max(data)+1.5)-0.5, weights=np.ones(len(data)) / len(data))
    plot.xticks(np.arange(min(data), max(data)+1, 1.0))
    plot.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plot.xlabel("Syllables")
    plot.ylabel("Percents")
    plot.title("Percentage of words with n syllables in " + path)
    out_path = str("Output/"+path+".png")
    plot.savefig(out_path)

    in_file.close()
    return (path, f_index, words/sentences, syllables/sentences)
"""
    Calculates the flesch index
"""
def calc_flesch(syllables, words, sentences):
    return 206.835 - (84.6 * (float(syllables) / float(words))) - (1.015 * (float(words) / float(sentences)))

"""
    Calculates the number of syllables in a word
"""
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
"""
    Checks to see if a character is a consonant
"""
def is_consonant(c):
    c = c.lower()
    consonants = ['b' ,'c' ,'d' ,'f' ,'g' ,'h' ,'j' ,'k' ,'l' ,'m' ,'n' ,'p' ,'q' ,'r' ,'s' ,'t' ,'v' ,'w' ,'x' ,'z']
    return (c in consonants)

"""
    Checks to see if a character is a vowel
"""
def is_vowel(c):
    c = c.lower()
    vowels = ['a' ,'e' ,'i' ,'o' ,'u', 'y']
    return (c in vowels)

"""
    Calculates the grade level of reading from the flesch index
"""
def calc_grade(fl_ind):
    if (fl_ind > 90):
        return "This text has a 5th grade reading level. It should be easily understood by an average 11-year-old student."
    elif (fl_ind > 80):
        return "This text has a 6th grade reading level. Easy to read, conversational english for consumers."
    elif (fl_ind > 70):
        return "This text has a 7th grade reading level. Fairly easy to read."
    elif (fl_ind > 60):
        return "This text has an 8th-9th grade reading level. Plain english, easily understood by 13-15 year old students."
    elif (fl_ind > 50):
        return "This text has a 10th-12th grade reading level. Fairly difficult to read."
    elif (fl_ind > 30):
        return "This text has a college reading level. Difficult to read."
    else:
        return "This text has a college graduate reading level. Very difficult to read, best understood by university graduates."

main()
