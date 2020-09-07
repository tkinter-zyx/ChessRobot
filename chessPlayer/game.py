class Game:  # 由于图像识别的限制,固定电脑方为白子后手,玩家方为黑子先手
    def __init__(self, size=(6, 6)):  # 传入棋盘大小元组:行数x列数
        self.size = size
        self.board = []
        # 初始化棋盘,0为空,1为白子,-1为黑子
        for i in range(size[0]):
            self.board.append([])
            for j in range(size[1]):
                self.board[i].append(0)
        self._visited = []
        self.win = 0

    def _search(self, coord, way, linknum):  # 传入本次搜索的中心与连接方式,0为横,1为竖,2为/,3为\,-1为首个中心棋子
        self._visited.append(coord)
        linknum += 1
        if linknum >= 5:
            self.win = 1
        try:
            if self.board[coord[0]][coord[1]] == self.board[coord[0]][coord[1] - 1] and (way == 0 or way == -1) and (
            coord[0], coord[1] - 1) not in self._visited:
                self._search((coord[0], coord[1] - 1), 0, linknum)
        except IndexError:
            pass
        try:
            if self.board[coord[0]][coord[1]] == self.board[coord[0]][coord[1] + 1] and (way == 0 or way == -1) and (
            coord[0], coord[1] + 1) not in self._visited:
                self._search((coord[0], coord[1] - 1), 0, linknum)
        except IndexError:
            pass
        try:
            if self.board[coord[0]][coord[1]] == self.board[coord[0] + 1][coord[1]] and (way == 1 or way == -1) and (
                coord[0] + 1, coord[1]) not in self._visited:
                self._search((coord[0] + 1, coord[1]), 1, linknum)
        except IndexError:
            pass
        try:
            if self.board[coord[0]][coord[1]] == self.board[coord[0] - 1][coord[1]] and (way == 1 or way == -1) and (
                coord[0] - 1, coord[1]) not in self._visited:
                self._search((coord[0] - 1, coord[1]), 1, linknum)
        except IndexError:
            pass
        try:
            if self.board[coord[0]][coord[1]] == self.board[coord[0] + 1][coord[1] - 1] and (
                    way == 2 or way == -1) and (coord[0] + 1, coord[1] - 1) not in self._visited:
                self._search((coord[0] + 1, coord[1] - 1), 2, linknum)
        except IndexError:
            pass
        try:
            if self.board[coord[0]][coord[1]] == self.board[coord[0] - 1][coord[1] + 1] and (
                    way == 2 or way == -1) and (coord[0] - 1, coord[1] + 1) not in self._visited:
                self._search((coord[0] - 1, coord[1] + 1), 2, linknum)
        except IndexError:
            pass
        try:
            if self.board[coord[0]][coord[1]] == self.board[coord[0] - 1][coord[1] - 1] and (
                    way == 3 or way == -1) and (coord[0] - 1, coord[1] - 1) not in self._visited:
                self._search((coord[0] - 1, coord[1] - 1), 3, linknum)
        except IndexError:
            pass
        try:
            if self.board[coord[0]][coord[1]] == self.board[coord[0] + 1][coord[1] + 1] and (
                    way == 3 or way == -1) and (coord[0] + 1, coord[1] + 1) not in self._visited:
                self._search((coord[0] + 1, coord[1] + 1), 3, linknum)
        except IndexError:
            pass
        return 0

    def if_win(self):  # 1为白子胜,-1为黑子胜,0为未结束
        self._visited = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 1 and (i, j) not in self._visited:
                    self._search((i, j), -1, 0)
                    if self.win:
                        self.win = 0
                        return 1
                if self.board[i][j] == -1 and (i, j) not in self._visited:
                    self._search((i, j), -1, 0)
                    if self.win:
                        self.win = 0
                        return -1
        return 0

    def _filter(self, board, kernel):
        # 传入原始棋盘与卷积核,返回处理后的棋盘
        import copy
        # 棋盘外围补0为卷积做准备
        board = copy.deepcopy(board)
        new_line = []
        for i in range(len(board[0])):
            new_line.append(0)
        board.append(copy.deepcopy(new_line))
        board.insert(0, new_line)
        for j in range(len(board)):
            board[j].insert(0, 0)
            board[j].append(0)

        res = []
        for i in range(len(board) - 2):
            line = []
            for j in range(len(board[0]) - 2):
                value = 0
                for a in range(len(kernel)):
                    for b in range(len(kernel[0])):
                        value += board[i + a][j + b] * kernel[a][b]
                line.append(value)
            res.append(line)
        return res

    def grade(self, board):
        # 传入要评估的棋盘,返回白子(算法方)的估值
        kernels = {
            'kernel_0': [[0, 0, 0],
                         [1, 1, 1],
                         [0, 0, 0]],
            'kernel_1': [[0, 1, 0],
                         [0, 1, 0],
                         [0, 1, 0]],
            'kernel_2': [[0, 0, 1],
                         [0, 1, 0],
                         [1, 0, 0]],
            'kernel_3': [[1, 0, 0],
                         [0, 1, 0],
                         [0, 0, 1]]
        }  # 定义卷积核
        point = 0
        for kernel in kernels.values():
            res = self._filter(self._filter(board, kernel), kernel)
            print('res:')
            self.show_board(res)
            for i in range(len(res)):
                for j in range(len(res[0])):
                    if res[i][j] >= 2:
                        point += j * 100 + 5 / ((i - self.size[0] / 2) ** 2 + (j - self.size[0] / 2) ** 2)
        return point

    def ab_pruning(self, board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if not board[i][j]:
                    pass

    def drop(self, coord, color):  # 传入用户落子坐标,调用算法返回电脑落子坐标
        if color != 1 and color != -1 and self.board[coord[0]][coord[1]] == 0:
            raise ValueError
        self.board[coord[0]][coord[1]] = color

    def show_board(self, board=1):
        j = 0
        if board == 1:
            for i in self.board:
                print(i)
                j += 1
                if j == len(self.board):
                    print('')
        else:
            for i in board:
                print(i)
                j += 1
                if j == len(board):
                    print('')


test = Game()
# test.show_board()
test.drop((5, 1), 1)
test.drop((5, 2), 1)
test.drop((5, 3), 1)
# test.drop((5, 4), 1)
test.show_board()
# test.drop((5, 5), 1)
print(test.grade(test.board))
test.show_board()
# print(test.if_win())