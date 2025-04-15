import pygame
import sys
from pygame.locals import *
from os import path
import copy


cur_path = path.dirname(__file__)
img_path = path.join(cur_path, 'images')

pygame.init()
screen=pygame.display.set_mode((450,550))
pygame.display.set_caption('Chinese Chess')

img_board=pygame.image.load(path.join(img_path, 'board.png'))
img_redSoldier=pygame.image.load(path.join(img_path, 'bing.png'))
img_redCannon=pygame.image.load(path.join(img_path, 'hongpao.png'))
img_redCar=pygame.image.load(path.join(img_path, 'hongju.png'))
img_redHorse=pygame.image.load(path.join(img_path, 'hongma.png'))
img_redElephant=pygame.image.load(path.join(img_path, 'hongxiang.png'))
img_redAttendant=pygame.image.load(path.join(img_path, 'hongshi.png'))
img_chief=pygame.image.load(path.join(img_path, 'shuai.png'))
img_blackSoldier=pygame.image.load(path.join(img_path, 'zu.png'))
img_blackCannon=pygame.image.load(path.join(img_path, 'heipao.png'))
img_blackCar=pygame.image.load(path.join(img_path, 'heiju.png'))
img_blackHorse=pygame.image.load(path.join(img_path, 'heima.png'))
img_blackElephant=pygame.image.load(path.join(img_path, 'heixiang.png'))
img_blackAttendant=pygame.image.load(path.join(img_path, 'heishi.png'))
img_general=pygame.image.load(path.join(img_path, 'jiang.png'))

screen.blit(img_board, (0, 0))
pygame.display.update()

red_chess = [[0, 6], [2, 6], [4, 6], [6, 6], [8, 6], [1, 7], [7, 7], [0, 9], [1, 9], [2, 9], [3, 9], [4, 9], [5, 9],
             [6, 9], [7, 9], [8, 9]]
black_chess = [[0, 3], [2, 3], [4, 3], [6, 3], [8, 3], [1, 2], [7, 2], [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0],
               [6, 0], [7, 0], [8, 0]]



# Mapping chess index to piece type
red_piece_names = {
    0: 'soldier', 1: 'soldier', 2: 'soldier', 3: 'soldier', 4: 'soldier',
    5: 'cannon', 6: 'cannon',
    7: 'car', 8: 'horse', 9: 'elephant', 10: 'attendant',
    11: 'general', 12: 'attendant', 13: 'elephant', 14: 'horse', 15: 'car'
}

black_piece_names = {
    0: 'soldier', 1: 'soldier', 2: 'soldier', 3: 'soldier', 4: 'soldier',
    5: 'cannon', 6: 'cannon',
    7: 'car', 8: 'horse', 9: 'elephant', 10: 'attendant',
    11: 'general', 12: 'attendant', 13: 'elephant', 14: 'horse', 15: 'car'
}


def evaluate_board(red_chess, black_chess):
    piece_values = {
        'soldier': 10, 'cannon': 35, 'car': 50,
        'horse': 30, 'elephant': 25, 'attendant': 20,
        'general': 1000
    }

    score = 0
    for i in range(len(red_chess)):
        if red_chess[i] != [-1, -1]:
            piece = red_piece_names[i]
            score += piece_values[piece]
    for i in range(len(black_chess)):
        if black_chess[i] != [-1, -1]:
            piece = black_piece_names[i]
            score -= piece_values[piece]
    return score  # higher is better for red



def get_all_moves(chess1, chess2, is_red):
    all_moves = []
    for i in range(len(chess1)):
        if chess1[i] == [-1, -1]:
            continue
        piece = red_piece_names[i] if is_red else black_piece_names[i]
        for x in range(9):
            for y in range(10):
                dest = [x, y]
                move_result = None
                try:
                    if piece == 'soldier':
                        move_result = soldier_rule(chess1, chess2, chess1[i][:], dest)
                    elif piece == 'car':
                        move_result = car_rule(chess1, chess2, chess1[i][:], dest)
                    elif piece == 'cannon':
                        move_result = cannon_rule(chess1, chess2, chess1[i][:], dest)
                    elif piece == 'horse':
                        move_result = horse_rule(chess2, chess1[i][:], dest)
                    elif piece == 'elephant':
                        move_result = elephant_rule(chess2, chess1[i][:], dest)
                    elif piece == 'attendant':
                        move_result = attendant_rule(chess1, chess2, chess1[i][:], dest)
                    elif piece == 'general':
                        move_result = boss_rule(chess1, chess2, chess1[i][:], dest, chess2[11])
                except:
                    continue
                if move_result and move_result != 0:
                    all_moves.append((i, dest))  # (piece index, new position)
    return all_moves

