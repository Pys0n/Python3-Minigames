import random, collections, os

CLEAR = 'cls' if os.name == 'nt' else 'clear'

class Wordle:
    def __init__(self, tries: int = 6) -> None:
        self.all_words = self.load_words()
        self.word = 'AGLEE'
        self.tries = tries

    
    def load_words(self) -> set:
        words = set()

        with open('valid-wordle-words.txt', 'r', encoding='utf-8') as file:
            for line in file.readlines():
                words.add(line.strip().upper())
        
        return words

    
    def guess(self, word: str) -> tuple[bool, str]:
        word = word.upper()

        result = ''
        
        if word != self.word:
            letters_in_guess = {}

            for letter in word:
                if letter in letters_in_guess:
                    letters_in_guess[letter] += 1
                else:
                    letters_in_guess[letter] = 1
    
            for pos, letter in enumerate(word):                    
                if letter not in self.word:
                    result += letter
                elif self.word[pos] == letter:
                    result += f'\033[42m{letter}\033[0m'
                else:
                    if word.count(letter) > self.word.count(letter):
                        count_right = 0

                        for i, l in enumerate(word):
                            if self.word[i] == l:
                                count_right += 1

                        if self.word.count(letter) + count_right <= letters_in_guess[letter]:
                            result += f'\033[43m{letter}\033[0m'
                            letters_in_guess[letter] -= 1
                        else:
                            result += letter

                    elif self.word.count(letter) >= letters_in_guess[letter]:
                        result += f'\033[43m{letter}\033[0m'
                        letters_in_guess[letter] -= 1
                    else:
                        result += letter
            
            self.tries -= 1
            
            return (False, result)
        else:
            return (True, f'\033[42m{word}\033[0m')


guessed = False
guesses = []
wordle = Wordle()
while wordle.tries > 0:
    os.system(CLEAR)
    for i in range(wordle.tries + len(guesses)):
        if i < len(guesses):
            print(guesses[i])
        else:
            print('_____')
    
    guess = input('\nYour Guess: ').upper()

    if guess in wordle.all_words:
        result = wordle.guess(guess)

        guesses.append(result[1])

        if result[0]:
            guessed = True
            break
    else:
        input('Word not in list! Press <Enter> to continue...')

os.system(CLEAR)

for guess in guesses:
    print(guess)

if not guessed: print('\nSolution: ' + wordle.word)