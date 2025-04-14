"""
Hello World
"""
import pygame as p

import ChessEngine, ChessDeterminer
import Moves


width = 512
height = 512
dimension = 8 #dimension of a chessboard
square_size = height // dimension
mx_fps = 200
img = {}
#C:\AI_CHESS_BOT\AI-chess-bot\images\bB.png
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
    p.display.set_caption("Center-Aligned Text")
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = ChessEngine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = False #flag variable for when a move is made
    animate = False
    load_images()
    running = True
    selected_square = () #no square selected , keep track of the last click of user (tuple: (row, col))
    player_click = [] #keep track of player clicks (two tuples: [(6, 4), (4, 4)]
    game_over = False
    human_player = True #human player
    ai_player = False #AI player turn
    while running:
        human_turn = (game_state.whiteToMove and human_player) or (not game_state.whiteToMove and ai_player)
        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
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
                        move = Moves.Move(player_click[0], player_click[1],game_state.board)
                        print(move.get_chess_notation()) #prints move made

                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                game_state.make_move(valid_moves[i])
                                move_made = True
                                animate = True
                                selected_square = ()  # reset user clicks
                                player_click = []
                        if not move_made:
                            player_click = [selected_square]

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    game_state.undo_move()
                    move_made = True
                    animate = False
                    game_over = False
                if e.key == p.K_r:
                    game_state = ChessEngine.GameState()
                    valid_moves = game_state.get_valid_moves()
                    selected_square = ()
                    player_click = []
                    move_made = False
                    animate = False
                    game_over = False

        if not game_over and not human_turn:
            ai_moves = ChessDeterminer.find_best_move_minmax(game_state, valid_moves)
            if ai_moves is None:
                ai_moves = ChessDeterminer.random_moves(valid_moves)
            game_state.make_move(ai_moves)
            move_made = True
            animate = True

        if move_made:
            if animate:
                animate_move(screen, game_state.board, game_state.moveLog[-1], clock)
            valid_moves = game_state.get_valid_moves()
            move_made = False
            animate = False

        draw_game_state(screen, game_state, valid_moves, selected_square)

        if game_state.count_moves == 0 :
            game_over = True
            winner = ''
            if game_state.stale_mate:
                winner += "Stalemate, "
            elif game_state.check_mate:
                winner += "Checkmate, "
            winner += "White" if not game_state.whiteToMove else "Black"
            draw_text(screen, winner + " wins!!")


        clock.tick(mx_fps)
        p.display.flip()
def draw_text(screen, text):
    font = p.font.SysFont("Algeria", 32, True, False)
    text_object = font.render(text, 0, p.Color('Gray'))
    text_location = p.Rect(0, 0, width, height).move(width/2 - text_object.get_width()/2, height/2 - text_object.get_height()/2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, p.Color('Black'))
    screen.blit(text_object, text_location.move(2, 2))


def animate_move(screen, board ,move_made, clock):
    global colours
    dr = move_made.end_row - move_made.start_row
    dc = move_made.end_col - move_made.start_col
    frame_per_square = 5
    frame_count = (abs(dr) + abs(dc)) * frame_per_square
    for frame in range(frame_count + 1):
        r, c = (move_made.start_row + dr * frame/ frame_count, move_made.start_col + dc * frame/ frame_count)
        draw_board(screen)
        draw_pieces(screen, board)
        colour = colours[(move_made.end_row + move_made.end_col) % 2]
        end_square = p.Rect(move_made.end_col * square_size, move_made.end_row * square_size,
                            square_size, square_size)
        p.draw.rect(screen, colour, end_square)
        if move_made.piece_captured != "--":
            screen.blit(img[move_made.piece_captured], end_square)
        screen.blit(img[move_made.piece_move], p.Rect(c * square_size, r * square_size, square_size, square_size))
        p.display.flip()
        clock.tick(mx_fps)


    # piece = game_state.board[move_made.start_row][move_made.start_col]




def highlight_squares(screen, game_state, valid_moves_list, square_selected):
    if square_selected != ():
        r, c = square_selected
        if game_state.board[r][c][0] == ('w' if game_state.whiteToMove else 'b'):
            s = p.Surface((square_size, square_size))
            s.set_alpha(100) #transparency value: if 0 - transparent else 255 - opaque
            s.fill(p.Color('yellow'))
            screen.blit(s, (c * square_size, r * square_size))
            s.fill(p.Color('green'))
            for moves in valid_moves_list:
                if moves.start_row == r and moves.start_col == c:
                    screen.blit(s, (moves.end_col * square_size, moves.end_row * square_size))


def draw_game_state(screen, game_state, valid_moves_list, selected_square):
    draw_board(screen) #draw squares on Board
    highlight_squares(screen, game_state, valid_moves_list, selected_square)
    draw_pieces(screen, game_state.board) #draw piece on the squares


def draw_board(screen):
    global colours
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