def simulate_move(chess1, chess2, move):
    i, dest = move
    chess1_copy = copy.deepcopy(chess1)
    chess2_copy = copy.deepcopy(chess2)

    piece = red_piece_names[i] if chess1 is red_chess else black_piece_names[i]
    
    if piece == 'soldier':
        result = soldier_rule(chess1_copy, chess2_copy, chess1_copy[i], dest)
    elif piece == 'car':
        result = car_rule(chess1_copy, chess2_copy, chess1_copy[i], dest)
    elif piece == 'cannon':
        result = cannon_rule(chess1_copy, chess2_copy, chess1_copy[i], dest)
    elif piece == 'horse':
        result = horse_rule(chess2_copy, chess1_copy[i], dest)
    elif piece == 'elephant':
        result = elephant_rule(chess2_copy, chess1_copy[i], dest)
    elif piece == 'attendant':
        result = attendant_rule(chess1_copy, chess2_copy, chess1_copy[i], dest)
    elif piece == 'general':
        result = boss_rule(chess1_copy, chess2_copy, chess1_copy[i], dest, chess2_copy[11])
    
    if result and result != 0:
        chess1_copy[i] = result[0]
    return chess1_copy, chess2_copy


def minimax(depth, is_maximizing, red, black):
    if depth == 0:
        return evaluate_board(red, black)

    if is_maximizing:
        max_eval = float('-inf')
        moves = get_all_moves(red, black, is_red=True)
        for move in moves:
            new_red, new_black = simulate_move(red, black, move)
            eval = minimax(depth - 1, False, new_red, new_black)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        moves = get_all_moves(black, red, is_red=False)
        for move in moves:
            new_black, new_red = simulate_move(black, red, move)
            eval = minimax(depth - 1, True, new_red, new_black)
            min_eval = min(min_eval, eval)
        return min_eval
def find_best_move(red, black, depth=2):
    best_score = float('-inf')
    best_move = None
    for index, move in enumerate(get_all_moves(red, black, is_red=True)):
        new_red, new_black = simulate_move(red, black, move)
        score = minimax(depth - 1, False, new_red, new_black)
        if score > best_score:
            best_score = score
            best_move = move
            best_index = index  # Save the piece's index
    if best_move:
        print(f"AI chose move: piece {best_index} -> {best_move[1]}")
    return best_move



# Draw the Chess pieces on the board
def draw_chess():
    for i in range(len(red_chess)):
        if 0 <= i <= 4:
            screen.blit(img_redSoldier, (red_chess[i][0] * 50, red_chess[i][1] * 50))
        elif 5 <= i <= 6:
            screen.blit(img_redCannon, (red_chess[i][0] * 50, red_chess[i][1] * 50))
        elif i == 7 or i == 15:
            screen.blit(img_redCar, (red_chess[i][0] * 50, red_chess[i][1] * 50))
        elif i == 8 or i == 14:
            screen.blit(img_redHorse, (red_chess[i][0] * 50, red_chess[i][1] * 50))
        elif i == 9 or i == 13:
            screen.blit(img_redElephant, (red_chess[i][0] * 50, red_chess[i][1] * 50))
        elif i == 10 or i == 12:
            screen.blit(img_redAttendant, (red_chess[i][0] * 50, red_chess[i][1] * 50))
        else:
            screen.blit(img_chief, (red_chess[i][0] * 50, red_chess[i][1] * 50))
    for i in range(len(black_chess)):
        if 0 <= i <= 4:
            screen.blit(img_blackSoldier, (black_chess[i][0] * 50, black_chess[i][1] * 50))
        elif 5 <= i <= 6:
            screen.blit(img_blackCannon, (black_chess[i][0] * 50, black_chess[i][1] * 50))
        elif i == 7 or i == 15:
            screen.blit(img_blackCar, (black_chess[i][0] * 50, black_chess[i][1] * 50))
        elif i == 8 or i == 14:
            screen.blit(img_blackHorse, (black_chess[i][0] * 50, black_chess[i][1] * 50))
        elif i == 9 or i == 13:
            screen.blit(img_blackElephant, (black_chess[i][0] * 50, black_chess[i][1] * 50))
        elif i == 10 or i == 12:
            screen.blit(img_blackAttendant, (black_chess[i][0] * 50, black_chess[i][1] * 50))
        else:
            screen.blit(img_general, (black_chess[i][0] * 50, black_chess[i][1] * 50))
    pygame.display.update()


