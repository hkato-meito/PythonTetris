import tkinter as tk
import random

class TetrisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("テトリス")
        
        self.canvas = tk.Canvas(self.root, width=300, height=600, bg='white')
        self.canvas.pack(pady=20)

        # キーボードイベントのバインド
        self.root.bind("<Key>", self.key_press)

        # ブロックの形状と色の定義
        self.shapes = [
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[1, 1, 0], [0, 1, 1]],
#            [[0, 1, 1], [1, 1]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 1, 1], [1, 0, 0]],
            [[1, 1, 1], [0, 0, 1]],
            [[1, 1, 1], [0, 1, 0]]
        ]
        self.colors = ['blue', 'red', 'green', 'yellow', 'orange', 'purple', 'cyan']

        # ゲームボードの初期化
        self.board = [[0 for _ in range(10)] for _ in range(20)]
        
        self.game_over = False  # 追加: ゲームオーバーの状態を追加
        self.score = 0  # 追加: スコアの初期化

        self.current_piece = self.new_piece()
        self.draw_piece()
        self.update_game()

    def place_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    if y + self.current_piece['y'] < 0 or self.board[y + self.current_piece['y']][x + self.current_piece['x']] != 0:
                        self.game_over = True
                        return
                    self.board[y + self.current_piece['y']][x + self.current_piece['x']] = self.current_piece['color']
        self.current_piece = self.new_piece()

    def collision(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    if y + self.current_piece['y'] > 19 or \
                       x + self.current_piece['x'] > 9 or \
                       x + self.current_piece['x'] < 0 or \
                       self.board[y + self.current_piece['y']][x + self.current_piece['x']] != 0:
                        return True
        return False

    def remove_line(self):
        lines_to_remove = []
        for y, row in enumerate(self.board):
            if all(row):
                lines_to_remove.append(y)
                self.score += 100  # スコアを増やす
        for y in lines_to_remove:
            del self.board[y]
            self.board.insert(0, [0 for _ in range(10)])
        if lines_to_remove:
            print(f"Score: {self.score}")  # スコアを表示
            
    def new_piece(self):
        shape = random.choice(self.shapes)
        color = random.choice(self.colors)
        x = (10 - len(shape[0])) // 2
        y = 0
        return {'shape': shape, 'color': color, 'x': x, 'y': y}

    def draw_piece(self):
        for y, row in enumerate(self.current_piece['shape']):
            for x, cell in enumerate(row):
                if cell:
                    self.canvas.create_rectangle(
                        (x + self.current_piece['x']) * 30,
                        (y + self.current_piece['y']) * 30,
                        (x + self.current_piece['x'] + 1) * 30,
                        (y + self.current_piece['y'] + 1) * 30,
                        fill=self.current_piece['color']
                    )

    def key_press(self, event):
        # キーボードイベントのハンドラ
        if event.keysym == "Left":
            self.move(-1)
        elif event.keysym == "Right":
            self.move(1)
        elif event.keysym == "Down":
            self.move_down()
        elif event.keysym == "space":
            self.rotate_piece()

    def move(self, dx):
        self.current_piece['x'] += dx
        if self.collision():
            self.current_piece['x'] -= dx
        self.canvas.delete('all')
        self.draw_board()
        self.draw_piece()

    def move_down(self):
        self.current_piece['y'] += 1
        if self.collision():
            self.current_piece['y'] -= 1
            self.place_piece()
            self.remove_line()
        self.canvas.delete('all')
        self.draw_board()
        self.draw_piece()

    def rotate_piece(self):
        original_shape = self.current_piece['shape']
        self.current_piece['shape'] = list(zip(*self.current_piece['shape'][::-1]))
        if self.collision():
            self.current_piece['shape'] = original_shape
        self.canvas.delete('all')
        self.draw_board()
        self.draw_piece()

    def draw_board(self):
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                if cell:
                    self.canvas.create_rectangle(
                        x * 30, y * 30, (x + 1) * 30, (y + 1) * 30, fill=cell
                    )

    def update_game(self):
        self.move_down()
        if not self.game_over:
            self.root.after(1000, self.update_game)
        else:
            print("Game Over!")  # ゲームオーバーメッセージを表示

root = tk.Tk()
app = TetrisApp(root)
root.mainloop()
