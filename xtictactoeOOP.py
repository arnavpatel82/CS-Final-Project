import pygame
import sys

class TicTacToe:
    def __init__(self, width=900, height=900):
        pygame.init()

        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tic Tac Toe!")

        self.bg_color = (214, 201, 227)
        self.circle_radius = 100
        self.line_width = 10
        self.circle_color = (0, 0, 255)
        self.cross_color = (255, 0, 0)
        self.win_color = (0, 255, 0)

        self.board = [[None, None, None], [None, None, None], [None, None, None]]

        self.to_move = 'X'
        self.game_finished = False

        self.font = pygame.font.SysFont(None, 100)

    def draw_board(self):
        """
        Draws the Tic Tac Toe board on the screen.
        """
        self.screen.fill(self.bg_color)
        pygame.draw.line(self.screen, (0, 0, 0), (self.width/3, 0), (self.width/3, self.height), self.line_width)
        pygame.draw.line(self.screen, (0, 0, 0), (2*self.width/3, 0), (2*self.width/3, self.height), self.line_width)
        pygame.draw.line(self.screen, (0, 0, 0), (0, self.height/3), (self.width, self.height/3), self.line_width)
        pygame.draw.line(self.screen, (0, 0, 0), (0, 2*self.height/3), (self.width, 2*self.height/3), self.line_width)

    def draw_circle(self, row, col):
        """
        Draws a blue circle at the specified row and column.
        """
        center_x = int(col * self.width/3 + self.width/6)
        center_y = int(row * self.height/3 + self.height/6)
        pygame.draw.circle(self.screen, self.circle_color, (center_x, center_y), self.circle_radius, self.line_width)

    def draw_cross(self, row, col):
        """
        Draws a red cross at the specified row and column.
        """
        x1 = int(col * self.width/3 + self.width/6 - self.circle_radius)
        y1 = int(row * self.height/3 + self.height/6 - self.circle_radius)
        x2 = int(col * self.width/3 + self.width/6 + self.circle_radius)
        y2 = int(row * self.height/3 + self.height/6 + self.circle_radius)
        pygame.draw.line(self.screen, self.cross_color, (x1, y1), (x2, y2), self.line_width)
        x1 = int(col * self.width/3 + self.width/6 + self.circle_radius)
        y1 = int(row * self.height/3 + self.height/6 - self.circle_radius)
        x2 = int(col * self.width/3 + self.width/6 - self.circle_radius)
        y2 = int(row * self.height/3 + self.height/6 + self.circle_radius)
        pygame.draw.line(self.screen, self.cross_color, (x1, y1), (x2, y2), self.line_width)

    def get_winner(self):
        """
        Checks if there is a winner and returns their symbol (X or O).
        Returns None if there is no winner yet.
        """
        # Check rows
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] and self.board[row][0] is not None:
                return self.board[row][0]

        # Check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] is not None:
                return self.board[0][col]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] is not None:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] is not None:
            return self.board[0][2]

        # No winner yet
        return None

    def end_game(self):
        """
        Displays the winner (or a tie) on the screen and resets the board.
        """
        winner = self.get_winner()
        if winner is None:
            message = self.font.render("Tie!", True, self.win_color)
        elif winner == 'X':
            message = self.font.render("X wins!", True, self.win_color)
        else:
            message = self.font.render("O wins!", True, self.win_color)

        self.screen.blit(message, (int(self.width/2 - message.get_rect().width/2), int(self.height/2 - message.get_rect().height/2)))
        pygame.display.update()

        self.game_finished = True
        
        pygame.time.wait(2000) # Wait for 2 seconds before resetting the board

        self.reset_board()
        self.draw_board()
        pygame.display.update()

    def reset_board(self):
        """
        Resets the board to its initial state.
        """
        self.board = [[None, None, None], [None, None, None], [None, None, None]]
        self.to_move = 'X'
        self.game_finished = False

    def run_game(self):
        """
        Runs the game loop.
        """
        self.draw_board()
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if not self.game_finished:
                move = input(f"{self.to_move}'s turn. Enter row,column (ex. 0,2): ")
                if move == 'q':
                    pygame.quit()
                    break
                try:
                    row, col = move.split(',')
                    row, col = int(row), int(col)
                except:
                    print("Invalid input. Please try again.")
                    continue

                if row < 0 or row > 2 or col < 0 or col > 2:
                    print("Invalid input. Please try again.")
                    continue

                if self.board[row][col] is not None:
                    print("That space is already taken. Please try again.")
                    continue

                if self.to_move == 'O':
                    self.draw_circle(row, col)
                else:
                    self.draw_cross(row, col)

                self.board[row][col] = self.to_move

                winner = self.get_winner()
                if winner is not None:
                    self.end_game()
                elif all(all(row) for row in self.board):
                    self.end_game()
                else:
                    self.to_move = 'O' if self.to_move == 'X' else 'X'

            pygame.display.update()

if __name__ == '__main__':
    game = TicTacToe()
    game.run_game()