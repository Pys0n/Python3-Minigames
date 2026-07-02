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

    
    def get_guess_result(self, word: str) -> list[str]:
        global guessed_words

        if word not in guessed_words: return None

        word = word.upper()

        result = []
        
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
                
        return result


def choose_word(guessed_words, wordle):
    # find gray & green letters

    gray_letters = set()
    yellow_letters = {}
    green_letters = {}
    for word in guessed_words:
        result = wordle.get_guess_result(word)
        for i, res in enumerate(result):
            if res == 'green':
                if word[i].upper() not in green_letters:
                    green_letters[word[i].upper()] = [i]
                elif i not in green_letters[word[i].upper()]:
                    green_letters[word[i].upper()].append(i)
                
                if word[i].upper() in gray_letters: gray_letters.remove(word[i].upper())
            elif res == 'yellow':
                if word[i].upper() not in yellow_letters:
                    yellow_letters[word[i].upper()] = [i]
                else:
                    yellow_letters[word[i].upper()].append(i)

                if word[i].upper() in gray_letters: gray_letters.remove(word[i].upper())
            elif res == 'gray' and word[i].upper() not in yellow_letters and word[i].upper() not in green_letters:
                gray_letters.add(word[i].upper())
            
    # count all letters

    letters = {}
    for word in list(wordle.all_words):
        for letter in word:
            if letter.upper() in gray_letters:  letters[letter.upper()] = 0
            elif letter.upper() not in letters: letters[letter.upper()] = 1
            else:                               letters[letter.upper()] += 1
    
    # find most word with "good" letters
    # find words with green letters at the right spot
    # find words with yellow letters at different spots
            
    words = {}
    all_valid_words = []
    for word in list(wordle.all_words):
        score = 0
        scored_letters = []
        for letter in word:
            if letter.upper() not in scored_letters:
                score += letters[letter.upper()]
                scored_letters.append(letter.upper())
    
        invalid = False
        for green_letter in green_letters:
            for pos in green_letters[green_letter]:
                if word[pos] != green_letter:
                    invalid = True

        for yellow_letter in yellow_letters:
            for pos in yellow_letters[yellow_letter]:
                if word[pos] == yellow_letter:
                    invalid = True
            if yellow_letter not in word:
                invalid = True

        for gray_letter in gray_letters:
            if gray_letter in word:
                invalid = True

        if invalid: continue
        else: all_valid_words.append(word)

        if score in words:
            words[score].append(word)
        else:
            words[score] = [word]

    best_words = words[max(words.keys())]

    # if count of remaining valid words low enough, return best word 
    if len(all_valid_words) <= wordle.tries or wordle.tries > 3 or wordle.tries == 1:
        return random.choice(best_words)

    letters_to_test = {}
    for word in all_valid_words:
        for letter in word:
            if letter not in gray_letters and letter not in list(yellow_letters.keys()) + list(green_letters.keys()):
                if letter not in letters_to_test:
                    letters_to_test[letter] = 1
                else:
                    letters_to_test[letter] += 1
    
    # find best word

    words = {}
    for word in list(wordle.all_words):
        score = 0
        tested_letters = []
        for letter in word:
            if letter in letters_to_test and letter not in tested_letters:
                score += letters_to_test[letter]
                tested_letters.append(letter)
        if score not in words:
            words[score] = [word]
        else:
            words[score].append(word)

    best_words = words[max(words.keys())]
    
    return random.choice(best_words)


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