# Return 1 for normal movement, return 2 for captured pieces, return 0 for rejection of movement
# Rules for pawn movement, red pawn chess1 is red_chess, chess2 is black_chess
def soldier_rule(chess1, chess2, current_pos, next_pos):
    if chess1 == red_chess:
        pos, index = [5, 6], 1
    elif chess1 == black_chess:
        pos, index = [3, 4], -1
    if current_pos[1] in pos:
        if current_pos[0] == next_pos[0] and current_pos[1] == next_pos[1] + index and next_pos not in chess1:
            for i in range(len(chess2)):
                if chess2[i] == next_pos:
                    chess2[i] = [-1, -1]
                    current_pos = next_pos
                    return [current_pos, 2, i]
            current_pos = next_pos
            return [current_pos, 1]
    else:
        if current_pos[0] == next_pos[0] and current_pos[1] == next_pos[1] + index and next_pos not in chess1:
            for i in range(len(chess2)):
                if chess2[i] == next_pos:
                    chess2[i] = [-1, -1]
                    current_pos = next_pos
                    return [current_pos, 2, i]
            current_pos = next_pos
            return [current_pos, 1]
        elif current_pos[1] == next_pos[1] and current_pos[0] + 1 == next_pos[0] and next_pos not in chess1:
            for i in range(len(chess2)):
                if chess2[i] == next_pos:
                    chess2[i] = [-1, -1]
                    current_pos = next_pos
                    return [current_pos, 2, i]
            current_pos = next_pos
            return [current_pos, 1]
        elif current_pos[1] == next_pos[1] and current_pos[0] - 1 == next_pos[0] and next_pos not in chess1:
            for i in range(len(chess2)):
                if chess2[i] == next_pos:
                    chess2[i] = [-1, -1]
                    current_pos = next_pos
                    return [current_pos, 2, i]
            current_pos = next_pos
            return [current_pos, 1]


# Rook movement rules, the first two parameters of the red rook are red_chess and black_chess, 
# and the first two parameters of the black rook are black_chess and red_chess
def car_rule(chess1, chess2, current_pos, next_pos):
    if next_pos not in chess1 and current_pos[0] == next_pos[0]:
        a, b = current_pos, next_pos
        if a[1] > b[1]:
            a, b = b, a
        for i in range(a[1] + 1, b[1]):
            if [a[0], i] in black_chess + red_chess:
                return 0
        for i in range(len(chess2)):
            if chess2[i] == next_pos:
                chess2[i] = [-1, -1]
                current_pos = next_pos
                return [current_pos, 2, i]
        current_pos = next_pos
        return [current_pos, 1]
    elif next_pos not in chess1 and current_pos[1] == next_pos[1]:
        a, b = current_pos, next_pos
        if a[0] > b[0]:
            a, b = b, a
        for i in range(a[0] + 1, b[0]):
            if [i, a[1]] in black_chess + red_chess:
                return 0
        for i in range(len(chess2)):
            if chess2[i] == next_pos:
                chess2[i] = [-1, -1]
                current_pos = next_pos
                return [current_pos, 2, i]
        current_pos = next_pos
        return [current_pos, 1]


# Cannon Movement Rules
def cannon_rule(chess1, chess2, current_pos, next_pos):
    print('chess1:',chess1)
    print('chess2:',chess2)
    print('current_pos:',current_pos)
    print('next_pos:',next_pos)
    if next_pos not in chess1 and current_pos[0] == next_pos[0]:
        num = 0
        a, b = current_pos, next_pos
        if a[1] > b[1]:
            a, b = b, a
        for i in range(a[1] + 1, b[1]):
            if [a[0], i] in black_chess + red_chess:
                num += 1
        if num == 1:
            for i in range(len(chess2)):
                if chess2[i] == next_pos:
                    chess2[i] = [-1, -1]
                    current_pos = next_pos
                    return [current_pos, 2, i]
            return 0
        elif num == 0 and next_pos not in chess2:
            current_pos = next_pos
            return [current_pos, 1]
        else:
            return 0
    elif next_pos not in chess1 and current_pos[1] == next_pos[1]:
        num = 0
        a, b = current_pos, next_pos
        if a[0] > b[0]:
            a, b = b, a
        for i in range(a[0] + 1, b[0]):
            if [i, a[1]] in black_chess + red_chess:
                num += 1
        if num == 1:
            for i in range(len(chess2)):
                if chess2[i] == next_pos:
                    chess2[i] = [-1, -1]
                    current_pos = next_pos
                    return [current_pos, 2, i]
            return 0
        elif num == 0 and next_pos not in chess2:
            current_pos = next_pos
            return [current_pos, 1]
        else:
            return 0


