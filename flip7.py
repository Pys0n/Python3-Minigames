import random, os

CLEAR = 'cls' if os.name == 'nt' else 'clear'

class Flip7:
    def __init__(self, playercount: int = 3) -> None:
        self.cards_remaining = self.load_all_cards()
        self.used_cards = []    # cards from previous rounds and cards from busted players
        self.players = {}
        for player in range(1, playercount+1):
            self.players[str(player)] = [[], [], False] # cards, bonus cards, has second chance

    
    def load_all_cards(self) -> list:
        # create cards list (bonus cards already included)
        cards = ['x2', '+2', '+4', '+6', '+8', '+10']

        # add all number cards
        for i in range(13):
            if i == 0: cards.append(str(i))

            for number in range(i):
                cards.append(str(i))

        # add action cards
        actions = ['Freeze', 'Second Chance', 'Flip Three']
        for action in actions:
            for _ in range(3):
                cards.append(action)

        # shuffle all cards
        random.shuffle(cards)

        return cards
    

    def reset_players(self) -> None:
        for player in self.players:
            cards = self.players[player]

            self.used_cards.extend(cards[0])
            self.used_cards.extend(cards[1])
            if cards[2]:
                self.used_cards.append('Second Chance')

            self.players[player] = [[], [], False]
    

    def reset_card_deck(self) -> None:
        self.cards_remaining = self.load_all_cards()
        self.used_cards = []

    
    def action_card(self, player: str, not_finished: list, card: str) -> None:
        choose_from = []
        for p in self.players:
            if p in not_finished:
                choose_from.append(p)
        
        while True:
            choice = input('Choose a player by typing the players number!\nChoose from ' + ', '.join(choose_from) + ': ')
            if choice in choose_from:
                if card == 'Freeze':
                    not_finished.remove(choice)
                else:
                    new_action_cards = []
                    for _ in range(3):
                        card = self.cards_remaining[0]
                        self.used_cards.append(card)
                        self.cards_remaining.pop(0)

                        print('You get', card)
                        input()

                        if card in self.players[choice][0]:
                            if self.players[choice][2]:
                                print('Duplicate! You lose your second chance!')
                                input()
                                self.players[choice][2] = False
                            else:
                                print('Duplicate! You lose!')
                                input()
                                self.players[choice] = [[], [], False]
                                not_finished.remove(player)
                                return
                        else:
                            if '+' in card or 'x' in card:
                                self.players[choice].append(card)
                            elif card in ['Freeze', 'Flip Three']:
                                new_action_cards.append(card)
                            elif card == 'Second Chance':
                                if not self.players[player][2]:
                                    self.players[player][2] = True
                                else:                               # player has a second chance card
                                    choose_from = []
                                    for p in flip7.players:
                                        if p not in not_finished: continue
                                        if not flip7.players[p][2]: choose_from.append(p)
                                    
                                    if len(choose_from) == 0:
                                        print('Nobody gets the card!')
                                        input()
                                    else:
                                        while True:
                                            choice = input('Choose a player by typing the players number!\nChoose from ' + ', '.join(choose_from) + ': ')
                                            if choice in choose_from:
                                                flip7.players[choice][2] = True
                                                break
                            else:
                                self.players[choice][0].append(card)
                    
                    for action_card in new_action_cards:
                        self.action_card(choice, not_finished, action_card)
                break


os.system(CLEAR)

players = int(input('Enter number of players: '))

flip7 = Flip7(players)
while True:
    os.system(CLEAR)

    print(len(flip7.cards_remaining), flip7.cards_remaining)

    points = [0 for _ in range(len(flip7.players))]
    round_ = 0
    while True:
        won = None
        os.system(CLEAR)
        round_ += 1
        print('Round: ', round_)
        print('Points: ')
        for i, value in enumerate(points):
            print('  Player', str(i+1) + ':', value)

        input()
    
        not_finished = [str(num+1) for num in range(len(flip7.players))]

        for _ in range((round_-1)%len(not_finished)):
            not_finished.append(not_finished[0])
            not_finished.pop(0)

        # Round
        flip7.reset_players()

        while len(not_finished) != 0:
            for player in not_finished:
                os.system(CLEAR)
                for player_txt in flip7.players:
                    print('Player ' + player_txt + ': Cards:', ', '.join(flip7.players[player_txt][0]), '| Bonus Cards:', ', '.join(flip7.players[player_txt][1]), ('| Second Chance' if flip7.players[player_txt][2] else ''))
                
                print('\nPlayer', player, 'turn!')
                action = input('[T]ake a card/[F]inish: ')

                if action.lower() == 'f':   # finish
                    not_finished.remove(player)
                    continue
                else:                       # take card
                    card = flip7.cards_remaining[0]
                    flip7.used_cards.append(card)
                    flip7.cards_remaining.pop(0)

                    if len(flip7.cards_remaining) == 0:
                        flip7.reset_card_deck()

                    print('You get', card)

                    if card in ['Freeze', 'Flip Three']:    # action cards (except second chance)
                        flip7.action_card(player, not_finished, card)
                        continue
                    elif card == 'Second Chance':           # second chance action card
                        if not flip7.players[player][2]:    # player don't has a second chance card
                            flip7.players[player][2] = True
                        else:                               # player has a second chance card
                            choose_from = []
                            for p in flip7.players:
                                if p not in not_finished: continue
                                if not flip7.players[p][2]: choose_from.append(p)
                            
                            if len(choose_from) == 0:
                                print('Nobody gets the card!')
                                input()
                                continue
                            else:
                                while True:
                                    choice = input('Choose a player by typing the players number!\nChoose from ' + ', '.join(choose_from) + ': ')
                                    if choice in choose_from:
                                        flip7.players[choice][2] = True
                                        break
                                continue
                    elif '+' in card or 'x' in card:        # bonus cards
                        flip7.players[player][1].append(card)
                    else:                                   # (normal) cards
                        if card in flip7.players[player][0] and flip7.players[player][2]:
                            print('Duplicate! You lose your second chance!')
                            flip7.players[player][2] = False
                        elif card in flip7.players[player][0]:
                            print('Duplicate! You lose!')
                            flip7.players[player] = [[], [], False]
                            not_finished.remove(player)
                            input()
                            continue
                        else: flip7.players[player][0].append(card)
                input() 
            
            if len(flip7.players[player][0]) >= 7:
                not_finished = []
                won = player
                break
        
        # calculate points
        for player in flip7.players:
            value = sum([int(x) for x in flip7.players[player][0]])

            for _ in range(flip7.players[player][1].count('x2')):
                value *= 2
            
            for bonus in flip7.players[player][1]:
                if bonus[0] != '+': continue
                value += int(bonus)

            if player == won:
                value += 15
            
            points[int(player)-1] += value
        
        # check if someone won
        if max(points) >= 200:
            break

    if points.count(max(points)) > 1:
        print('The Winners are: ', end='')
        for i, value in enumerate(points):
            if value == max(points): print('Player', i+1, ';', end='')
        print()

        print('\nPoints: ')
        points.sort(reverse=True)
        for i, value in enumerate(points):
            print('  Player', str(i+1) + ':', value)
        break
    else:
        print('The Winner is: Player', points.index(max(points))+1)

        print('\nPoints: ')
        points.sort(reverse=True)
        for i, value in enumerate(points):
            print('  Player', str(i+1) + ':', value)
        break
