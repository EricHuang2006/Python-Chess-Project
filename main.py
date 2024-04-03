import pygame

from constants import *

pygame.init()

counter = 0
winner = ''
game_over = False
white_time = 36000
black_time = 36000
takeback = 0
take_back_a = 0
theme = 0
stage = 0
text = [['Yes', ' No'], [' 3 min', ' 5 min', '10 min', '30 min']]
text_pos = [[(510, 125), (712, 125)], [(300, 275), (500, 275), (700, 275), (900, 275)]];
highlight = [[], [], []]
select = [0, 0, 0]
# gray-white / green-white / blue-white / brown-white 
color_theme = [[(128, 128, 128), (220, 220, 220)], [(131, 197, 82), (220, 220, 220)], [(66, 190, 216), (220, 220, 220)], [(244, 119, 33), (254, 220, 170)]]
white_pieces = []
white_locations = []
black_pieces = []
black_locations = []
captured_pieces_white = []
captured_pieces_black = []
black_options = []
white_options = []
en_white = (-1, -1)
en_black = (-1, -1)
promote_color = ''
promote_index = -1
promotion_list = ['queen', 'rook', 'knight', 'bishop']
black_score = 0
white_score = 0
castle = [1, 1, 1, 1]
swp = []
swl = []
sbp = []
sbl = []
cpw = []
cpb = []
sc = []
eb = (-1, -1)
ew = (-1, -1)
sts = 0
pc = ''
pi = -1
sbs = 0
sws = 0

def init():
    global white_pieces, white_locations, black_pieces, black_locations, captured_pieces_white, captured_pieces_black
    white_pieces = white_pieces_init.copy()
    white_locations = white_locations_init.copy()
    black_pieces = black_pieces_init.copy()
    black_locations = black_locations_init.copy()
    captured_pieces_white = []
    captured_pieces_black = []
    global black_options, white_options
    black_options = check_options(black_pieces, black_locations, 'black')
    white_options = check_options(white_pieces, white_locations, 'white')
    counter = 0
    global winner, game_over, white_time, black_time, takeback_a, theme, highlight, select, turn_step, selection, castle
    winner = ''
    game_over = False
    white_time = 36000
    black_time = 36000
    takeback_a = 0
    theme = 0
    turn_step = 0 
    highlight = [[], [], []]
    select = [0, 0, 0]
    selection = 100
    castle = [1, 1, 1, 1]
    global white_score, black_score
    white_score = 0
    black_score = 0

def font(x):
    return pygame.font.Font('freesansbold.ttf', x)

def draw_init():
    screen.fill('gray')
    screen.blit(medium_font.render('Allow Takeback?', True, 'black'), (510, 50))
    screen.blit(medium_font.render('Timer', True, 'black'), (585, 200))
    screen.blit(medium_font.render('Color Theme', True, 'black'), (532, 375))
    mid_font = pygame.font.Font('freesansbold.ttf', 25)
    for i in range(2):
        for j in range(len(text[i])):
            screen.blit(mid_font.render(text[i][j], True, 'black'), text_pos[i][j])
            pygame.draw.rect(screen, 'black', [text_pos[i][j][0] - 25 + i * 15, text_pos[i][j][1] - 15, 100, 50], 5)
        if len(highlight[i]) :
            pygame.draw.rect(screen, 'red', [highlight[i][0], highlight[i][1], 100, 50], 5)
    for i in range(4):
        pygame.draw.rect(screen, color_theme[i][0], [100 + i * 300, 450, 100, 100]);
        pygame.draw.rect(screen, color_theme[i][1], [200 + i * 300, 450, 100, 100]);
    screen.blit(medium_font.render('Ok', True, 'black'), (1100, 675))
    if len(highlight[2]):
        pygame.draw.rect(screen, 'red', [highlight[2][0], highlight[2][1], 200, 100], 5)
    pygame.draw.rect(screen, 'black', [1085, 660, 70, 60], 5)
