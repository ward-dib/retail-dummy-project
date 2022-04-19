import random

with open("allwords.txt", "r") as file:
   allwords = eval(file.readline())

#answer = random.choice(allwords)
#print(answer)

answer = "stare"

#guess = random.choice(allwords)
#print(guess)

guess = "arise"
 
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

