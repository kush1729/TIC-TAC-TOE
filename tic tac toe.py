import pygame
from time import sleep      #to delay updating screen after screen change to prevent unwanted actions occuring in next screen
pygame.init()

#Initialize-----------------
pygame.display.set_caption('TIC TAC TOE')
icon = pygame.image.load('icon_pic.png')
pygame.display.set_icon(icon)
#---------------------------

#Colours--------------------
white = (255, 255, 255)
black = (0, 0, 0)
grey = (200, 200, 200)
red = (200, 0, 0)
light_red = (255, 0, 0)
yellow = (200, 200, 0)
light_yellow = (255, 255, 0)
blue = (0, 0, 255)
green = (34, 177, 76)
light_green = (0, 255, 0)
#---------------------------

#Constants------------------
block_size = 150
gap = 15
sleep_time = 0.40
display_width = display_height = 3*block_size + 2*gap
display_height += 20
gameDisplay = pygame.display.set_mode((display_width, display_height))
smallfont = pygame.font.SysFont("comicsansms", 20)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)
clock = pygame.time.Clock()
FPS = 15
comp_turn = 2 #whether comp is X or O
backColour = grey
gridXpos = 0
gridYpos = 0
gridLoc = []
cells = []
for i in range(3):
    gridLoc.append([])
    cells.append([])
    for j in range(3):
        gridLoc[i].append(((gridXpos + i*block_size + i*gap), (gridYpos + j*block_size + j*gap)))
        cells[i].append(False)
#---------------------------

#Functions------------------

def drawCross(x, y, size = 100, colour = black, thickness = 5):
    pygame.draw.line(gameDisplay, colour, (x, y), (x + size, y + size), thickness)
    pygame.draw.line(gameDisplay, colour, (x, y + size), (x + size, y), thickness)

def drawCircle(x1, y1, radius = 50, thickness = 5, colour = black, BackColour = backColour):
    x = x1 + radius
    y = y1 + radius
    pygame.draw.circle(gameDisplay, colour, (x, y), radius, thickness)

def drawGrid(x = 0, y = 0, indSize = block_size, colour = grey):
    for row in gridLoc:
        for box in row:
            pygame.draw.rect(gameDisplay, colour, (box[0], box[1], indSize, indSize))