def store_takeback():
    global swp, swl, sbp, sbl, cpw, cpb, sts, pc, pi, eb, ew, sc, sbs, sws
    swp = white_pieces.copy()
    swl = white_locations.copy()
    sbp = black_pieces.copy()
    sbl = black_locations.copy()
    sts = turn_step
    pc = promote_color
    pi = promote_index
    eb = en_black
    ew = en_white
    sc = castle.copy()
    sbs = black_score
    sws = white_score

def rollback():
    global white_pieces, white_locations, black_pieces, black_locations, captured_pieces_white, captured_pieces_black
    white_pieces = swp.copy()
    white_locations = swl.copy()
    black_pieces = sbp.copy()
    black_locations = sbl.copy()
    captured_pieces_white = cpw.copy()
    captured_pieces_black = cpb.copy()
    global turn_step, promote_color, promote_index, black_options, white_options, en_black, en_white, selection, castle
    global white_score, black_score
    castle = sc.copy()
    turn_step = sts - (sts % 2)
    selection = 100
    promote_color = pc
    promote_index = pi
    en_black = eb
    en_white = ew
    white_score = sws
    black_score = sbs
    black_options = check_options(black_pieces, black_locations, 'black')
    white_options = check_options(white_pieces, white_locations, 'white')
    black_options = check_options(black_pieces, black_locations, 'black')
    white_options = check_options(white_pieces, white_locations, 'white')

def access(coord):
    for i in range(4):
        if coord[0] >= 100 + i * 300 and coord[0] <= 300 + i * 300 and coord[1] >= 450 and coord[1] <= 550:
            select[2] = i
            highlight[2] = [100 + i * 300, 450]
    for i in range(2):
        for j in range(len(text[i])):
            if coord[0] >= text_pos[i][j][0] - 25 + i * 15 and coord[0] <= text_pos[i][j][0] + 75 + i * 15 and\
               coord[1] >= text_pos[i][j][1] - 15 and coord[1] <= text_pos[i][j][1] + 85:
               highlight[i] = [text_pos[i][j][0] - 25 + i * 15, text_pos[i][j][1] - 15]
               select[i] = j
    if coord[0] >= 1085 and coord[0] <= 1155 and coord[1] >= 660 and coord[1] <= 720:
        return False
    return True

def check_ok(coord):
    if coord[0] >= 1085 and coord[0] <= 1155 and coord[1] >= 660 and coord[1] <= 720:
        return True
    return False

def setup():
    global takeback_a
    takeback_a = (select[0] == 1)
    time = [3, 5, 10, 30]
    global white_time, black_time
    white_time = time[select[1]] * 60 * 60
    black_time = time[select[1]] * 60 * 60

def get_time(t):
    t = t // 60
    m = t // 60
    s = t % 60
    ret = str(m) + ' : ' 
    if s < 10:
        ret += '0' + str(s)
    else:
        ret += str(s)
    return ret

def draw_board(ck = True):
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, color_theme[select[2]][0], [100 + column * 200, row * 100, 100, 100])
            pygame.draw.rect(screen, color_theme[select[2]][1], [column * 200, row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, color_theme[select[2]][0], [column * 200, row * 100, 100, 100])
            pygame.draw.rect(screen, color_theme[select[2]][1], [100 + column * 200, row * 100, 100, 100])
    for i in range(2):
        pygame.draw.line(screen, 'yellow', (i * 1298, (1 - i) * 800), (i * 1298, i * 800), 2)
        pygame.draw.line(screen, 'yellow', ((1 - i) * 2398, i * 800), (i * 1298, i * 800), 2)
    pygame.draw.line(screen, 'yellow', (800, 0), (800, 800), 2)
    pygame.draw.line(screen, 'yellow', (800, 100), (1300, 100), 2)
    if ck == False:
        screen.blit(font(35).render('Select Handicap Pieces!', True, 'black'), (840, 40))
        return
    screen.blit(font(25).render('+' + str(white_score), True, 'black'), (820, 280))
    screen.blit(font(25).render('+' + str(black_score), True, 'black'), (820, 500))
    for i in [1, 2, 6, 7] :
        pygame.draw.line(screen, 'yellow', (800, i * 100), (1300, i * 100), 2)
    pygame.draw.line(screen, 'yellow', (1050, 700), (1050, 800), 2)
    status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                   'Black: Select a Piece to Move!', 'Black: Select a Destination!']
    if promote_index != -1:
        screen.blit(medium_font.render(promote_color + ": Promote Pawn!", True, 'black'), (820, 40))
    else:
        screen.blit(medium_font.render(status_text[turn_step], True, 'black'), (820, 40))
    screen.blit(medium_font.render('Forfeit', True, 'black'), (875, 735))
    if takeback_a == 0:
        screen.blit(medium_font.render('Takeback', True, 'black'), (1103, 735))
    screen.blit(font(40).render(get_time(white_time), True, 'black'), (1000, 132))
    screen.blit(font(40).render(get_time(black_time), True, 'black'), (1000, 632))

