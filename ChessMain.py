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
    load_images()
    draw_game_state(screen, game_state)
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

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