import connection

visibility = {'w': "PNBRQK", 'b': "pnbrqk"}


def coordToIndex(coord):
    index = 8 * (7 - coord[1]) + coord[0]
    return index


def coordOfIndex(index):
    x = index % 8
    y = int(index / 8)
    y = 7 - y
    return x, y


def coordOnBoard(coords):
    if coords[0] in range(8) and coords[1] in range(8):
        return True
    else:
        return False


def zwischensquares(move):
    x1, y1 = move[0]
    x2, y2 = move[1]

    move_list = []

    if (x1, y1) == (x2, y2):
        return []

    # straight moves
    elif x1 == x2:
        direction = int(y2 - y1)
        direction = int( direction / abs(direction) )
        for y in range(y1+direction, y2, direction):
            move_list.append((x1,y))
    elif y1 == y2:
        direction = int(x2 - x1)
        direction = int(direction / abs(direction))
        for x in range(x1+direction, x2, direction):
            move_list.append((x, y1))

    # diagonal moves
    elif abs(x1-x2) == abs(y1-y2):
        print("DIAGONAL")
        dx = int(x2-x1)
        dy = int(y2-y1)
        direction = (int(dx/abs(dx)), int(dy/abs(dy)))
        x = x1 + direction[0]
        y = y1 + direction[1]
        print("DIRECTION:",direction)
        while x != x2 and y != y2:
            move_list.append((x,y))
            x += direction[0]
            y += direction[1]
        print("DIAGONAL END")

    # knight moves and illegal moves: return no zwischensquares
    else:
        return []

    return move_list


class Board:
    def __init__(self, color):
        if color not in ['b', 'w']:
            print("invalid color")
            quit()
        self.color = color
        if color == 'w':
            self.altered = True
        else:
            self.altered = False

        self.board = [None] * 64
        self.visiboard = [0] * 64

        self.board[0] = 'R'
        self.board[1] = 'N'
        self.board[2] = 'B'
        self.board[3] = 'Q'
        self.board[4] = 'K'
        self.board[5] = 'B'
        self.board[6] = 'N'
        self.board[7] = 'R'
        self.board[8] = 'P'
        self.board[9] = 'P'
        self.board[10] = 'P'
        self.board[11] = 'P'
        self.board[12] = 'P'
        self.board[13] = 'P'
        self.board[14] = 'P'
        self.board[15] = 'P'
        self.board[48] = 'p'
        self.board[49] = 'p'
        self.board[50] = 'p'
        self.board[51] = 'p'
        self.board[52] = 'p'
        self.board[53] = 'p'
        self.board[54] = 'p'
        self.board[55] = 'p'
        self.board[56] = 'r'
        self.board[57] = 'n'
        self.board[58] = 'b'
        self.board[59] = 'q'
        self.board[60] = 'k'
        self.board[61] = 'b'
        self.board[62] = 'n'
        self.board[63] = 'r'

        # setup input socket
        if self.color is 'w':
            port = 60000
        else:
            port = 60001
        self.tIn = connection.RecvThread(port, self.recv_callback)
        self.tIn.start()

        self.reilluminate()


    # connection callback
    def recv_callback(self, data):
        temp = data.split()
        origin = (int(temp[0]), int(temp[1]))
        target = (int(temp[2]), int(temp[3]))
        self.move(origin, target, sendToPartner=False)

    def move(self, origin, target, sendToPartner=False):

        # allowing to cancel picking up a piece
        if origin == target:
            print("move cancelled")
            return

        # track changes of received moves
        self.altered = not sendToPartner
        print("checking move:", origin, "->", target)

        # stop on first obstacles
        zwsq = zwischensquares((origin, target))
        print("zwischensquares:", zwsq)
        for square in zwischensquares((origin, target)):
            if self.board[coordToIndex(square)] is not None:
                target = square
                break

        # send move to other playert
        if sendToPartner is True:
            print("sending move to partner")
            if self.color is 'w':
                port = 60001  # black recieves on port 60001, so white sends there
            else:
                port = 60000
            tOut = connection.SendThread(connection.ipPartner, port)
            tOut.set_move(origin, target)  # store the move to be send in object
            tOut.start()  # send the stored move

        # move pieces
        indOrigin = coordToIndex(origin)
        indTarget = coordToIndex(target)
        self.board[indTarget] = self.board[indOrigin]
        self.board[indOrigin] = None
        self.reilluminate()

    def reilluminate(self):
        self.visiboard = [False] * 64
        appendList = []
        for i in range(64):
            if self.board[i] is not None and self.board[i] in visibility[self.color]:
                self.visiboard[i] = True
                x, y = coordOfIndex(i)
                # shine with 1 square distance
                appendList.append((x - 1, y - 1))
                appendList.append((x - 1, y))
                appendList.append((x - 1, y + 1))
                appendList.append((x, y - 1))
                appendList.append((x, y + 1))
                appendList.append((x + 1, y - 1))
                appendList.append((x + 1, y))
                appendList.append((x + 1, y + 1))
        # remove shine out of any field
        for coord in appendList:
            if coord[0] in range(8) and coord[1] in range(8):
                self.visiboard[coordToIndex(coord)] = True

    def colorToMove(self):
        otherColor = {'w': 'b', 'b': 'w'}
        if self.altered:
            return self.color
        else:
            return otherColor[self.color]


    def getPieceFromIndex(self, index):
        if self.visiboard[index] == True:
            return self.board[index]
        else:
            return 'f'

    def consoleOut(self):
        for x in range(8):
            s = ""
            for y in range(8):
                index = coordToIndex((x, y))
                if self.board[index] == None:
                    s += " "
                else:
                    s += self.board[index]
            print(s)
