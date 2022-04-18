# ---------- PART 1 : Get data ----------

# Import required libraries.
import nltk
nltk.download('words')
from nltk.corpus import words
words = words.words()
import re

# Open the text file containing all the words that Wordle (NYT) uses.
# Copied from the website source code at https://www.nytimes.com/games/wordle/main.b84b7aa7.js.
with open('nytwords.txt', 'r') as a:
    nytwords = []
    nytwords = a.read().split('","')


# Extract only 5 letter words from the dataset.
def allwords():
    
    wordlist = words
        
    # Manyally add NYT Wordle words that are not in our dataset.
    wordlist = list(set(nytwords + wordlist)) 
    wordlist = sorted(wordlist)
    
    # Remove anything more than 5 letters
    wordlist = filter(lambda words: len (words) == 5, wordlist) 
    wordlist = [words for words in wordlist if len (words) == 5]

    # Remove capital letters (removing names of cities and people), special characters, and empties.
    wordlist = [re.sub(r'\s*[A-Z]\w*\s*', '', string) for string in wordlist]
    wordlist = [string.replace('"', '') for string in wordlist]
    wordlist = ' '.join(wordlist).split()
    
    # Save the output to a text file.
    with open("allwords.txt", "w") as output:
       output.write(str(wordlist))

    return wordlist

# Call as a new list.
print(allwords())
print(len(list(allwords())))

# ---------- PART 2 : Letter Frequency ----------

# Import required libraries.
import seaborn as sns
import matplotlib.pyplot as plt

# Letter frequency function; will count the occurance of the letters and sort them accordingly.
def letter_freq():
    counts = {}
    sortedcounts = {}
    
    for word in allwords:
        for letter in word:
            if letter.isalpha():
                counts.setdefault(letter, 0)
                counts[letter.lower()] += 1
                counts = {x:y for x, y in counts.items() if y!= 0}
                sortedcounts = sorted(counts.items(),
                                    key = lambda x:x[1],
                                    reverse = True)
                sortedcounts = dict(sortedcounts)
    return sortedcounts

# Checks.
print(letter_freq())

def plotting():
    fig = plt.figure(figsize = (10, 4))
    sns.set(style = 'darkgrid')
    plt.bar(*zip(*letter_freq().items()), color = '#756bb1')
    plt.axhline(y = (max(letter_freq().values())/2),
                ls = 'solid', lw = 2, c = '#41b6c4', alpha = 0.75)
    plt.xlabel('Letters')
    plt.ylabel('Number of occurances in 5 letter words')
    plt.show()
    fig.savefig('letter_freq.png', dpi = 200)


def top_words():
    clw = []
    bestwords = []
    a = list(letter_freq().keys())
    b = ''.join(a[0:7]) 
    for i in allwords:
        c = all(x in b for x in i)
        if c:
            clw.append(i)
            clw.sort()
    # make sure no letters are repeated (aalii?) so we get the most amount of information
    for i in clw:
        uniq_letters = len(set(i))
        if uniq_letters == 5:
            bestwords.append(i)
    
    return bestwords
 
print(f"{len(top_words())} words contain the 7 most frequently used letters.")

print(top_words())

 
# ---------- PART 3: Simple Weights ----------

# Assignt weights to letters as the percentage of total.
freq_percent = {char: val / sum(letter_freq().values())
                for char, val in letter_freq().items()}


def words_weighted(word):
    score = 0.0
    for char in word:
        score += freq_percent[char]
    return score / (5 - len(set(word)) + 1)

words_weighted("arose")

def sorted_weights(allwords):
    weight_tupples = sorted([(word, words_weighted(word)) for word in allwords],
                            key = lambda x:x[1], reverse = False)
    return weight_tupples

top7 = sorted_weights(top_words())
print(top7)

# ---------- PART 4: Delete function to be called on given lists ----------

def remove_words(in_list, out_list):
    new_list = []
    for line in in_list:
        new_words = ''.join([word for word in line.split()
                             if not any([phrase in word for phrase in char_list])])
        new_list.append(new_words)
    return new_list
  
"""

Example of use: 

in_list = allwords
out_list = ['a', 'o', 's']

# Any characters we want. Further down, this will be a list created by the guesser function, consisting of grey and yellow letters.
# Then we call the function on the lists we created.
guess = remove_words(in_list, out_list)

"""

# ---------- PART 5: Guesser 1 (deletes grey, yellow, repeat green.) ----------


