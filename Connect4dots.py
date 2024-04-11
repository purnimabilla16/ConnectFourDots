import pygame, sys

from pygame import mixer_music

pygame.init()
pygame.mixer.init()

ball_sound = pygame.mixer.Sound('ballpop.mp3')
win_sound = pygame.mixer.Sound('winner.mp3')
tie_sound = pygame.mixer.Sound('tie.mp3')
buzzer_sound = pygame.mixer.Sound('buzzer.mp3')   
screen = pygame.display.set_mode((900, 800))  
board_game = pygame.Surface([700,600])
player1 = pygame.image.load('p1.jpg') 
player2 = pygame.image.load('p2.jpg') 

def draw_start_menu():
    pygame.display.set_caption("CONNECT FOUR DOTS")
    text = pygame.font.Font('font6.ttf', 60)
    back_g = pygame.image.load('backg1.jpg')
    surface = text.render('CONNECT FOUR DOTS', True, (50, 38, 83)) #anti-alias False - 8, True - 24 no. of colors
    screen.blit(back_g, (0, 0))
    screen.blit(surface, (110, 250))
    game_logo = pygame.image.load('logo.jpg')
    screen.blit(game_logo,(350,10))

    global start_rect
    start_text = text.render("START", True, (205, 24, 24))
    start_rect = pygame.rect.Rect((150,650), (230, 60))

    pygame.draw.rect(screen, (155, 164, 181), start_rect, 0, 150) #square and curve
    screen.blit(start_text, (153,653))

    global exit_rect  #used in input function
    exit_button = text.render("EXIT", True, (205, 24, 24))
    exit_rect = pygame.rect.Rect((600,650), (170, 60))
    pygame.draw.rect(screen, (155, 164, 181), exit_rect, 0, 150)
    screen.blit(exit_button, (603,653))

    text1 = pygame.font.Font('font6.ttf', 40)

    player_1_cd = (100,400)
    player1_text = text1.render("PLAYER1", True, (205, 24, 24))
    player1_rect = pygame.rect.Rect(player_1_cd, (200, 40))
    pygame.draw.rect(screen, (155, 164, 181), player1_rect, 0,5)
    screen.blit(player1_text, player_1_cd)

    player_2_cd = (100,500)
    player2_text = text1.render("PLAYER2", True, (205, 24, 24))
    player2_rect = pygame.rect.Rect(player_2_cd, (200, 40))
    pygame.draw.rect(screen, (155, 164, 181), player2_rect, 0, 5)
    screen.blit(player2_text, player_2_cd)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: #immediately after clicking
                if start_rect.collidepoint(event.pos):
                    return
                elif player1_rect.collidepoint(event.pos) or player2_rect.collidepoint(event.pos):
                    input_player_name()
                elif exit_rect.collidepoint(event.pos):
                    sys.exit()
        pygame.display.update()