# Horse movement rules, red horse chess is black_chess
def horse_rule(chess, current_pos, next_pos):
    index = [[2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2], [1, 2], [2, 1]]
    leg = [[1, 0], [0, -1], [0, -1], [-1, 0], [-1, 0], [0, 1], [0, 1], [1, 0]]
    if next_pos not in red_chess + black_chess:
        for i in range(len(index)):
            if current_pos[0] + index[i][0] == next_pos[0] and current_pos[1] + index[i][1] == next_pos[1]:
                if [current_pos[0] + leg[i][0], current_pos[1] + leg[i][1]] not in black_chess + red_chess:
                    current_pos = next_pos
                    return [current_pos, 1]
    elif next_pos in chess:
        for i in range(len(index)):
            if current_pos[0] + index[i][0] == next_pos[0] and current_pos[1] + index[i][1] == next_pos[1]:
                if [current_pos[0] + leg[i][0], current_pos[1] + leg[i][1]] not in black_chess + red_chess:
                    for i in range(len(chess)):
                        if chess[i] == next_pos:
                            chess[i] = [-1, -1]
                            current_pos = next_pos
                            return [current_pos, 2, i]


# elephant movement rules, red elephant chess is black_chess
def elephant_rule(chess, current_pos, next_pos):
    index = [[2, -2], [-2, -2], [-2, 2], [2, 2]]
    leg = [[1, -1], [-1, -1], [-1, 1], [1, 1]]
    if chess == black_chess:
        pos = [5, 7, 9]
    elif chess == red_chess:
        pos = [0, 2, 4]
    if next_pos not in red_chess + black_chess and next_pos[1] in pos:
        for i in range(len(index)):
            if current_pos[0] + index[i][0] == next_pos[0] and current_pos[1] + index[i][1] == next_pos[1]:
                if [current_pos[0] + leg[i][0], current_pos[1] + leg[i][1]] not in black_chess + red_chess:
                    current_pos = next_pos
                    return [current_pos, 1]
    elif next_pos in chess and next_pos[1] in pos:
        for i in range(len(index)):
            if current_pos[0] + index[i][0] == next_pos[0] and current_pos[1] + index[i][1] == next_pos[1]:
                if [current_pos[0] + leg[i][0], current_pos[1] + leg[i][1]] not in black_chess + red_chess:
                    for i in range(len(chess)):
                        if chess[i] == next_pos:
                            chess[i] = [-1, -1]
                            current_pos = next_pos
                            return [current_pos, 2, i]


# Attendant movement rules, red attendant chess is black_chess
def attendant_rule(chess1, chess2, current_pos, next_pos):
    if chess1 == red_chess:
        pos1 = [[3, 9], [3, 7], [5, 7], [5, 9]]
        pos2 = [4, 8]
    elif chess1 == black_chess:
        pos1 = [[3, 0], [3, 2], [5, 2], [5, 0]]
        pos2 = [4, 1]
    if current_pos in pos1 and next_pos == pos2 and next_pos not in chess1:
        if next_pos not in chess2:
            current_pos = next_pos
            return [current_pos, 1]
        else:
            for i in range(len(chess2)):
                if chess2[i] == next_pos:
                    chess2[i] = [-1, -1]
                    current_pos = next_pos
                    return [current_pos, 2, i]
    elif current_pos == pos2 and next_pos in pos1 and next_pos not in chess1:
        if next_pos not in chess2:
            current_pos = next_pos
            return [current_pos, 1]
        else:
            for i in range(len(chess2)):
                if chess2[i] == next_pos:
                    chess2[i] = [-1, -1]
                    current_pos = next_pos
                    return [current_pos, 2, i]


