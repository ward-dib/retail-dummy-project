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

 
# ---------- PART 3: Simple "Weights" ----------

# Assignt weights to letters as the percentage of total.
freq_percent = {char: val / sum(letter_freq().values())
                for char, val in letter_freq().items()}


def words_weighted(word):
    score = 0.0
    for char in word:
        score += freq_percent[char]
    return score / (5 - len(set(word)) + 1)

def sorted_weights(allwords):
    weight_tupples = sorted([(word, words_weighted(word)) for word in allwords],
                            key = lambda x:x[1], reverse = False)
    return weight_tupples


# ---------- PART 4: SOLVER 1 (Deletes grey, yellow, keeps green, prints possible remaining words sorted by word weight above) ----------

# Green is "g"
# Yellow is "y"
# Black is "b"

def letter_info(letter_hints: list):
  black_letter = []
  green_letter = []
  yellow_letter = []
  for l, hint in letter_hints:
    if hint.lower() == 'b':
      black_letter.append(l)
    elif hint.lower() == 'g':
      green_letter.append((l, guessed.index(l)))
    else:
      yellow_letter.append((l, guessed.index(l)))
  return black_letter, green_letter, yellow_letter

def with_green(word_list, green_letter):
  if len(green_letter) > 0:
    possible_words = []
    for w in word_list:
        try:
          if all([w.index(l) == idx for l, idx in green_letter]):
            possible_words.append(w)
        except:
          continue
    return list(set(possible_words))
  else:
    return word_list

def with_black(word_list: list, black_letter: list):
  if len(black_letter) > 0:
    discard = []
    for w in word_list:
        for l in black_letter:
          if l in w:
            discard.append(w)
    return list(set(discard))
  else:
    return []

def with_yellow(word_list: list, yellow_letter: list):
  if len(yellow_letter) > 0:
    possible_words = []
    for w in word_list:
      if all([l in w for l, idx in yellow_letter]) and all([w.index(l) != idx for l, idx in yellow_letter]):
            possible_words.append(w)
    return list(set(possible_words))
  else:
    return word_list

def correct_word(green_letter):
  word = ['_'] * 5
  for letter, idx in green_letter:
    word[idx] = letter
  return ''.join(word)


word_list = []
words = allwords
for i in words:
  if len(i) == 5:
    word_list.append(i.lower())

word_list = list(set(word_list))
hint = int(input(f"Inspiration starters (choose a number): "))
if hint:
  for word in list((sorted_weights(word_list)[:hint])):
    print(word)
else:
  print("Ok, think of your own.")

print("__________________________")

while True:
  guessed = input("Type guess: ").lower()
  result = input("Type feedback: (bgy)")

  if result != 'ggggg':
    letter_hints = list(zip(list(guessed), list(result)))
    black_letter, green_letter, yellow_letter = letter_info(letter_hints)
    
    discard = with_black(word_list, black_letter)
    for ds in discard:
      word_list.remove(ds)
    corrects_list = with_green(word_list, green_letter)
    possible_words = with_yellow(corrects_list, yellow_letter)
    word_list = possible_words

    print(f"Number of possible words: {len(possible_words)}")
    print(f"Correct letters: {correct_word(green_letter)}")

    if len(possible_words) > 50:
      print(f"Possible words (top 50 listed): ")
      for word in list((sorted_weights(word_list)[:50])):
        print(word)
    else:
      print(f"All possible words:")
      for word in list(sorted_weights(possible_words)):
        print(word)
    print("__________________________")

  else:
      print(f"Correct solution is: {guessed}")
      break
  


# ---------- PART 5: SOLVER 2 (Runs solver 1 with a condition) ----------

# The idea is, IF len(possible_words) > remaining_attempts, AND all (possible_answers) have GGG, try entirely new letters. 
# Get new info, and when you break the green cycle, proceed with guesser 1 again.



