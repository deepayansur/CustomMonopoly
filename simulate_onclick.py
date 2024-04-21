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
        self.current_player = 0
        self.current_pass = 0
        self.circle_size = 10
        self.current_player_list = []
        self.roll_val_list = []
        self.current_roll_val = 0
        self.random_action = ""
        self.random_action_list = []
        self.appended_pos_list = []
        self.draw_board()

    def draw_board(self):
        self.create_rectangle(0, 0, 500, 500, outline='black', width=2)
        for city, pos in self.cities.items():
            self.create_text(pos['x'], pos['y'], text=city, anchor='center')
        self.create_text(510,10,text='Player', anchor = 'center')
        self.create_text(510,25,text='Roll Value', anchor = 'center')
        self.create_text(510,40,text='Action', anchor = 'center')
        self.create_oval(500 - self.circle_size - 15, 500 - self.circle_size + 15,
                 500 + self.circle_size - 15, 500 + self.circle_size + 15,
                 fill='black', tags="current_position1")
        self.create_oval(500 - self.circle_size +15, 500 - self.circle_size - 15,
                 500 + self.circle_size + 15, 500 + self.circle_size - 15,
                 fill='blue', tags="current_position2")

        self.update_pass()

    def update_pass(self):
        if self.current_pass < len(self.pass_data):
            self.delete("player_circle")
            self.delete("player_num")
            self.delete("roll_val")
            self.delete("random_action")
            self.delete("current_position1")
            self.delete("current_position2")
            pass_data = self.pass_data[self.current_pass]
            for city, player in pass_data:
                if player in self.players:
                    pos = self.cities[city]
                    self.create_oval(pos['x'] - self.circle_size, pos['y'] - self.circle_size,
                                     pos['x'] + self.circle_size, pos['y'] + self.circle_size,
                                     fill=self.players[player]['color'], tags="player_circle")
            current_player = self.current_player_list[self.current_pass]
            self.create_text(510,15,text =current_player, anchor = 'center', tags = "player_num")
            current_roll_val = self.roll_val_list[self.current_pass]
            self.create_text(510,30,text =current_roll_val, anchor = 'center', tags = "roll_val")
            random_action = self.random_action_list[self.current_pass]
            self.create_text(510,45,text =random_action, anchor = 'center', tags = "random_action")
            player1_city = list(self.cities.keys())[self.appended_pos_list[self.current_pass][0]]
            player2_city  = list(self.cities.keys())[self.appended_pos_list[self.current_pass][1]]
            player1_pos = self.cities[player1_city]
            player2_pos = self.cities[player2_city]
            print(player1_city)

            self.create_oval(player1_pos['x'] - self.circle_size - 15, player1_pos['y'] - self.circle_size + 15,
                             player1_pos['x'] + self.circle_size - 15, player1_pos['y'] + self.circle_size + 15,
                             fill='black', tags="current_position1")
            self.create_oval(player2_pos['x'] - self.circle_size + 15, player2_pos['y'] - self.circle_size - 15,
                             player2_pos['x'] + self.circle_size + 15, player2_pos['y'] + self.circle_size - 15,
                             fill='blue', tags="current_position2")
            self.current_pass += 1

    def reset(self):
        self.delete("player_circle")
        self.delete("player_num")
        self.delete("roll_val")
        self.delete("random_action")
        self.delete("current_position1")
        self.delete("current_position2")
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
    appending_data = []
    current_player_list = []
    roll_val_list = []
    current_player = 0
    current_roll_val = 0
    random_action = ""
    random_action_list = []
    position_list = []
    appended_pos_list = []

    with open("ownership_data.txt", 'r') as file:
        for line in file:
            # print("READING A LINE FROM FILE ")
            data_list = eval(line.strip())
            # print(data_list)
            appending_data.append(data_list)

            line = file.readline()
            current_player = eval(line.strip())
            # print(current_player)
            current_player_list.append(current_player)

            line = file.readline()
            current_roll_val = eval(line.strip())
            roll_val_list.append(current_roll_val)

            line = file.readline()
            random_action = line.strip()
            random_action_list.append(random_action)

            line = file.readline()
            position_list = eval(line.strip())
            # print(position_list)
            appended_pos_list.append(position_list)
    # print(appending_data)
    print("TOTAL PASSES:")
    print(len(appending_data))
    print("PRINTING ACTION LIST")
    print(random_action_list)
    print(appended_pos_list)
    # print(current_player_list)
    # print(roll_val_list)
    # print(len(roll_val_list))

    # Sample data
#     board.pass_data = [
#         [('Mediterranean Avenue/Old Kent Rd', 1), ('Baltic Avenue/Whitechapel Rd', 2), ('Oriental Avenue/The Angel, Islington', 1), ('Vermont Avenue/Euston Rd', 2)],
#     [('Mediterranean Avenue/Old Kent Rd', 1), ('Baltic Avenue/Whitechapel Rd', 2), ('Oriental Avenue/The Angel, Islington', 2), ('Vermont Avenue/Euston Rd', 2)],
#     [('Mediterranean Avenue/Old Kent Rd', 1), ('Baltic Avenue/Whitechapel Rd', 2), ('Oriental Avenue/The Angel, Islington', 2), ('Vermont Avenue/Euston Rd', 1)]
# ]
    #Real data
    board.pass_data = appending_data
    board.current_player_list = current_player_list
    board.roll_val_list = roll_val_list
    board.random_action_list = random_action_list
    board.appended_pos_list = appended_pos_list

    root.mainloop()

if __name__ == "__main__":
    main()