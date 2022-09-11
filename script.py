import random
import re

with open('allwords.txt', 'r') as a:
    allwords = []
    allwords = a.read().split('","')
    
with open('answerwords.txt', 'r') as a:
    answerwords = []
    answerwords = a.read().split('","')
    answerwords = [re.sub('[^a-zA-Z0-9]+', '', _) for _ in answerwords]
    
# Letter frequency function; will count the occurance of the letters and sort them accordingly.

def wordList(sortedlist):
    def letter_freq():
        counts = {}
        sortedcounts = {}
        
        for word in answerwords:
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
    
    
    # Assignt weights to letters as the percentage of total.
    freq_percent = {char: val / sum(letter_freq().values())
                    for char, val in letter_freq().items()}
    
    def words_weighted(word):
        score = 0.0
        for char in word:
            score += freq_percent[char]
        return score / (5 - len(set(word)) + 1)
    
    def sorted_weights(answerwords):
        weight_tupples = sorted([(word,
                                  words_weighted(word)) for word in answerwords],
                                key = lambda x:x[1], reverse = True)
        return weight_tupples
    return sorted_weights(sortedlist)

# Will give hints as a string "ggbby" etc.
class WordleAPI:

    def __init__(self, answer):
        self.answer = answer
    
    def playWordle(self, guess):
            
        guesscode = ["", "", "", "", ""]
        
        if guess not in allwords:
            return print("That is not a valid word!")
        
        elif guess in allwords:   
            
            for x in range(len(guess)): 
                
                if guess[x] not in self.answer[x]: 
                    guesscode[x] = "b"
                                
                if guess[x] in self.answer: 
                    guesscode[x] = "y"
                                
                if guess[x] == self.answer[x]: 
                    guesscode[x] = "g"                  
                
        return "".join(guesscode)   

# function to create a list of guess words 

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
  word = ['_', '_', '_', '_', '_']
  for letter, idx in green_letter:
    word[idx] = letter
  return ''.join(word)

word_list = []
words = answerwords
for i in words:
  if len(i) == 5:
    word_list.append(i.lower())

guess_words = []
results = []

while True:
        
    while len(guess_words) < 6:

        guessed = input("Type guess: ").lower() 
        guess_words.append(guessed)
        result = input("Type hints: ").lower() 
        results.append(result)
        
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
            for word in list((wordList(word_list)[:50])):
              print(word)
          else:
            print(f"All possible words:")
            for word in list(wordList(possible_words)):
              print(word)
          print("__________________________")
        
        else:
            print(f"Correct solution is: {guessed}")
            break

from typing import Any, Dict

def play_wordle(api: WordleAPI) -> Dict[str, Any]:


    n_guesses = 0
    
    guess = guess_words[0]
    
    
    result = {
        "words_tried": [],
        "colours": [],
        "n_guesses": 0,
        "success": 0}

    while n_guesses < 6:

        n_guesses += 1
        score = api.playWordle(guess)

        result["words_tried"].append(guess)
        result["colours"].append(score)

        if score == "ggggg":
            result["success"] = 1
            result["n_guesses"] = n_guesses
            return result
        
        else:
            
            guess = guess_words[n_guesses - 1]

    result["n_guesses"] = n_guesses
    result["success"] = 0
    
    return result

print(play_wordle(WordleAPI("flood")))
