import pygame

import board as b

pygame.init()

display_size = (800, 800)



gameDisplay = pygame.display.set_mode(display_size)
pygame.display.set_caption("Dark Chess")
clock = pygame.time.Clock()

lightSquareImg = pygame.image.load('sprites/light_square.png')
darkSquareImg = pygame.image.load("sprites/dark_square.png")
whitePawnImg = pygame.image.load("sprites/white_pawn.png")
blackPawnImg = pygame.image.load("sprites/black_pawn.png")
whiteKnightImg = pygame.image.load("sprites/white_knight.png")
blackKnightImg = pygame.image.load("sprites/black_knight.png")
whiteBishopImg = pygame.image.load("sprites/white_bishop.png")
blackBishopImg = pygame.image.load("sprites/black_bishop.png")
whiteRookImg = pygame.image.load("sprites/white_rook.png")
blackRookImg = pygame.image.load("sprites/black_rook.png")
whiteQueenImg = pygame.image.load("sprites/white_queen.png")
blackQueenImg = pygame.image.load("sprites/black_queen.png")
whiteKingImg = pygame.image.load("sprites/white_king.png")
blackKingImg = pygame.image.load("sprites/black_king.png")
fogImg = pygame.image.load("sprites/fog.png")
whiteTurnImg = pygame.image.load("sprites/white_turn.png")
blackTurnImg = pygame.image.load("sprites/black_turn.png")


def pieceImage(p):
    if p == 'f':
        return fogImg
    elif p == 'P':
        return whitePawnImg
    elif p == 'p':
        return blackPawnImg
    elif p == 'N':
        return whiteKnightImg
    elif p == 'n':
        return blackKnightImg
    elif p == 'B':
        return whiteBishopImg
    elif p == 'b':
        return blackBishopImg
    elif p == 'R':
        return whiteRookImg
    elif p == 'r':
        return blackRookImg
    elif p == 'Q':
        return whiteQueenImg
    elif p == 'q':
        return blackQueenImg
    elif p == 'K':
        return whiteKingImg
    elif p == 'k':
        return blackKingImg
    elif p == None:
        return None
    else:
        quit()


def setLight(x, y):
    gameDisplay.blit(lightSquareImg, (100 * x, 100 * y))


def setDark(x, y):
    gameDisplay.blit(darkSquareImg, (100 * x, 100 * y))


def putPiece(piece, x, y):
    sprite = pieceImage(piece)
    if sprite != None:
        gameDisplay.blit(sprite, (100 * x, 100 * y))

def putTurn(color):
    sprite = None
    if color is 'w':
        sprite = whiteTurnImg
    elif color is 'b':
        sprite = blackTurnImg
    if sprite is not None:
        gameDisplay.blit(sprite, (0, 0))


def showBoard(bd):
    setLight(0, 0)
    setLight(0, 2)
    setLight(0, 4)
    setLight(0, 6)
    setLight(1, 1)
    setLight(1, 3)
    setLight(1, 5)
    setLight(1, 7)
    setLight(2, 0)
    setLight(2, 2)
    setLight(2, 4)
    setLight(2, 6)
    setLight(3, 1)
    setLight(3, 3)
    setLight(3, 5)
    setLight(3, 7)
    setLight(4, 0)
    setLight(4, 2)
    setLight(4, 4)
    setLight(4, 6)
    setLight(5, 1)
    setLight(5, 3)
    setLight(5, 5)
    setLight(5, 7)
    setLight(6, 0)
    setLight(6, 2)
    setLight(6, 4)
    setLight(6, 6)
    setLight(7, 1)
    setLight(7, 3)
    setLight(7, 5)
    setLight(7, 7)
    setDark(1, 0)
    setDark(1, 2)
    setDark(1, 4)
    setDark(1, 6)
    setDark(0, 1)
    setDark(0, 3)
    setDark(0, 5)
    setDark(0, 7)
    setDark(3, 0)
    setDark(3, 2)
    setDark(3, 4)
    setDark(3, 6)
    setDark(2, 1)
    setDark(2, 3)
    setDark(2, 5)
    setDark(2, 7)
    setDark(5, 0)
    setDark(5, 2)
    setDark(5, 4)
    setDark(5, 6)
    setDark(4, 1)
    setDark(4, 3)
    setDark(4, 5)
    setDark(4, 7)
    setDark(7, 0)
    setDark(7, 2)
    setDark(7, 4)
    setDark(7, 6)
    setDark(6, 1)
    setDark(6, 3)
    setDark(6, 5)
    setDark(6, 7)
    for i in range(64):
        piece = bd.getPieceFromIndex(i)
        coord = b.coordOfIndex(i)
        x = coord[0]
        y = coord[1]
        putPiece(piece, x, y)
    putTurn(globalBoard.colorToMove())
    bd.altered = False

globalBoard = None

posOrigin = (0, 0)
posTarget = (0, 0)


def pixelToSquare(pixPos):
    return int(pixPos[0] / 100), int(pixPos[1] / 100)


def setOrigin(mousePos):
    global posOrigin
    posOrigin = pixelToSquare(mousePos)
    print("origin set:", posOrigin)


def setTarget(mousePos):
    global posTarget
    posTarget = pixelToSquare(mousePos)
    print("target set:", posTarget)


def executeMove():
    print("invoke move:", posOrigin, "->", posTarget)
    globalBoard.move(posOrigin, posTarget, sendToPartner=True)


colorChoice = input("color (b/w):")
globalBoard = b.Board(colorChoice)

showBoard(globalBoard)
pygame.display.update()

crashed = False
while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            setOrigin(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
            setTarget(pygame.mouse.get_pos())
            executeMove()
            showBoard(globalBoard)
            pygame.display.update()

    # refresh (opponents moves) when display is behind board class
    if globalBoard.altered:
        showBoard(globalBoard)
    pygame.display.update()
    clock.tick(60)

pygame.quit()

quit()