def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 23, white_locations[i][1] * 100))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 21, white_locations[i][1] * 100 + 5))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100, 100, 100], 2)
    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 23, black_locations[i][1] * 100))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 21, black_locations[i][1] * 100 + 5))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100, 100, 100], 2)
def draw_handicap():
    screen.blit(medium_font.render('Ok', True, 'black'), (1100, 675))
    pygame.draw.rect(screen, 'yellow', [1085, 660, 70, 60], 3)
#function to check all pieces valid options on board
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range(len(pieces)):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        all_moves_list.append(moves_list)

    return all_moves_list

def inbound(x, y):
    return x >= 0 and y >= 0 and x < 8 and y < 8

def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        enemies_list = white_locations
        friends_list = black_locations
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]
    for i in range(4):
        x = position[0]
        y = position[1]
        flag = 1;
        while(flag):
            x += dx[i]
            y += dy[i]
            if inbound(x, y) == 0:
                break
            elif (x, y) in friends_list:
                flag = 0
            elif (x, y) in enemies_list:
                moves_list.append((x, y))
                flag = 0
            else:
                moves_list.append((x, y))
    return moves_list

def check_queen(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        enemies_list = white_locations
        friends_list = black_locations
    dx = [1, 1, 0, -1, -1, -1, 0, 1]
    dy = [0, 1, 1, 1, 0, -1, -1, -1]
    for i in range(8):
        x = position[0]
        y = position[1]
        flag = 1;
        while(flag):
            x += dx[i]
            y += dy[i]
            if inbound(x, y) == 0:
                break
            elif (x, y) in friends_list:
                flag = 0
            elif (x, y) in enemies_list:
                moves_list.append((x, y))
                flag = 0
            else:
                moves_list.append((x, y))
    return moves_list

def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        enemies_list = white_locations
        friends_list = black_locations
    dx = [1, -1, -1, 1]
    dy = [1, 1, -1, -1]
    for i in range(4):
        x = position[0]
        y = position[1]
        flag = 1;
        while(flag):
            x += dx[i]
            y += dy[i]
            if inbound(x, y) == 0:
                break
            elif (x, y) in friends_list:
                flag = 0
            elif (x, y) in enemies_list:
                moves_list.append((x, y))
                flag = 0
            else:
                moves_list.append((x, y))
    return moves_list

def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        enemies_list = white_locations
        friends_list = black_locations
    dx = [2, 1, -1, -2, -2, -1, 1, 2]
    dy = [1, 2, 2, 1, -1, -2, -2, -1]
    for i in range(8):
        x = position[0] + dx[i]
        y = position[1] + dy[i]
        if inbound(x, y) and (x, y) not in friends_list:
            moves_list.append((x, y))
    return moves_list

def check_king(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
        ok = castle[0]
        for i in range(1, 3):
            if (i, 0) in enemies_list or (i, 0) in friends_list:
                ok = 0
            for j in range(len(black_options)):
                if (i, 0) in black_options[j]:
                    ok = 0
        if ok :
            moves_list.append([0, 0])
        ok = castle[1]
        for i in range(4, 7):
            if (i, 0) in enemies_list or (i, 0) in friends_list:
                ok = 0
            for j in range(len(black_options)):
                if (i, 0) in black_options[j]:
                    ok = 0
        if ok :
            moves_list.append([7, 0])
    else:
        enemies_list = white_locations
        friends_list = black_locations
        ok = castle[2]
        for i in range(1, 3):
            if (i, 7) in enemies_list or (i, 7) in friends_list:
                ok = 0
            for j in range(len(white_options)):
                if (i, 7) in white_options[j]:
                    ok = 0
        if ok :
            moves_list.append([0, 7])
        ok = castle[3]
        for i in range(4, 7):
            if (i, 7) in enemies_list or (i, 7) in friends_list:
                ok = 0
            for j in range(len(white_options)):
                if (i, 7) in white_options[j]:
                    ok = 0
        if ok :
            moves_list.append([7, 7])
    dx = [1, 1, 0, -1, -1, -1, 0, 1]
    dy = [0, 1, 1, 1, 0, -1, -1, -1]
    for i in range(8):
        x = position[0] + dx[i]     
        y = position[1] + dy[i]
        if inbound(x, y) and (x, y) not in friends_list:
            moves_list.append((x, y))
    return moves_list

def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_locations and \
           (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
            if (position[0], position[1] + 2) not in white_locations and \
               (position[0], position[1] + 2) not in black_locations and position[1] == 1:
               moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations or (position[0] + 1, position[1]) == en_white:
           moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations or (position[0] - 1, position[1]) == en_white:
           moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and \
           (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
            if (position[0], position[1] - 2) not in white_locations and \
               (position[0], position[1] - 2) not in black_locations and position[1] == 6:
               moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations or (position[0] + 1, position[1]) == en_black:
           moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations or (position[0] - 1, position[1]) == en_black:
           moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list

#check valid moves for just selected piece
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options

#draw valid moves on screen
def draw_valid(moves):
    # color = 'tan'
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 10)

def draw_captured():
    for i in range(len(captured_pieces_white)):
        piece = captured_pieces_white[i]
        index = piece_list.index(piece)
        screen.blit(small_black_images[index], (815 + 30 * i, 330))
    for i in range(len(captured_pieces_black)):
        piece = captured_pieces_black[i]
        index = piece_list.index(piece)
        screen.blit(small_white_images[index], (815 + 30 * i, 410))

def draw_check():
    if game_over:
        return
    checked = False

    king_index = white_pieces.index('king')
    king_location = white_locations[king_index]
    for i in range(len(black_options)):
        if king_location in black_options[i]:
            if counter < 15:
                pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1, 
                                                      white_locations[king_index][1] * 100 + 1, 100, 100], 5)
    king_index = black_pieces.index('king')
    king_location = black_locations[king_index]
    for i in range(len(white_options)):
        if king_location in white_options[i]:
            if counter < 15:
                pygame.draw.rect(screen, 'dark red', [black_locations[king_index][0] * 100 + 1, 
                                                      black_locations[king_index][1] * 100 + 1, 100, 100], 5)

def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 300, 400, 100])
    pygame.draw.rect(screen, 'yellow', [200, 300, 400, 100], 2)
    screen.blit(medium_font.render(f'{winner} won the game!', True, 'white'), (210, 310))
    screen.blit(medium_font.render(f'Press ENTER to restart', True, 'white'), (210, 360))

