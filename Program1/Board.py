import array
import sys

def create_empty_board(self):
    for x in range(10):
        self.append(["_"] * 10)
    return self

def own_board(own):
    create_empty_board(own)
    own[0][0] = 'C'
    own[0][1] = 'C'
    own[0][2] = 'C'
    own[0][3] = 'C'
    own[0][4] = 'C'

    own[1][0] = 'B'
    own[1][1] = 'B'
    own[1][2] = 'B'
    own[1][3] = 'B'

    own[2][0] = 'R'
    own[2][1] = 'R'
    own[2][2] = 'R'

    own[3][0] = 'S'
    own[3][1] = 'S'
    own[3][2] = 'S'

    own[4][0] = 'D'

    own[5][0] = 'D'



def print_board(self):
    for row in self:
        print(" ".join(row))


def update_board(board, x, y, update):
    file = open("own_board.txt","r")
    f1 = file.readlines()
    #for x in f1:
        #print(x)
    #self[x][y] = "X"
    #return self
    if update == 1: # hit
        board[x][y] = 'C' # the letter of ship
    elif update == 2: # miss
        board[x][y] = 'M'
    elif update == 3: # sink
        board[x][y] = 'S'
    else:
        print("UPDATE: something is wrong")
    

def read_board(board, i, j):
    print("IN READ BOARD")
    with open(board) as textFile:
        lines = [line.split() for line in textFile]
    file = open(board, "w")
    length = len(lines)
    var = lines[i][j]
    print("var: ", var)
    # for i in range(length):
        # for j in range(length):
            #print(lines[i][j])
            # var = lines[i][j]

    file.close()
    # return var

