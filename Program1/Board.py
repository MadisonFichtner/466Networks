import array

def create_empty_board(self):
    for x in range(10):
        self.append(["_"] * 10)
    return self


def print_board(self):
    for row in self:
        print(" ".join(row))


def update_board(self, x, y):
    file = open("own_board.txt","r")
    f1 = file.readlines()
    #for x in f1:
        #print(x)
    #self[x][y] = "X"
    #return self

def read_board(self):
    return 0
