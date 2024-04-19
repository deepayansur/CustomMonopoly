import tkinter as tk

class MonopolyBoard(tk.Canvas):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.cities = {
            'Mediterranean Avenue/Old Kent Rd': {'x': 50, 'y': 250},
            'Baltic Avenue/Whitechapel Rd': {'x': 250, 'y': 450},
            'Oriental Avenue/The Angel, Islington': {'x': 450, 'y': 250},
            'Vermont Avenue/Euston Rd': {'x': 250, 'y': 50}
        }
        self.players = {
            1: {'x': 50, 'y': 250, 'color': 'yellow'},
            2: {'x': 50, 'y': 250, 'color': 'red'}
        }
        self.pass_data = []
        self.current_pass = 0
        self.circle_size = 10
        self.draw_board()

    def draw_board(self):
        self.create_rectangle(0, 0, 500, 500, outline='black', width=2)
        for city, pos in self.cities.items():
            self.create_text(pos['x'], pos['y'], text=city, anchor='center')
        self.update_pass()

    def update_pass(self):
        if self.current_pass < len(self.pass_data):
            self.delete("player_circle")
            pass_data = self.pass_data[self.current_pass]
            print(pass_data)
            for city, player in pass_data:
                if player in self.players:
                    pos = self.cities[city]
                    self.create_oval(pos['x'] - self.circle_size, pos['y'] - self.circle_size,
                                     pos['x'] + self.circle_size, pos['y'] + self.circle_size,
                                     fill=self.players[player]['color'], tags="player_circle")
            self.current_pass += 1

    def reset(self):
        self.delete("player_circle")
        self.current_pass = 0

def main():
    root = tk.Tk()
    root.title("Monopoly Board")
    root.geometry("500x600")

    board = MonopolyBoard(root, width=500, height=500)
    board.pack(fill=tk.BOTH, expand=True)

    def simulate_move():
        board.update_pass()

    def reset_game():
        board.reset()

    simulate_button = tk.Button(root, text="Simulate Move", command=simulate_move)
    simulate_button.pack()

    reset_button = tk.Button(root, text="Reset Game", command=reset_game)
    reset_button.pack()
    appending_data=[]
    with open("ownership_data.txt", 'r') as file:
        for line in file:
            data_list = eval(line.strip())
            appending_data.append(data_list)
    print(appending_data)
    print("TOTAL PASSES:")
    print(len(appending_data))
    # Sample data
#     board.pass_data = [
#         [('Mediterranean Avenue/Old Kent Rd', 1), ('Baltic Avenue/Whitechapel Rd', 2), ('Oriental Avenue/The Angel, Islington', 1), ('Vermont Avenue/Euston Rd', 2)],
#     [('Mediterranean Avenue/Old Kent Rd', 1), ('Baltic Avenue/Whitechapel Rd', 2), ('Oriental Avenue/The Angel, Islington', 2), ('Vermont Avenue/Euston Rd', 2)],
#     [('Mediterranean Avenue/Old Kent Rd', 1), ('Baltic Avenue/Whitechapel Rd', 2), ('Oriental Avenue/The Angel, Islington', 2), ('Vermont Avenue/Euston Rd', 1)]
# ]
    #Real data
    board.pass_data = appending_data

    root.mainloop()

if __name__ == "__main__":
    main()