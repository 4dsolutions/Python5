"""
Adapted from hangman.py by Al Sweigart
https://inventwithpython.com/chapter9.html

* add case sensitivity
* allow spaces
* use a class
"""

import random

HANGMANPICS = ['''



  +---+

  |   |

      |

      |

      |

      |

=========''', '''



  +---+

  |   |

  O   |

      |

      |

      |

=========''', '''



  +---+

  |   |

  O   |

  |   |

      |

      |

=========''', '''



  +---+

  |   |

  O   |

 /|   |

      |

      |

=========''', '''



  +---+

  |   |

  O   |

 /|\  |

      |

      |

=========''', '''



  +---+

  |   |

  O   |

 /|\  |

 /    |

      |

=========''', '''



  +---+

  |   |

  O   |

 /|\  |

 / \  |

      |

=========''']

class Hangman:
    
    def __init__(self, words):
        self.words = words
        self.secretWord = random.choice(self.words)
        self.missedLetters = ''
        self.correctLetters = ''
        self.alreadyGuessed = ''
   
    def __str__(self):  # print(hm) triggers this method
        display = ("\n"
        "H A N G M A N \n"
        "{picture}\n" 
        "Guessed: {blanks}\n"
        " Missed: {missed}\n")
        
        content = {}
        content['picture'] = HANGMANPICS[len(self.missedLetters)] 
        content['missed']  = ""
        for letter in self.missedLetters:
            content['missed'] += letter + " "
    
        blanks = list('_' * len(self.secretWord))
        for i in range(len(self.secretWord)):  # replace blanks
            if self.secretWord[i] in self.correctLetters:
                blanks[i] = self.secretWord[i]
        blanks = "".join(blanks)
        
        content["blanks"] = ""
        for letter in blanks:  # masked secret word 
            content['blanks'] += letter + " "  # spaces between each letter
        
        return display.format(**content) # keyword arguments to format()

    def getGuess(self):
        """
        Accept a letter (case sensitive) or space
        """
        while True:
            guess = input("Guess a letter (or 'exit'): ")
            if guess == 'exit':
                break
            elif len(guess) != 1:
                print('Please enter a single letter or space.')
            elif guess in self.alreadyGuessed:
                print('You have already guessed that letter. Choose again.')
            elif not guess.isalpha() and not guess == " ":
                print('Please enter a LETTER or SPACE.')
            else:
                break

        return guess

def playAgain():
    """
    This function returns True if the player wants to 
    play again, otherwise it returns False.
    """
    return input('Do you want to play again? (yes or no) ').lower().startswith('y')

words = 'Big Data : HTML : CSS : Anaconda : Python : JavaScript'.split(" : ")

hm = Hangman(words)

gameIsDone = False

while not gameIsDone:
    
    print(hm)
    # Let the player type in a letter.
    guess = hm.getGuess()

    if guess == 'exit':
        print("Thanks for playing")
        break

    if guess in hm.secretWord:
        hm.correctLetters += guess
        hm.alreadyGuessed += guess

        # Check if the player has won
        foundAllLetters = True
        for i in range(len(hm.secretWord)):
            if hm.secretWord[i] not in hm.correctLetters:
                foundAllLetters = False
                continue

        if foundAllLetters:
            print(hm)
            print('Yes! The secret word is "{}"! '
            'You have won!'.format(hm.secretWord))
            gameIsDone = True

    else:
        
        hm.missedLetters += guess
        hm.alreadyGuessed += guess
        
        # Check if player has guessed too many times and lost
        if len(hm.missedLetters) == len(HANGMANPICS) - 1:
            print(hm)
            print('You have run out of guesses!\n'
                  + 'After {}'.format(len(hm.missedLetters))
                  + ' missed guesses and {}'.format(len(hm.correctLetters))
                  + ' correct guesses, the word was "{}"'.format(hm.secretWord))
            gameIsDone = True

    # Ask the player if they want to play again (but only if the game is done).
    if gameIsDone:
        if playAgain():
           hm = Hangman(words)
           gameIsDone = False
        else:
           break