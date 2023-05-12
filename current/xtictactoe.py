import pygame, sys
 
pygame.init()
 
WIDTH, HEIGHT = 900, 900
 
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe!")

BG_COLOR = (214, 201, 227)
CIRCLE_RADIUS = 100
LINE_WIDTH = 10
CIRCLE_COLOR = (0, 0, 255)
CROSS_COLOR = (255, 0, 0)
WIN_COLOR = (0, 255, 0)

board = [[None, None, None], [None, None, None], [None, None, None]]

to_move = 'X'
game_finished = False

def draw_board():
    """
    Draws the Tic Tac Toe board on the screen.
    """
    SCREEN.fill(BG_COLOR)
    pygame.draw.line(SCREEN, (0, 0, 0), (WIDTH/3, 0), (WIDTH/3, HEIGHT), LINE_WIDTH)
    pygame.draw.line(SCREEN, (0, 0, 0), (2*WIDTH/3, 0), (2*WIDTH/3, HEIGHT), LINE_WIDTH)
    pygame.draw.line(SCREEN, (0, 0, 0), (0, HEIGHT/3), (WIDTH, HEIGHT/3), LINE_WIDTH)
    pygame.draw.line(SCREEN, (0, 0, 0), (0, 2*HEIGHT/3), (WIDTH, 2*HEIGHT/3), LINE_WIDTH)

def draw_circle(row, col):
    """
    Draws a blue circle at the specified row and column.
    """
    center_x = int(col * WIDTH/3 + WIDTH/6)
    center_y = int(row * HEIGHT/3 + HEIGHT/6)
    pygame.draw.circle(SCREEN, CIRCLE_COLOR, (center_x, center_y), CIRCLE_RADIUS, LINE_WIDTH)

def draw_cross(row, col):
    """
    Draws a red cross at the specified row and column.
    """
    x1 = int(col * WIDTH/3 + WIDTH/6 - CIRCLE_RADIUS)
    y1 = int(row * HEIGHT/3 + HEIGHT/6 - CIRCLE_RADIUS)
    x2 = int(col * WIDTH/3 + WIDTH/6 + CIRCLE_RADIUS)
    y2 = int(row * HEIGHT/3 + HEIGHT/6 + CIRCLE_RADIUS)
    pygame.draw.line(SCREEN, CROSS_COLOR, (x1, y1), (x2, y2), LINE_WIDTH)
    x1 = int(col * WIDTH/3 + WIDTH/6 + CIRCLE_RADIUS)
    y1 = int(row * HEIGHT/3 + HEIGHT/6 - CIRCLE_RADIUS)
    x2 = int(col * WIDTH/3 + WIDTH/6 - CIRCLE_RADIUS)
    y2 = int(row * HEIGHT/3 + HEIGHT/6 + CIRCLE_RADIUS)
    pygame.draw.line(SCREEN, CROSS_COLOR, (x1, y1), (x2, y2), LINE_WIDTH)

def get_winner():
    """
    Checks if there is a winner and returns their symbol (X or O).
    Returns None if there is no winner yet.
    """
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] is not None:
            return board[row][0]

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

    # No winner yet
    return None

def end_game():
    """
    Displays the winner (or a tie) on the screen and resets the board.
    """
    winner = get_winner()
    if winner is None:
        font = pygame.font.SysFont(None, 100)
        message = font.render("Tie!", True, WIN_COLOR)
    elif winner == 'X':
        font = pygame.font.SysFont(None, 100)
        message = font.render("X wins!", True, WIN_COLOR)
    else:
        font = pygame.font.SysFont(None, 100)
        message = font.render("O wins!", True, WIN_COLOR)

    SCREEN.blit(message, (int(WIDTH/2 - message.get_rect().width/2), int(HEIGHT/2 - message.get_rect().height/2)))
    pygame.display.update()

    # Reset board
    for row in range(3):
        for col in range(3):
            board[row][col] = None

    pygame.time.wait(2000) # Wait for 2 seconds before resetting the board

    draw_board()
    pygame.display.update()

draw_board()
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_finished:
        try:
            user_input = input("Enter coordinates as row,col: ")
            row, col = map(int, user_input.strip().split(','))
            if row < 0 or row > 2 or col < 0 or col > 2:
                print("Invalid input, please enter values between 0 and 2.")
                continue
            elif board[row][col] is not None:
                print("That square is already taken! Try another one.")
                continue
            else:
                if to_move == 'O':
                    draw_circle(row, col)
                else:
                    draw_cross(row, col)
                    
                board[row][col] = to_move
                    
                if get_winner() is not None:
                    game_finished = True
                    end_game()
                else:
                    if to_move == 'O':
                        to_move = 'X'
                    else:
                        to_move = 'O'

                pygame.display.update()

        except ValueError:
            print("Invalid input, please enter values separated by a comma.")