#  Boss movement rules, red boss chess is black_chess
def boss_rule(chess1, chess2, current_pos, next_pos, j_pos):
    if chess1 == red_chess:
        pos = [7, 8, 9]
    elif chess1 == black_chess:
        pos = [0, 1, 2]
    flag = 0
    if next_pos not in chess1:
        if next_pos[0] == j_pos[0]:
            a, b = j_pos, next_pos
            if a[1] > b[1]:
                a, b = b, a
            for i in range(a[1] + 1, b[1]):
                if [a[0], i] in black_chess + red_chess:
                    flag = 1
                    break
            if flag == 0:
                return 0
    if next_pos not in chess1 and 3 <= next_pos[0] <= 5 and next_pos[1] in pos:
        if next_pos not in chess2:
            if current_pos[0] == next_pos[0]:
                if current_pos[1] + 1 == next_pos[1] or current_pos[1] - 1 == next_pos[1]:
                    current_pos = next_pos
                    return [current_pos, 1]
            elif current_pos[1] == next_pos[1]:
                if current_pos[0] + 1 == next_pos[0] or current_pos[0] - 1 == next_pos[0]:
                    current_pos = next_pos
                    return [current_pos, 1]
        else:
            if current_pos[0] == next_pos[0]:
                if current_pos[1] + 1 == next_pos[1] or current_pos[1] - 1 == next_pos[1]:
                    for i in range(len(chess2)):
                        if chess2[i] == next_pos:
                            chess2[i] = [-1, -1]
                            current_pos = next_pos
                            return [current_pos, 2, i]
            elif current_pos[1] == next_pos[1]:
                if current_pos[0] + 1 == next_pos[0] or current_pos[0] - 1 == next_pos[0]:
                    for i in range(len(chess2)):
                        if chess2[i] == next_pos:
                            chess2[i] = [-1, -1]
                            current_pos = next_pos
                            return [current_pos, 2, i]


bj = 0


# Move function, chess1 is red_chess, chess2 is black_chess
def move(chess1, chess2, next_pos):
    x = 0
    global bj
    temp = []
    if i in range(5):  # Soldier
        x = soldier_rule(chess1, chess2, chess1[i], next_pos)
        if x is not None and x != 0:
            temp = chess1[i]
            chess1[i] = x[0]
            fl = check(chess2, chess1)  # Check if the move leads to checkmate
            if fl == 1:
                if x[1] == 2:
                    chess2[x[2]] = x[0]
                chess1[i] = temp
                draw_text("Checkmate", 225, 250, 15)
                return 2  # Move is not allowed because it would result in check
            else:
                bj = 0
                draw_text("           ", 225, 250, 15)
                screen.blit(img_board, (0, 0))
                draw_chess()
                return x  # Move is allowed because it does not result in check
    elif i == 5 or i == 6:  # Cannon
        x = cannon_rule(chess1, chess2, chess1[i], next_pos)
        if x is not None and x != 0:
            temp = chess1[i]
            chess1[i] = x[0]
            fl = check(chess2, chess1)
            if fl == 1:
                if x[1] == 2:
                    chess2[x[2]] = x[0]
                chess1[i] = temp
                draw_text("Still Checkmate", 225, 250, 15)
                return 2
            else:
                bj = 0
                draw_text("           ", 225, 250, 15)
                screen.blit(img_board, (0, 0))
                draw_chess()
                return x
    elif i == 7 or i == 15:  # Chariot (Rook)
        x = car_rule(chess1, chess2, chess1[i], next_pos)
        if x is not None and x != 0:
            temp = chess1[i]
            chess1[i] = x[0]
            fl = check(chess2, chess1)
            if fl == 1:
                if x[1] == 2:
                    chess2[x[2]] = x[0]
                chess1[i] = temp
                draw_text("Still Checkmate!", 225, 250, 15)
                return 2
            else:
                bj = 0
                draw_text("           ", 225, 250, 15)
                screen.blit(img_board, (0, 0))
                draw_chess()
                return x
    elif i == 8 or i == 14:  # Horse (Knight)
        x = horse_rule(chess2, chess1[i], next_pos)
        if x is not None and x != 0:
            temp = chess1[i]
            chess1[i] = x[0]
            fl = check(chess2, chess1)
            if fl == 1:
                if x[1] == 2:
                    chess2[x[2]] = x[0]
                chess1[i] = temp
                draw_text("Still Checkmate!", 225, 250, 15)
                return 2
            else:
                bj = 0
                draw_text("           ", 225, 250, 15)
                screen.blit(img_board, (0, 0))
                draw_chess()
                return x
    elif i == 9 or i == 13:  # Elephant (Bishop)
        x = elephant_rule(chess2, chess1[i], next_pos)
        if x is not None and x != 0:
            temp = chess1[i]
            chess1[i] = x[0]
            fl = check(chess2, chess1)
            if fl == 1:
                if x[1] == 2:
                    chess2[x[2]] = x[0]
                chess1[i] = temp
                draw_text("Still Checkmate!", 225, 250, 15)
                return 2
            else:
                bj = 0
                draw_text("           ", 225, 250, 15)
                screen.blit(img_board, (0, 0))
                draw_chess()
                return x
    elif i == 10 or i == 12:  # Advisor (Guard)
        x = attendant_rule(chess1, chess2, chess1[i], next_pos)
        if x is not None and x != 0:
            temp = chess1[i]
            chess1[i] = x[0]
            fl = check(chess2, chess1)
            if fl == 1:
                if x[1] == 2:
                    chess2[x[2]] = x[0]
                chess1[i] = temp
                draw_text("Still Checkmate!", 225, 250, 15)
                return 2
            else:
                bj = 0
                draw_text("           ", 225, 250, 15)
                screen.blit(img_board, (0, 0))
                draw_chess()
                return x
    else:  # General (King)
        x = boss_rule(chess1, chess2, chess1[i], next_pos, chess2[11])
        if x is not None and x != 0:
            temp = chess1[i]
            chess1[i] = x[0]
            fl = check(chess2, chess1)
            if fl == 1:
                if x[1] == 2:
                    chess2[x[2]] = x[0]
                chess1[i] = temp
                draw_text("Still Checkmate!", 225, 250, 15)
                return 2
            else:
                bj = 0
                draw_text("           ", 225, 250, 15)
                screen.blit(img_board, (0, 0))
                draw_chess()
                return x



