import array

def create_empty_board(self):
    for x in range(10):
        self.append(["_"] * 10)
    return self


def print_board(self):
    for row in self:
        print(" ".join(row))


def update_board(self, x, y):
    self[x][y] = "X"
    return self