def check_forfeit(x, y):
    return x >= 800 and x <= 1050 and y >= 700 and y <= 800
def check_takeback(x, y):
    return x >= 1050 and y >= 700 and y <= 800 and takeback and takeback_a == 0

def draw_promotion(index, color):
    if(color == 'White'):
        pygame.draw.rect(screen, 'red', [805, 500, 400, 100], 5)
        for i in range(4):
            id = piece_list.index(promotion_list[i])
            screen.blit(white_images[id], (805 + i * 100 + 22, 505))
    else:
        pygame.draw.rect(screen, 'red', [805, 202, 400, 100], 5)
        for i in range(4):
            id = piece_list.index(promotion_list[i])
            screen.blit(black_images[id], (805 + i * 100 + 22, 207))

def check_promotion(x, y):
    if promote_color == 'White':
        return x >= 805 and x <= 1205 and y >= 500 and y <= 600;
    else :
        return x >= 805 and x <= 1205 and y >= 200 and y <= 300;

run = True
# stage = 0 : initialize variables / stage = 1 : starting page / stage = 2 : handicap 
# stage = 3 : main function
while run:
    timer.tick(fps)
    if stage == 0:
        init()
        stage = 1
        continue;
    if stage == 1:
        draw_init()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x = event.pos[0]
                y = event.pos[1]
                coord = (x, y)
                if access(coord) == False:
                    setup()
                    stage = 2

        pygame.display.flip()
        continue

    counter = (counter + 1) % 30
    screen.fill('tan')
    if stage == 2:
        draw_handicap()
        draw_board(False)
    else:
        draw_board(True)
    draw_pieces()
    draw_captured()
    draw_check()

    if promote_color != '':
        draw_promotion(promote_index, promote_color)
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
    if turn_step < 2:
        white_time -= 1 - game_over + (stage - 3)
        if white_time == 0:
            winner = 'Black'
    else:
        black_time -= 1 - game_over + (stage - 3)
        if black_time == 0:
            winner = 'White'
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    stage = 0
            continue
        if stage == 2:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x = event.pos[0] // 100
                y = event.pos[1] // 100
                click_coords = (x, y)
                if click_coords in black_locations:
                    black_piece = black_locations.index(click_coords)
                    index = piece_list.index(black_pieces[black_piece]);
                    white_score += score[index]
                    captured_pieces_white.append(black_pieces[black_piece])
                    black_pieces.pop(black_piece)
                    black_locations.pop(black_piece)
                if click_coords in white_locations:
                    white_piece = white_locations.index(click_coords)
                    index = piece_list.index(white_pieces[white_piece])
                    black_score += score[index]
                    captured_pieces_black.append(white_pieces[white_piece])
                    white_pieces.pop(white_piece)
                    white_locations.pop(white_piece)
                click_coords = (event.pos[0], event.pos[1]);
                if check_ok(click_coords):
                    stage = 3
                    white_options = check_options(white_pieces, white_locations, 'white')
                    black_options = check_options(black_pieces, black_locations, 'black')
                    black_options = check_options(black_pieces, black_locations, 'black') # for castling
                    white_options = check_options(white_pieces, white_locations, 'white') # for castling
            continue
        if game_over == 0 and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if promote_index != -1:
                if check_promotion(event.pos[0], event.pos[1]):
                    if promote_color == 'White':
                        white_pieces[promote_index] = promotion_list[(event.pos[0] - 805) // 100]
                    else:
                        black_pieces[promote_index] = promotion_list[(event.pos[0] - 805) // 100]
                    promote_color = ''
                    promote_index = -1
                    white_options = check_options(white_pieces, white_locations, 'white')
                    black_options = check_options(black_pieces, black_locations, 'black')
                continue;

            if check_forfeit(event.pos[0], event.pos[1]):
                if turn_step < 2 :
                    winner = 'Black'
                else:
                    winner = 'White'
                continue
            if check_takeback(event.pos[0], event.pos[1]):
                rollback()
                takeback = 0
                continue
            x = event.pos[0] // 100
            y = event.pos[1] // 100
            click_coords = (x, y)
            if turn_step < 2:
                ok = 0
                for i in range(len(valid_moves)):
                    if click_coords[0] == valid_moves[i][0] and click_coords[1] == valid_moves[i][1]:
                        ok = 1;
                if ok and selection != 100:
                    # move_sfx.play()
                    store_takeback()
                    takeback = 1
                    if click_coords in white_locations:
                        a = white_locations.index(click_coords)
                        if white_locations[a][0] == 0:
                            white_locations[selection] = (1, 0)
                            white_locations[a] = (2, 0)
                        else:
                            white_locations[selection] = (5, 0)
                            white_locations[a] = (4, 0)
                        castle[0] = castle[1] = False

                        white_options = check_options(white_pieces, white_locations, 'white')
                        black_options = check_options(black_pieces, black_locations, 'black')
                        black_options = check_options(black_pieces, black_locations, 'black') # for castling
                        white_options = check_options(white_pieces, white_locations, 'white') # for castling
                        turn_step = 2
                        selection = 100
                        valid_moves = []
                        continue  # castling

                    if white_pieces[selection] == 'king':
                        castle[0] = 0
                        castle[1] = 0
                    if white_pieces[selection] == 'rook':
                        if white_locations[selection] == (0, 0):
                            castle[0] = 0
                        if white_locations[selection] == (7, 0):
                            castle[1] = 0
                    if white_pieces[selection] == 'pawn':
                        if click_coords[0] == white_locations[selection][0] and click_coords[1] == white_locations[selection][1] + 2:
                            en_black = click_coords
                        if click_coords[1] == en_white[1] + 1 and click_coords[0] == en_white[0]:
                            white_score += 1
                            black_piece = black_locations.index(en_white)
                            captured_pieces_white.append(black_pieces[black_piece])
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)
                    white_locations[selection] = click_coords
                    if click_coords in black_locations:
                        if click_coords == (0, 7):
                            castle[2] = 0
                        if click_coords == (7, 7):
                            castle[3] = 0
                        black_piece = black_locations.index(click_coords)
                        index = piece_list.index(black_pieces[black_piece]);
                        white_score += score[index]
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'White'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    if white_pieces[selection] == 'pawn' and y == 7:
                        promote_index = selection
                        promote_color = 'White'

                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []
                    en_white = (-1, -1)
                    continue

                if click_coords in white_locations: 
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1

            if turn_step >= 2:
                ok = 0
                for i in range(len(valid_moves)):
                    if click_coords[0] == valid_moves[i][0] and click_coords[1] == valid_moves[i][1]:
                        ok = 1;
                if ok and selection != 100:
                    # move_sfx.play()
                    store_takeback()
                    takeback = 1
                    if click_coords in black_locations:
                        a = black_locations.index(click_coords)
                        if black_locations[a][0] == 0:
                            black_locations[selection] = (1, 7)
                            black_locations[a] = (2, 7)
                        else:
                            black_locations[selection] = (5, 7)
                            black_locations[a] = (4, 7)
                        castle[2] = castle[3] = False

                        white_options = check_options(white_pieces, white_locations, 'white')
                        black_options = check_options(black_pieces, black_locations, 'black')
                        black_options = check_options(black_pieces, black_locations, 'black') # for castling
                        white_options = check_options(white_pieces, white_locations, 'white') # for castling
                        turn_step = 0
                        selection = 100
                        valid_moves = []
                        continue # castling

                    if black_pieces[selection] == 'king':
                        castle[2] = 0
                        castle[3] = 0
                    if black_pieces[selection] == 'rook':
                        if black_locations[selection] == (0, 7):
                            castle[2] = 0
                        if black_locations[selection][0] == (7, 7):
                            castle[3] = 0
                    if black_pieces[selection] == 'pawn':
                        if click_coords[0] == black_locations[selection][0] and click_coords[1] == black_locations[selection][1] - 2:
                            en_white = click_coords
                        if click_coords[1] == en_black[1] - 1 and click_coords[0] == en_black[0]:
                            black_score += 1
                            white_piece = white_locations.index(en_black)
                            captured_pieces_black.append(white_pieces[white_piece])
                            white_pieces.pop(white_piece)
                            white_locations.pop(white_piece)
                    black_locations[selection] = click_coords
                    if click_coords in white_locations:
                        if click_coords == (0, 0):
                            castle[2] = 0
                        if click_coords == (7, 0):
                            castle[3] = 0
                        white_piece = white_locations.index(click_coords)
                        index = piece_list.index(white_pieces[white_piece]);
                        black_score += score[index]
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'Black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    if black_pieces[selection] == 'pawn' and y == 0:
                        promote_index = selection
                        promote_color = 'Black'

                    white_options = check_options(white_pieces, white_locations, 'white')
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    black_options = check_options(black_pieces, black_locations, 'black')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
                    en_black = (-1, -1)
                    continue

                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3

    if winner != '':
        game_over = True
        draw_game_over()
    pygame.display.flip()
pygame.quit()