# Check if the general (king) is under attack
def check(chess1, chess2):
    # Soldier checks General
    if chess1 == red_chess:
        for i in range(5):
            if chess1[i] != [-1, -1]:
                if chess1[i][0] == chess2[11][0] and chess1[i][1] - 1 == chess2[11][1]:
                    return 1
                elif chess1[i][1] == chess2[11][1] and (
                        chess1[i][0] + 1 == chess2[11][0] or chess1[i][0] - 1 == chess2[11][0]):
                    return 1
    elif chess1 == black_chess:
        for i in range(5):
            if chess1[i] != [-1, -1]:
                if chess1[i][0] == chess2[11][0] and chess1[i][1] + 1 == chess2[11][1]:
                    return 1
                elif chess1[i][1] == chess2[11][1] and (
                        chess1[i][0] + 1 == chess2[11][0] or chess1[i][0] - 1 == chess2[11][0]):
                    return 1

    # Cannon checks General
    num = 0
    for i in [5, 6]:
        if chess1[i] != [-1, -1]:
            # Forward
            if chess1[i][0] == chess2[11][0] and chess1[i][1] > chess2[11][1] + 1:
                for j in range(chess2[11][1] + 1, chess1[i][1]):
                    if [chess1[i][0], j] in chess1 + chess2:
                        num += 1
                if num == 1:
                    num = 0
                    return 1
                else:
                    num = 0
            # Backward
            elif chess1[i][0] == chess2[11][0] and chess1[i][1] < chess2[11][1] - 1:
                for j in range(chess1[i][1] + 1, chess2[11][1]):
                    if [chess1[i][0], j] in chess1 + chess2:
                        num += 1
                if num == 1:
                    num = 0
                    return 1
                else:
                    num = 0
            # Right
            elif chess1[i][1] == chess2[11][1] and chess1[i][0] > chess2[11][0] + 1:
                for j in range(chess2[11][0] + 1, chess1[i][0]):
                    if [j, chess1[i][1]] in chess1 + chess2:
                        num += 1
                if num == 1:
                    num = 0
                    return 1
                else:
                    num = 0
            # Left
            elif chess1[i][1] == chess2[11][1] and chess1[i][0] < chess2[11][0] - 1:
                for j in range(chess1[i][0] + 1, chess2[11][0]):
                    if [j, chess1[i][1]] in chess1 + chess2:
                        num += 1
                if num == 1:
                    num = 0
                    return 1
                else:
                    num = 0

    # Chariot (Rook) checks General
    for i in [7, 15]:
        if chess1[i] != [-1, -1]:
            # Forward
            if chess1[i][0] == chess2[11][0] and chess1[i][1] > chess2[11][1]:
                for j in range(chess2[11][1] + 1, chess1[i][1]):
                    if [chess1[i][0], j] in chess1 + chess2:
                        num += 1
                if num == 0:
                    return 1
                else:
                    num = 0
            # Backward
            elif chess1[i][0] == chess2[11][0] and chess1[i][1] < chess2[11][1]:
                for j in range(chess1[i][1] + 1, chess2[11][1]):
                    if [chess1[i][0], j] in chess1 + chess2:
                        num += 1
                if num == 0:
                    return 1
                else:
                    num = 0
            # Right
            elif chess1[i][1] == chess2[11][1] and chess1[i][0] > chess2[11][0]:
                for j in range(chess2[11][0] + 1, chess1[i][0]):
                    if [j, chess1[i][1]] in chess1 + chess2:
                        num += 1
                if num == 0:
                    return 1
                else:
                    num = 0
            # Left
            elif chess1[i][1] == chess2[11][1] and chess1[i][0] < chess2[11][0]:
                for j in range(chess1[i][0] + 1, chess2[11][0]):
                    if [j, chess1[i][1]] in chess1 + chess2:
                        num += 1
                if num == 0:
                    return 1
                else:
                    num = 0
        pass

    # Horse (Knight) checks General
    index = [[2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2], [1, 2], [2, 1]]
    leg = [[1, 0], [0, -1], [0, -1], [-1, 0], [-1, 0], [0, 1], [0, 1], [1, 0]]
    for i in [8, 14]:
        for j in range(len(index)):
            if chess1[i][0] + index[j][0] == chess2[11][0] and chess1[i][1] + index[j][1] == chess2[11][1]:
                if [chess1[i][0] + leg[j][0], chess1[i][1] + leg[j][1]] not in chess1 + chess2:
                    return 1