def pressButton(turn, loc, size = block_size):
    global cells
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    Loc = gridLoc[loc[0]][loc[1]]
    if click[0] == 1:
        if Loc[0] + size > cur[0] > Loc[0] and Loc[1] + size > cur[1] > Loc[1]:
            if cells[loc[1]][loc[0]] == False:
                if turn % 2 == 0:
                    drawCross(Loc[0], Loc[1], size)
                else:
                    drawCircle(Loc[0], Loc[1], size//2)
                cells[loc[1]][loc[0]] = 2 if turn%2==0 else 1
                return turn + 1
    return turn

def button(text, x, y, width, height, inactiveColour, activeColour, action = None):
    global comp_turn
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > cur[0] > x and y + height > cur[1] > y:
        if click[0] == 1 and action != None:
            if action == 'quit':
                pygame.quit()
                quit()
            if action == 'play':
                gameLoop_multi()
            if action == 'single':
                gameLoop_single_menu()
            if action == 'restart':
                gameStart()
            if action == 'x':
                comp_turn = 1
                gameLoop_single()
            if action == 'o':
                comp_turn = 2
                gameLoop_single()
        pygame.draw.rect(gameDisplay, activeColour, (x, y, width, height))
    else:
        pygame.draw.rect(gameDisplay, inactiveColour, (x, y, width, height))
    text_to_button(text, black, x, y, width, height)

def text_objects(text, color, size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def text_to_button(msg, color, btnx, btny, btnwidth, btnheight, size = "small"):
    textSurf , textRect = text_objects(msg, color, size)
    textRect.center = ((btnx + (btnwidth / 2)), (btny + (btnheight / 2)))
    gameDisplay.blit(textSurf, textRect)

def message_to_screen(msg, color, y_displace = 0, size = "small"):
    textSurf , textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)

def reset():
    global cells
    cells = [[False for i in range(3)] for j in range(3)]

def gameOver(single_player = False, sin_play_winner = None): 
    flag = False
    player = 0
    draw = False
    for i in range(3):  #to check for win
        if cells[i][0] == cells[i][1] == cells[i][2] != False:
            flag = True
            player = cells[i][0]
            break
        elif cells[0][i] == cells[1][i] == cells[2][i] != False:
            flag = True
            player = cells[0][i]
            break
    else:
        if cells[0][0] == cells[1][1] == cells[2][2] != False:
            flag = True
            player = cells[0][0]
        elif cells[0][2] == cells[1][1] == cells[2][0] != False:
            flag = True
            player = cells[1][1]
    if not flag:    #to check for draw
        for rows in cells:
            if False in rows: break
        else:
            flag = True
            draw = True
    if flag:
        player = 2 if player == 1 else 1
        sleep(sleep_time)
        gameDisplay.fill(white)
        message_to_screen('GAME OVER', red, -60, "medium")
        if not draw:
            if single_player:
                if sin_play_winner.lower() == 'player':
                    message_to_screen('YOU HAVE WON  :-D', light_red, -10 ,  size = 'small')
                elif sin_play_winner.lower() == 'comp':
                    message_to_screen('COMPUTER HAS WON :-(', light_red, -10 ,  size = 'small')
            else:
                message_to_screen('PLAYER ' + str(player) + ' HAS WON', light_red, -10 ,  size = 'small')
        else:
            message_to_screen('IT WAS A DRAW', light_red, -10 ,  size = 'small')
        pygame.display.update()
        sleep(sleep_time)
        message_to_screen('Do You Want To Play Again?', green, 20, 'small')
        while True:
            sleep(2.0 * sleep_time/3.0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            SizeOfTheButton = 3*gap + block_size // 2
            button('YES', 20, display_height - SizeOfTheButton - 20 , SizeOfTheButton, SizeOfTheButton,
                   green, light_green, 'restart')
            pygame.display.update()
            button('NO', display_width - SizeOfTheButton - 20, display_height - SizeOfTheButton - 20 , SizeOfTheButton,
                   SizeOfTheButton, red, light_red, 'quit')
            pygame.display.update()
            clock.tick(FPS)

def gameLoop_single_menu():
    reset()
    gameDisplay.fill(white)
    message_to_screen('WHICH PLAYER', red, 75 - display_height / 2, 'medium')
    message_to_screen('DO YOU WANT', red, 125 - display_height / 2, 'medium')
    message_to_screen('TO BE?', red, 175 - display_height / 2, 'medium')
    message_to_screen('X plays first', black, 225 - display_height / 2, 'small')
    while True:
        SizeOfTheButton = 3*gap + block_size // 2
        button('X', 20, display_height - SizeOfTheButton - 20 , SizeOfTheButton, SizeOfTheButton,
                   green, light_green, 'x')
        pygame.display.update()
        button('O', display_width - SizeOfTheButton - 20, display_height - SizeOfTheButton - 20 , SizeOfTheButton,
                   SizeOfTheButton, green, light_green, 'o')
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        pygame.display.update()
        clock.tick(FPS)

def gameLoop_single():
    global cells
    sleep(sleep_time)
    gameDisplay.fill(white)
    reset()
    message_to_screen('Player 1 = X, Player 2 = O', black, display_height/2 - 10)
    drawGrid()
    turn = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if turn % 2 != comp_turn % 2:
            for x in range(3):
                for y in range(3):
                    turn = pressButton(turn, [x, y], block_size)
        pygame.display.update()
        gameOver(True, 'player')
        if turn % 2 == comp_turn % 2:
            y, x = compPlay()
            cells[y][x] = comp_turn
            if turn % 2 == 0:
                drawCross(gridLoc[x][y][0], gridLoc[x][y][1], block_size)
            else:
                drawCircle(gridLoc[x][y][0], gridLoc[x][y][1], block_size//2)
            turn += 1
        pygame.display.update()
        gameOver(True, 'comp')
        clock.tick(FPS)

def gameLoop_multi():
    sleep(sleep_time)
    gameDisplay.fill(white)
    reset()
    message_to_screen('Player 1 = X, Player 2 = O', black, display_height/2 - 10)
    drawGrid()
    turn = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        for x in range(3):
            for y in range(3):
                turn = pressButton(turn, [x, y], block_size)
        pygame.display.update()
        gameOver()
        clock.tick(FPS)

def gameStart():
    gameDisplay.fill(white)
    message_to_screen('TIC TAC TOE', red, 60 - display_height/2, 'medium')
    while True:
        button('SINGLE PLAYER', 40, 160, display_width - 80, 60, green, light_green, action = 'single')
        button('MULTI PLAYER', 40, 260, display_width - 80, 60, green, light_green, action = 'play')
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        clock.tick(FPS)
#-------------------------

#Artificial Intelligence--
def winPosition(player):
    for x in range(3):
        if cells[x][0] == cells[x][1] == player and cells[x][2] == False:
            return (x, 2)
        elif cells[x][0] == cells[x][2] == player and cells[x][1] == False:
            return (x, 1)
        elif cells[x][2] == cells[x][1] == player and cells[x][0] == False:
            return (x, 0)
    for x in range(3):
        if cells[0][x] == cells[1][x] == player and cells[2][x] == False:
            return (2, x)
        elif cells[0][x] == cells[2][x] == player and cells[1][x] == False:
            return (1, x)
        elif cells[2][x] == cells[1][x] == player and cells[0][x] == False:
            return (0, x)
    if cells[0][0] == cells[1][1] == player and cells[2][2] == False:
        return (2, 2)
    elif cells[0][0] == cells[2][2] == player and cells[1][1] == False:
        return (1, 1)
    elif cells[1][1] == cells[2][2] == player and cells[0][0] == False:
        return (0, 0)
    if cells[0][2] == cells[1][1] == player and cells[2][0] == False:
        return (2, 0)
    elif cells[0][2] == cells[2][0] == player and cells[1][1] == False:
        return (1, 1)
    elif cells[1][1] == cells[2][0] == player and cells[0][2] == False:
        return (0, 2)
    return False

def compPlay():
    comp_win_pos = winPosition(comp_turn)
    player_win_pos = winPosition(1 if comp_turn % 2 == 0 else 2) 
    if comp_win_pos: return comp_win_pos    #Check if computer can win
    if player_win_pos: return player_win_pos    #Check if human(?) player can win
    if cells[1][1] == False: return (1, 1)
    from random import choice   #to randomize the computer's move
    edges_bool = list()
    corners_bool = list()
    if cells[0][2] == False: corners_bool.append((0, 2))
    if cells[2][0] == False: corners_bool.append((2, 0))
    if cells[0][0] == False: corners_bool.append((0, 0))
    if cells[2][2] == False: corners_bool.append((2, 2))
    if cells[0][1] == False: edges_bool.append((0, 1))
    if cells[1][0] == False: edges_bool.append((1, 0))
    if cells[2][1] == False: edges_bool.append((2, 1))
    if cells[1][2] == False: edges_bool.append((1, 2))
    if len(corners_bool) != 0: return choice(corners_bool)
    if len(edges_bool) != 0: return choice(edges_bool)
#-------------------------

#Actual Game Play---------
gameStart()
#-------------------------