def input_player_name():
    input_box_1 = pygame.Rect(400,400, 200, 60)
    input_box_2 = pygame.Rect(400,500, 200, 60)
    color_inactive = pygame.Color(230, 115, 159)
    color_active = pygame.Color(121, 12, 90)
    color1 = color_inactive
    color2 = color_inactive
    active1 = False
    active2 = False
    global text1 #used to display player names in main function
    global text2
    text1 = ""
    text2 = ""
    input_font = pygame.font.Font('freesansbold.ttf', 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_1.collidepoint(event.pos):
                    active1 = True
                    active2 = False
                    color1 = color_active
                    color2 = color_inactive
                    break 
                if input_box_2.collidepoint(event.pos):
                    active2 = True       
                    active1 = False
                    color1 = color_inactive
                    color2 = color_active
                    break
                if start_rect.collidepoint(event.pos) :
                    return
                elif exit_rect.collidepoint(event.pos) :
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if active1 :
                    if event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    else:
                        text1 += event.unicode
                if active2 :
                    if event.key == pygame.K_BACKSPACE:
                        text2 = text2[:-1]
                    else:
                        text2 += event.unicode

        pygame.draw.rect(screen, (250, 243, 240), input_box_1, 0,5)
        pygame.draw.rect(screen, (250, 243, 240), input_box_2, 0,5)       
        txt_surface1 = input_font.render(text1, True, color1)
        txt_surface2 = input_font.render(text2, True, color2)
        width1 = max(400, txt_surface1.get_width() + 10)
        width2 = max(400, txt_surface2.get_width() + 10)
        input_box_1.w = width1
        input_box_2.w = width2
        screen.blit(txt_surface1, (input_box_1.x + 5, input_box_1.y + 5))
        pygame.draw.rect(screen, color1, input_box_1, 2)
        screen.blit(txt_surface2, (input_box_2.x + 5, input_box_2.y + 5))
        pygame.draw.rect(screen, color2, input_box_2, 2)
        pygame.display.update()   
        
def won(turn) :
    font = pygame.font.Font("font7.otf", 40)
    if turn == 1 :
        text = font.render(f"{text1} WINS!!", True, (0, 129, 138), (219, 196, 240))
    else :
        text = font.render(f"{text2} WINS!!", True, (0, 129, 138), (219, 196, 240))
    win_sound.play()
    win = text.get_rect()
    win.center = (450,350)
    screen.blit(text,win)
    play_again()
    pygame.display.update()

def horizontal(board,symbol): 
    for i in range(6): 
          for j in range(4): 
            if board[i][j] == symbol and board[i][j+1] == symbol  and board[i][j+2] == symbol and board[i][j+3] == symbol :
                return True

def vertical(board,symbol):  
    for i in range(3):
        for j in range(7):
            if board[i][j] == symbol and board[i+1][j] == symbol  and board[i+2][j] == symbol and board[i+3][j] == symbol :
                return True
            
def diagonal(board,symbol):          
    for i in range(3):
        for j in range(4):
            if board[i][j] == symbol and board[i+1][j+1] == symbol and board[i+2][j+2] == symbol and board[i+3][j+3] == symbol :
                return True
    for i in range(3):
        for j in range(3, 7):
            if board[i][j] == symbol and board[i+1][j-1] == symbol and board[i+2][j-2] == symbol and board[i+3][j-3] == symbol :
                return True  
            
def column_filled(board, c) : 
    for row in range(5, -1, -1) :
        if board[row][c - 1] == "_" :
            return False
    return True      

def tie_check(board) : 
    for row in board :
        for element in row :
            if element == "_" :
                return False
    return True

def print_board(board) :
    for row in board :
        for element in row :
            print(element, end = " ") 
        print()

def p1(board,r,c) :
    for row in range(5, -1, -1) :
        if board[row][c - 1] == "X" or board[row][c - 1] == "O" :
            continue
        else :    
            board[row][c - 1] = "X"
            print_board(board)
            break
    return row

def p2(board,r, c) :
    for row in range(5, -1, -1) :
        if board[row][c - 1] == "X" or board[row][c - 1] == "O":
            continue
        else :    
            board[row][c - 1] = "O"
            print_board(board)
            break   
    return row

def play_again() :
    text = pygame.font.Font('font6.ttf',40)
    button_reset = text.render("PLAY AGAIN?",True,(145, 53, 53))
    reset_rect = pygame.rect.Rect((30,720),(300,50)) 
    pygame.draw.rect(screen,(227, 196, 168),reset_rect,0,5)
    screen.blit(button_reset,(33,723))
    button_quit = text.render("QUIT",True,(145, 53, 53))
    quit_rect = pygame.rect.Rect((650,720),(130,50)) 
    pygame.draw.rect(screen,(227, 196, 168),quit_rect,0,5)
    screen.blit(button_quit,(653,723))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                 pygame.quit
                 sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                 if reset_rect.collidepoint(event.pos) :
                    main() 
                 elif quit_rect.collidepoint(event.pos) :
                    draw_start_menu()
                    main()
        pygame.display.update()

def circles(board_game) :
    y = 50
    for rows in range(6) :
        x = 50
        for columns in range(7) :
            pygame.draw.circle(board_game,(244, 211, 211),(x, y),35)  
            x += 100
        y += 100

def main() :   
    screen.fill((244, 211, 211)) 
    board_game.fill((0, 0, 255))
    circles(board_game)
    screen.blit(player1,(15,15)) 
    screen.blit(player2,(815,15))
    text = pygame.font.Font('font7.otf', 25)
    text1_rect = text.render(text1, True, (0, 0, 0))
    text2_rect = text.render(text2, True, (0, 0, 0))
    screen.blit(text1_rect, (110, 30))
    screen.blit(text2_rect, (690, 30))

    board = [["_" for columns in range(7)] for rows in range(6)]
    turn = 1
    c, row = 0, 0
    global symbol
    symbol = "X"
    # r - selected row, row - row to be filled 
    while True :
        for event in pygame.event.get() : 
            if event.type == pygame.QUIT :
                pygame.quit()  
                sys.exit() 
            if event.type == pygame.MOUSEBUTTONDOWN:
                position=pygame.mouse.get_pos()     
                x = position[0]        
                y = position[1]  
                print (f"x-{x},y-{y}")
                r = y//100
                c = x//100
                print(r, c) 
                if column_filled(board, c) :
                    font = pygame.font.Font("freesansbold.ttf", 40)
                    text = font.render("Oops! Column filled", True, (228, 88, 38))
                    buzzer_sound.play()
                    col_fill = text.get_rect()
                    col_fill.center = (450,50)
                    screen.blit(text,col_fill)
                    continue
                font = pygame.font.Font("freesansbold.ttf", 40)
                text = font.render("Oops! Column filled", True, (244,211,211),(244,211,211))
                rectangle = text.get_rect()
                rectangle.center = (450,50)
                screen.blit(text,rectangle)
                if turn == 1 :
                    row = p1(board,r,c)
                    symbol = "X"
                    pygame.draw.circle(board_game,(234, 146, 21),(c*100-50,(row+1)*100-50),35) 
                    ball_sound.play()
                    turn = 2
                else :
                    row = p2(board,r,c)
                    symbol = "O"
                    pygame.draw.circle(board_game,(218, 0, 55),(c*100-50,(row+1)*100-50),35)
                    ball_sound.play()
                    turn = 1
                pygame.display.update()
                if tie_check(board) :
                    font = pygame.font.Font("freesansbold.ttf", 60)
                    text = font.render("Tie! Gameover!!", True, (155, 0, 0))
                    tie_sound.play()
                    tie = text.get_rect()
                    tie.center = (450,50)
                    screen.blit(text,tie)
                    pygame.display.update()
                    play_again()
                    while True :
                        for event in pygame.event.get() : 
                            if event.type == pygame.QUIT :
                                pygame.quit()  
                                sys.exit()
        screen.blit(board_game,(100,100))    
        pygame.display.update()
        if horizontal(board,symbol) or vertical(board,symbol) or diagonal(board,symbol) :
            if turn == 1 :
                won(2)
            else :
                won(1)
            while True :
                for event in pygame.event.get() : 
                    if event.type == pygame.QUIT :
                        pygame.quit()  
                        sys.exit()

draw_start_menu()
main()