# Decisive move (game-winning move)
def chess_jam(chess1, chess2):
    all_pos = []
    for i in range(9):
        for j in range(10):
            all_pos.append([i, j])
    if bj == 0:
        return [1, 0]
    else:
        for i in range(5):
            for j in all_pos:
                x = soldier_rule(chess1, chess2, chess1[i], j)
                if x is not None and x != 0:
                    temp = chess1[i]
                    chess1[i] = x[0]
                    fl = check(chess2, chess1)
                    chess1[i] = temp
                    if x[1] == 2:
                        chess2[x[2]] = x[0]
                    if fl != 1:
                        return [1, x]
        for i in [5, 6]:
            for j in all_pos:
                x = cannon_rule(chess1, chess2, chess1[i], j)
                if x is not None and x != 0:
                    temp = chess1[i]
                    chess1[i] = x[0]
                    fl = check(chess2, chess1)
                    chess1[i] = temp
                    if x[1] == 2:
                        chess2[x[2]] = x[0]
                    if fl != 1:
                        return [1, x]
        for i in [7, 15]:
            for j in all_pos:
                x = car_rule(chess1, chess2, chess1[i], j)
                if x is not None and x != 0:
                    temp = chess1[i]
                    chess1[i] = x[0]
                    fl = check(chess2, chess1)
                    chess1[i] = temp
                    if x[1] == 2:
                        chess2[x[2]] = x[0]
                    if fl != 1:
                        return [1, x]
        for i in [8, 14]:
            for j in all_pos:
                x = horse_rule(chess2, chess1[i], j)
                if x is not None and x != 0:
                    temp = chess1[i]
                    chess1[i] = x[0]
                    fl = check(chess2, chess1)
                    chess1[i] = temp
                    if x[1] == 2:
                        chess2[x[2]] = x[0]
                    if fl != 1:
                        return [1, x]
        for i in [9, 13]:
            for j in all_pos:
                x = elephant_rule(chess2, chess1[i], j)
                if x is not None and x != 0:
                    temp = chess1[i]
                    chess1[i] = x[0]
                    fl = check(chess2, chess1)
                    chess1[i] = temp
                    if x[1] == 2:
                        chess2[x[2]] = x[0]
                    if fl != 1:
                        return [1, x]
        for i in [10, 12]:
            for j in all_pos:
                x = attendant_rule(chess1, chess2, chess1[i], j)
                if x is not None and x != 0:
                    temp = chess1[i]
                    chess1[i] = x[0]
                    fl = check(chess2, chess1)
                    chess1[i] = temp
                    if x[1] == 2:
                        chess2[x[2]] = x[0]
                    if fl != 1:
                        return [1, x]
        i = 11
        for j in all_pos:
            x = boss_rule(chess1, chess2, chess1[i], j, chess2[11])
            if x is not None and x != 0:
                temp = chess1[i]
                chess1[i] = x[0]
                fl = check(chess2, chess1)
                chess1[i] = temp
                if x[1] == 2:
                    chess2[x[2]] = x[0]
                if fl != 1:
                    return [1, x]
    return [0, chess1, chess2]


white = (255, 255, 255)
black = (0, 0, 0)

def highlight_piece(pos, color=(255,255,0), border_width=3):
    # pos is a two-element list [col, row] where each cell is 50x50 pixels.
    rect = pygame.Rect(pos[0]*50, pos[1]*50, 50, 50)
    pygame.draw.rect(screen, color, rect, border_width)
    pygame.display.update(rect)


