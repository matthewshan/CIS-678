def main():
    syllables = 0
    words = 0
    sentences = 0
    
    print ("Program started")

    # Open text document to read with str_tok
    file = open("test.txt", "r")

    all_words = []

    # Read file line by line
    for line in file:
        line_words = line.split(" ")
        # Append line word by word
        for word in line_words:
            all_words.append(word)

    for nextWord in all_words:
        # Read another word, so increment words
        words = words + 1

        # If there is a period, exclamation, or a question mark, increment sentences
        if (("." in nextWord) or ("!" in nextWord) or ("?" in nextWord)):
            sentences = sentences + 1

        # Calculate the number of syllables and add them to syllables
        syllables = syllables + calc_syllables(nextWord)
    
    f_ind = calc_flesch(syllables, words, sentences)
    print("The total complexity of your document with " + str(sentences) + " sentences, " + str(words) + " words, and " + str(syllables) + " syllables has a Flesch complexity of " + str(f_ind) + ".")

def calc_flesch(syllables, words, sentences):
    return 206.835 - (84.6 * (float(syllables) / float(words))) - (1.015 * (float(words) / float(sentences)))

def calc_syllables(word):
    total = 0
    curr_ind = 0

    # Trim any punctuation off the start of the word so it is just letters
    while not is_vowel(word[0]) and not is_consonant(word[0]):
        word = word[1:]

    # Trim any punctuation off the end of the word so it is just letters
    word_len = len(word)
    while not is_vowel(word[word_len-1]) and not is_consonant(word[word_len-1]):
        word = word[:-1]
        word_len = len(word)

    # Update the word length
    word_len = len(word)

    # If the word starts with a vowel, increase the number of syllables
    if (is_vowel(word[0])):
        total = total + 1
    elif (not is_consonant(word[0])):
        # If not consonant or a vowel, it must be a number or a non-letter, and it makes sense to return 1 syllable for that imo
        return 1
    
    # If at least 2 letters
    while (curr_ind < word_len - 1):
        # Check if the current character is a consonant
        if (is_consonant(word[curr_ind])):
            # If it is, see if the next is a vowel
            if (is_vowel(word[curr_ind + 1])):
                # If it is, make sure it isn't the last character (ie. make sure the curr_ind isn't 2 less than the word length) and an 'e' at the same time
                if not(curr_ind == word_len - 2 and word[curr_ind + 1].lower() != 'e'):
                    # Then increment the number of syllables
                    total = total + 1
        curr_ind += 1
    return total

def is_consonant(c):
    c = c.lower()
    if (c == 'b' or c == 'c' or c == 'd' or c == 'f' or c == 'g' or c == 'h' or c == 'j' or c == 'k' or c == 'l' or c == 'm' or c == 'n' or c == 'o' or c == 'p' or c == 'q' or c == 'r' or c == 's' or c == 't' or c == 'v' or c == 'w' or c == 'x' or c == 'z'):
        return True
    return False

def is_vowel(c):
    c = c.lower()
    if (c == 'a' or c == 'e' or c == 'i' or c == 'o' or c == 'u' or c == 'y'):
        return True
    return False

main()