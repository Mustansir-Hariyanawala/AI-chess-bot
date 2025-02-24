"""
Hello World
"""
import pygame as p
import ChessEngine

print(dir())
width = 512
height = 512
dimension = 8 #dimension of a chessboard
square_size = height // dimension
mx_fps = 15
img = {}

"""
initialize global dictionary of images. This will be called
"""

def load_images():
    pieces = ['bB', 'bK','bN', 'bQ', 'bR','bp', 'wB', 'wK','wN','wQ','wR','wp']
    for piece in pieces:
        img[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"),
                                       (square_size, square_size))

def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = ChessEngine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False #flag variable for when a move is made
    load_images()
    running = True
    selected_square = () #no square selected , keep track of the last click of user (tuple: (row, col))
    player_click = [] #keep track of player clicks (two tuples: [(6, 4), (4, 4)]

    while running:
        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                position = p.mouse.get_pos() #(x, y)
                col = position[0]//square_size
                row = position[1]//square_size
                if selected_square == (row, col): #the user clicked same square twice
                    selected_square = ()
                    player_click = [] #clear player clicks

                else:
                    selected_square = (row, col)
                    player_click.append(selected_square) #append for both 1st and 2nd clicks
                if len(player_click) == 2: #after 2nd click
                    move = ChessEngine.Move(player_click[0], player_click[1], game_state.board)
                    print(move.get_chess_notation()) #prints move made

                    if move in valid_moves:
                        game_state.make_move(move)
                        move_made = True
                    selected_square = () #reset user clicks
                    player_click = []

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    game_state.undo_move()
                    move_made = True

        if move_made:
            valid_moves = game_state.get_valid_moves()
            move_made = False;
        draw_game_state(screen, game_state)
        clock.tick(mx_fps)
        p.display.flip()

def draw_game_state(screen, game_state):
    draw_board(screen) #draw squares on Board
    draw_pieces(screen, game_state.board) #draw piece on the squares


def draw_board(screen):
    colours = [p.Color("white"), p.Color('Grey')]
    for row in range(dimension):
        for col in range(dimension):
            colour = colours[((row + col) % 2)] #optimal solution;
            p.draw.rect(screen, colour, p.Rect(col * square_size,
                                               row * square_size,
                                               square_size,
                                               square_size))
"""
used to draw pieces on the board. The reason we are not adding draw_pieces content
within draw_board is because we will had highlights.
"""
def draw_pieces(screen, game_state):
    for row in range(dimension):
        for col in range(dimension):
            piece = game_state[row][col]
            if piece != "--":
                screen.blit(img[piece], p.Rect(col * square_size,
                                           row * square_size,
                                           square_size,
                                           square_size))



if __name__ == "__main__":
    main()