def draw_text(text, x, y, size, pad_left=20, pad_right=20):
    pygame.font.init()
    fontObj = pygame.font.SysFont('Arial', size, bold=True)
    # Render the text with white on a black background
    textSurfaceObj = fontObj.render(text, True, white, black)
    # Get the original size
    text_width, text_height = textSurfaceObj.get_size()
    # Create a new surface with extra width for left and right padding
    new_width = text_width + pad_left + pad_right
    padded_surface = pygame.Surface((new_width, text_height))
    padded_surface.fill(black)
    # Blit the text onto the padded surface at an offset for left padding
    padded_surface.blit(textSurfaceObj, (pad_left, 0))
    # Get the rectangle of the padded surface and set its center
    textRectObj = padded_surface.get_rect()
    textRectObj.center = (x, y)
    # Blit the padded surface onto the main screen
    screen.blit(padded_surface, textRectObj)
    pygame.display.update(textRectObj)



def highlight_piece(pos, color=(255,255,0), border_width=3):
    """
    Draws an outline around the board cell at the given position.
    pos: a list [col, row] indicating the cell position.
    color: the highlight color (default yellow).
    border_width: thickness of the outline.
    """
    rect = pygame.Rect(pos[0] * 50, pos[1] * 50, 50, 50)
    pygame.draw.rect(screen, color, rect, border_width)
    pygame.display.update(rect)

if __name__ == '__main__':
    all_pos, progress = [], []
    for i in range(10):
        for j in range(9):
            all_pos.append([j, i])
    draw_text('Red First', 225, 525, 15)
    chess_kind = 0
    gameover = 0
    selected_piece = None
    while True:
        draw_chess()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                cell = [pos[0] // 50, pos[1] // 50]
                
                # Determine which side is active
                # if chess_kind == 0:
                #     chess1, chess2 = red_chess, black_chess
                if chess_kind == 0:  # Red (AI) turn
                    draw_text("Red (AI) thinking...", 225, 525, 15)
                    pygame.time.wait(500)  # optional delay to simulate thinking

                    best_move = find_best_move(red_chess, black_chess, depth=2)
                    if best_move:
                        index, new_pos = best_move
                        red_chess[index] = new_pos

                    chess_kind = 1  # switch to black (player)
                    draw_text("Black's turn", 225, 525, 15)
                    continue
                elif chess_kind == 1:
                    chess1, chess2 = black_chess, red_chess
                
                #If no piece is selected and the click hits one of our pieces, select it.
                for i in range(len(chess1)):
                    if (chess1[i][0] * 50 < pos[0] < (chess1[i][0] + 1) * 50 and 
                        chess1[i][1] * 50 < pos[1] < ((chess1[i][1] + 1) * 50)):
                        # Draw a green highlight on the selected piece
                        highlight_piece(chess1[i], color=(0, 255, 0), border_width=4)
                        flag = False
                        while True:
                            for event in pygame.event.get():
                                if event.type == MOUSEBUTTONDOWN:
                                    pos = pygame.mouse.get_pos()
                                    next_pos = [pos[0] // 50, pos[1] // 50]
                                    flag = True
                                    break
                            if flag:
                                break
                        progress.append(move(chess1, chess2, next_pos))
                        jj = 0
                        if progress[-1] is not None and progress[-1] != 0 and progress[-1] != 2:
                            if chess_kind == 0:
                                chess_kind = 1
                            elif chess_kind == 1:
                                chess_kind = 0
                            jj = check(chess1, chess2)
                        if chess_kind == 1:
                            if jj == 1:
                                bj = 1
                                cj = chess_jam(chess2, chess1)
                                print("cj:", cj)
                                if cj[0] != 1:
                                    gameover = 1
                                    draw_text("Red wins!", 225, 250, 30)
                                else:
                                    draw_text("Black's turn", 225, 525, 15)
                            else:
                                draw_text('    ', 150, 525, 15)
                                draw_text("Black's turn", 225, 525, 15)
                        elif chess_kind == 0:
                            if jj == 1:
                                bj = 1
                                cj = chess_jam(chess2, chess1)
                                print("cj:", cj)
                                if cj[0] != 1:
                                    gameover = 1
                                    draw_text("Black wins!", 225, 250, 30)
                                else:
                                    draw_text("Red's turn", 225, 525, 15)
                            else:
                                draw_text('            ', 150, 525, 15)
                                draw_text("Red's turn", 225, 525, 15)
                        if gameover == 1:
                            while True:
                                for event in pygame.event.get():
                                    if event.type == QUIT:
                                        pygame.quit()
                                        sys.exit()
                        break