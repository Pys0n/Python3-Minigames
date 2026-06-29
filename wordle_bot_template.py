import random, collections, os

CLEAR = 'cls' if os.name == 'nt' else 'clear'

class Wordle:
    def __init__(self, tries: int = 6) -> None:
        self.all_words = self.load_words()
        self._word = random.choice(list(self.all_words))
        self.tries = tries

    
    def load_words(self) -> set:
        words = set()

        with open('valid-wordle-words.txt', 'r', encoding='utf-8') as file:
            for line in file.readlines():
                words.add(line.strip().upper())
        
        return words

    
    def guess(self, word: str) -> tuple[bool, str]:
        word = word.upper()

        letters = set(list(self._word))
        result = ''
        
        if word != self._word:
            letters_in_guess = {}
    
            for pos, letter in enumerate(word):
                if letter in letters_in_guess:
                    letters_in_guess[letter] += 1
                else:
                    letters_in_guess[letter] = 1
                    
                if letter not in self._word:
                    result += letter
                elif self._word[pos] == letter:
                    result += f'\033[42m{letter}\033[0m'
                else:
                    if word.count(letter) > self._word.count(letter):
                        count_right = 0

                        for i, l in enumerate(word):
                            if self._word[i] == l:
                                count_right += 1

                        if self._word.count(letter) - count_right - letters_in_guess[letter] >= 0:
                            result += f'\033[43m{letter}\033[0m'
                        else:
                            result += letter

                    elif self._word.count(letter) >= letters_in_guess[letter]:
                        result += f'\033[43m{letter}\033[0m'
                    else:
                        result += letter
            
            self.tries -= 1
            
            return (False, result)
        else:
            return (True, f'\033[42m{word}\033[0m')

    
    def get_guess_result(self, word: str) -> list[str]:
        global guessed_words

        if word not in guessed_words: return None

        word = word.upper()

        letters = set(list(self._word))
        result = []
        
        if word != self._word:
            letters_in_guess = {}
    
            for pos, letter in enumerate(word):
                if letter in letters_in_guess:
                    letters_in_guess[letter] += 1
                else:
                    letters_in_guess[letter] = 1
                    
                if letter not in self._word:
                    result.append('gray')
                elif self._word[pos] == letter:
                    result.append('green')
                else:
                    if word.count(letter) > self._word.count(letter):
                        count_right = 0

                        for i, l in enumerate(word):
                            if self._word[i] == l:
                                count_right += 1

                        if self._word.count(letter) - count_right - letters_in_guess[letter] >= 0:
                            result.append('yellow')
                        else:
                            result.append('gray')

                    elif self._word.count(letter) >= letters_in_guess[letter]:
                        result.append('yellow')
                    else:
                        result.append('gray')
            
            self.tries -= 1
            
            return (False, result)
        else:
            return (True, f'\033[42m{word}\033[0m')


def choose_word(guessed_words, wordle):
    word = input()

    if len(guessed_words) > 0: input(wordle.get_guess_result(guessed_words[-1]))

    # here comes your code

    # Rules:
    # do not use ...
    # ... wordle._word
    # ... wordle.load_words()
    # ... wordle.guess()

    return word


guessed = False
guesses = []
guessed_words = []
wordle = Wordle()
while wordle.tries > 0:
    os.system(CLEAR)
    for i in range(wordle.tries + len(guesses)):
        if i < len(guesses):
            print(guesses[i])
        else:
            print('_____')
    
    guess = choose_word(guessed_words, wordle).upper()

    if guess in wordle.all_words:
        result = wordle.guess(guess)

        guesses.append(result[1])
        guessed_words.append(guess)

        if result[0]:
            guessed = True
            break
    else:
        input('Word not in list! Press <Enter> to continue...')

os.system(CLEAR)

for guess in guesses:
    print(guess)

if not guessed: print('\nSolution: ' + wordle._word)