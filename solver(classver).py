# Open the file. This file contains only the official answer word list, 2309 entries.
with open('answerwords.txt', 'r') as a:
    answerwords = []
    answerwords = a.read().split('","')


# Letter frequency function; will count the occurance of the letters and sort them accordingly.

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
    weight_tupples = sorted([(word, words_weighted(word)) for word in answerwords],
                        key=lambda x:x[1], reverse = True)
    return weight_tupples
    print(weight_tupples())

# Open a file with all the possible words, 12974 entiries.
with open('allwords.txt', 'r') as a:
    allwords = []
    allwords = a.read().split('","')

# some arbitrary answer/guess for the sake of trial.
answer = "stare"
guess = "arose"

class GAME():
    
    def __init__(self, play):
        self.play = play
        
    # Simulate a Wordle Game.
    def playWordle(self, play):
             
        def check_guess(answer, guess): 
            guesscode = ["", "", "", "", ""]
            
            if guess not in allwords:
                return print("That is not a valid word!")
            
            elif guess in allwords:   
                
                for x in range(len(guess)): 
                    
                    if guess[x] in answer: 
                        guesscode[x] = "Y"
                    
                    if answer[x] == guess[x]: 
                        guesscode[x] = "G" 
                    
                    if guess[x] not in answer: 
                        guesscode[x] = "B"
                             
                return guesscode
            
        def split(guess):
            return list(guess)
        
        result = dict(zip(split(guess), check_guess(answer, guess)))
                
        return result

    
    # Output the results from the simulation into a string that can be put into the later functions.
    def color_hints(self, colors):
        color_hints = []
        colorstr = ""
        for values in self.playWordle().values():
            color_hints.append(values)
        colorstr = colorstr.join(color_hints)    
        return colorstr    
    
    def solver1(self, solve1):
        
        # After getting feedback from a word, divide the letters into different lists to be processed later.
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
    
        # What to do with green letters (keep only in same place)
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
    
        # What to do with black letters (delete all)
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
    
        # What to do with yellow letters (delete, keep complementary set)
        def with_yellow(word_list: list, yellow_letter: list):
          if len(yellow_letter) > 0:
            possible_words = []
            for w in word_list:
              if all([l in w for l, idx in yellow_letter]) and all([w.index(l) != idx for l, idx in yellow_letter]):
                    possible_words.append(w)
            return list(set(possible_words))
          else:
            return word_list
    
        # Function for the all-green correct word.
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
        
        # Using the generated hints from earlier...
        while True:
          guessed = guess
          result = self.color_hints()
        
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
          
# Open the file. This file contains only the official answer word list, 2309 entries.
with open('answerwords.txt', 'r') as a:
    answerwords = []
    answerwords = a.read().split('","')


# Letter frequency function; will count the occurance of the letters and sort them accordingly.

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
    weight_tupples = sorted([(word, words_weighted(word)) for word in answerwords],
                        key=lambda x:x[1], reverse = True)
    return weight_tupples
    print(weight_tupples())

# Open a file with all the possible words, 12974 entiries.
with open('allwords.txt', 'r') as a:
    allwords = []
    allwords = a.read().split('","')

# some arbitrary answer/guess for the sake of trial.
answer = "stare"
guess = "arose"

class GAME():
    
    def __init__(self, play):
        self.play = play
        
    # Simulate a Wordle Game.
    def playWordle(self, play):
             
        def check_guess(answer, guess): 
            guesscode = ["", "", "", "", ""]
            
            if guess not in allwords:
                return print("That is not a valid word!")
            
            elif guess in allwords:   
                
                for x in range(len(guess)): 
                    
                    if guess[x] in answer: 
                        guesscode[x] = "Y"
                    
                    if answer[x] == guess[x]: 
                        guesscode[x] = "G" 
                    
                    if guess[x] not in answer: 
                        guesscode[x] = "B"
                             
                return guesscode
            
        def split(guess):
            return list(guess)
        
        result = dict(zip(split(guess), check_guess(answer, guess)))
                
        return result

    
    # Output the results from the simulation into a string that can be put into the later functions.
    def color_hints(self, colors):
        color_hints = []
        colorstr = ""
        for values in self.playWordle().values():
            color_hints.append(values)
        colorstr = colorstr.join(color_hints)    
        return colorstr    
    
    def solver1(self, solve1):
        
        # After getting feedback from a word, divide the letters into different lists to be processed later.
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
    
        # What to do with green letters (keep only in same place)
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
    
        # What to do with black letters (delete all)
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
    
        # What to do with yellow letters (delete, keep complementary set)
        def with_yellow(word_list: list, yellow_letter: list):
          if len(yellow_letter) > 0:
            possible_words = []
            for w in word_list:
              if all([l in w for l, idx in yellow_letter]) and all([w.index(l) != idx for l, idx in yellow_letter]):
                    possible_words.append(w)
            return list(set(possible_words))
          else:
            return word_list
    
        # Function for the all-green correct word.
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
        
        # Using the generated hints from earlier...
        while True:
          guessed = guess
          result = self.color_hints()
        
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
          
f = GAME()
f.solver1()
