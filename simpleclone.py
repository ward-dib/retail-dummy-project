import random

with open('allwords.txt', 'r') as a:
    allwords = []
    allwords = a.read().split('","')
    
with open('answerwords.txt', 'r') as a:
    NYTwords = []
    NYTwords = a.read().split('","')
    
#answer = random.choice(NYTwords)
#print(answer)

answer = "stare"

#guess = random.choice(allwords)
#print(guess)

guess = "arose"
 
def playWordle():
          
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

print(playWordle())

def color_hints():
    color_hints = []
    colorstr = ""
    for values in playWordle().values():
        color_hints.append(values)
    colorstr = colorstr.join(color_hints)    
    return colorstr

print(color_hints())

