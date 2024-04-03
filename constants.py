import pygame
from pygame import mixer
pygame.init()
WIDTH = 1300
HEIGHT = 802
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two-Player Pygame Chess!')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 30)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60

white_pieces_init = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations_init = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), 
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces_init = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations_init = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), 
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
# 0 - white, no selection 1 - white, piece selected, 2 - black, no selection, 3 - black, piece selected
turn_step = 0
selection = 100
valid_moves = []

black_queen = pygame.image.load('assets/images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (54, 90))
black_queen_small = pygame.transform.scale(black_queen, (30, 50))
black_king = pygame.image.load('assets/images/black king.png')
black_king = pygame.transform.scale(black_king, (54, 90))
black_king_small = pygame.transform.scale(black_king, (30, 50))
black_rook = pygame.image.load('assets/images/black rook.png')
black_rook = pygame.transform.scale(black_rook, (54, 90))
black_rook_small = pygame.transform.scale(black_rook, (30, 50))
black_bishop = pygame.image.load('assets/images/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (54, 90))
black_bishop_small = pygame.transform.scale(black_bishop, (30, 50))
black_knight = pygame.image.load('assets/images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (54, 90))
black_knight_small = pygame.transform.scale(black_knight, (30, 50))
black_pawn = pygame.image.load('assets/images/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (54, 90))
black_pawn_small = pygame.transform.scale(black_pawn, (30, 50))
white_queen = pygame.image.load('assets/images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (54, 90))
white_queen_small = pygame.transform.scale(white_queen, (30, 50))
white_king = pygame.image.load('assets/images/white king.png')
white_king = pygame.transform.scale(white_king, (54, 90))
white_king_small = pygame.transform.scale(white_king, (30, 50))
white_rook = pygame.image.load('assets/images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (54, 90))
white_rook_small = pygame.transform.scale(white_rook, (30, 50))
white_bishop = pygame.image.load('assets/images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (54, 90))
white_bishop_small = pygame.transform.scale(white_bishop, (30, 50))
white_knight = pygame.image.load('assets/images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (54, 90))
white_knight_small = pygame.transform.scale(white_knight, (30, 50))
white_pawn = pygame.image.load('assets/images/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (54, 90))
white_pawn_small = pygame.transform.scale(white_pawn, (30, 50))
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small, white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small, black_rook_small, black_bishop_small]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
score = [1, 9, 0, 3, 5, 3]
# move_sfx = pygame.mixer.Sound('assets/sound.mp3')
