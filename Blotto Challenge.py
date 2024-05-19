'''
from Jane Street
Here are 10 castles, numbered 1, 2, 3, ... , 10, and worth 1, 2, 3, ... , 10 points respectively. You have 100 soldiers, which you can allocate between the castles however you wish. Your opponent also (independently) does the same. The number of soldiers on each castle is then compared, and for each castle, whoever has the most soldiers on that castle wins its points. Additionally, you lose 0.2 points for each "extra" soldier that you have, in excess of your opponent's army size, at each castle that you win. You still need to deploy all 100 soldiers. In the case of a tie, no one gets points for that castle.
'''



import random

def compare(list1,list2):
    sc1 = 0
    sc2 = 0
    for i in range(1,11):
        if list1[i-1]>list2[i-1]:
            sc1 += 10*i - 2 * list1[i-1] + list2[i-1]
        if list1[i-1]<list2[i-1]:
            sc2 += 10*i - 2 * list2[i-1] + list1[i-1]
    return sc1,sc2



class Player:
    def __init__(self,num_list):
        self.num_list = num_list    
        self.next = None
        self.score = 0

    def create_next(self,num_list):
        self.next = Player(num_list)

    def inh_player(self):
        result = [self.num_list[i] for i in range(10)]
        result[random.randint(0,9)] += 1
        while(1):
            k = random.randint(0,9)
            if result[k]:
                result[k] -= 1
                break
        return result

def get_scores(root):
    scores = []
    player = root.next
    while player:
        scores.append(player.score)
        player = player.next
    return scores

def clear_scores(root):
    player = root.next
    while player:
        player.score = 0
        player = player.next


def find_winner(root):
    score = 0
    player = root.next
    winner = player
    while player:
        if player.score > winner.score:
            winner = player
        player = player.next
    return winner.num_list

turn = 1000
num_of_players = 100
eliminate_num = 30
dumb_player = 50
smart_player = 150

d_root = Player([10]*10)
d_player = d_root
for i in range(dumb_player):
    spl = [0]+[random.randint(0,100) for _ in range(9)]+[100]
    spl.sort()
    d_player.create_next([spl[i+1]-spl[i] for i in range(10)])
    d_player = d_player.next

s_root = Player([10]*10)
s_player = s_root
for i in range(smart_player):
    spl = [0]+[random.randint(0,100) for _ in range(9)]+[100]
    spl.sort()
    s_player.create_next(sorted([spl[i+1]-spl[i] for i in range(10)]))
    s_player = s_player.next



root = Player([10]*10)
player = root


for i in range(num_of_players):
    player.create_next(player.inh_player())
    player = player.next


for t in range(turn):
    clear_scores(root)

    player1 = root.next
    player2 = player1.next
    while player1.next:
        while player2:
            sc1,sc2 = compare(player1.num_list,player2.num_list)
            player1.score += sc1
            player2.score += sc2

            player2 = player2.next
        player1 = player1.next
        player2 = player1.next
    
    player = root.next
    while player:
        player.score += random.random()
        d_player = d_root.next
        while d_player:
            player.score += compare(player.num_list,d_player.num_list)[0]
            d_player = d_player.next
        s_player = s_root.next
        while s_player:
            player.score += compare(player.num_list,s_player.num_list)[0]
            s_player = s_player.next
        player = player.next




    scores = get_scores(root)
    pass_line = sorted(scores)[eliminate_num]
    inherit_line = sorted(scores)[num_of_players-eliminate_num]

    print(t,find_winner(root),max(scores)/(num_of_players-1+dumb_player+smart_player)/10)


    player = root
    new_branch = Player([10]*10)
    new_player = new_branch
    while player.next:
        if player.next.score < pass_line:
            player.next = player.next.next
            continue
        elif player.next.score >= inherit_line:
            new_player.create_next(player.next.inh_player())
            new_player = new_player.next
        player =  player.next
    player.next = new_branch.next


    




