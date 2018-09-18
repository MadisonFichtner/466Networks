import array

def create_empty_board(self):
    for x in range(10):
        self.append(["_"] * 10)
    return self


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

def check_board(board, x, y):
    if board[x][y] == '_':
        print("MISS")
    

def read_board(self):
    return 0
