import tkinter as tk
from tkinter import font

class MonopolyBoard(tk.Canvas):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.cities = {
            'Oriental Avenue': {'x': 740, 'y': 575, 'color': 'cyan', 'price': '$100'},
            'Vermont Avenue': {'x': 640, 'y': 575, 'color': 'cyan', 'price': '$100'},
            'Connecticut Avenue': {'x': 540, 'y': 575, 'color': 'cyan', 'price': '$120'},
            'St. Charles Place': {'x': 415, 'y': 450, 'color': '#D73E78', 'price': '$140'},
            'States Avenue': {'x': 415, 'y': 350, 'color': '#D73E78', 'price': '$140'},
            'Virginia Avenue': {'x': 415, 'y': 250, 'color': '#D73E78', 'price': '$160'},
            'St. James Place': {'x': 540, 'y': 125, 'color': 'orange', 'price': '$180'},
            'Tennessee Avenue': {'x': 640, 'y': 125, 'color': 'orange', 'price': '$180'},
            'New York Avenue': {'x': 740, 'y': 125, 'color': 'orange', 'price': '$200'},
            'Kentucky Avenue': {'x': 865, 'y': 250, 'color': 'red', 'price': '$220'},
            'Mediterranean Avenue': {'x': 865, 'y': 350, 'color': 'brown', 'price': '$60'},
            'Baltic Avenue': {'x': 865, 'y': 450, 'color': 'brown', 'price': '$60'},
            
            # 'Indiana Avenue': {'x': 440, 'y': 180, 'color': 'red'},
        }
        self.players = {
            1: {'x': 50, 'y': 250, 'color': 'yellow'},
            2: {'x': 50, 'y': 250, 'color': 'red'}
        }
        self.pass_data = []
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
        self.create_rectangle(340, 50, 940, 650, outline='black', width=2)
        for city, pos in self.cities.items():
            if city in ['Kentucky Avenue', 'Mediterranean Avenue', 'Baltic Avenue',
                    'Virginia Avenue', 'States Avenue', 'St. Charles Place']:
                self.create_rectangle(pos['x'] - 75, pos['y'] - 50, pos['x'] + 75, pos['y'] + 50, outline='black', width=2)
                # self.create_text(pos['x'], pos['y'], text=city, anchor='center', width= 100)
                if city in ['Kentucky Avenue', 'Mediterranean Avenue', 'Baltic Avenue']:
                    self.create_rectangle(pos['x'] - 75, pos['y'] - 50, pos['x'] - 40, pos['y'] + 50, fill=pos['color'], outline='black', width=2, tags="city_color")
                    self.create_text(pos['x'] - 15, pos['y'], text=city, anchor='center', width= 70, angle= 90, tags="city_text")
                    self.create_text(pos['x'] + 50, pos['y'], text=pos['price'], anchor='center', width= 70, angle= 90, tags="price_text")
                    
                if city in ['Virginia Avenue', 'States Avenue', 'St. Charles Place']:
                    self.create_rectangle(pos['x'] + 40, pos['y'] - 50, pos['x'] + 75, pos['y'] + 50, outline='black', width=2, fill=pos['color'], tags="city_color")
                    self.create_text(pos['x'] + 15, pos['y'], text=city, anchor='center', width= 70, angle=270, tags="city_text")
                    self.create_text(pos['x'] - 50, pos['y'], text=pos['price'], anchor='center', width= 70, angle= 270, tags="price_text")
                    
            else:
                self.create_rectangle(pos['x'] - 50, pos['y'] - 75, pos['x'] + 50, pos['y'] + 75, outline='black', width=2)
                if city in ['St. James Place', 'Tennessee Avenue', 'New York Avenue']:
                    self.create_rectangle(pos['x'] - 50, pos['y'] + 40, pos['x'] + 50, pos['y'] + 75, outline='black', width=2, fill=pos['color'], tags="city_color")
                    self.create_text(pos['x'], pos['y'] + 15, text=city, anchor='center', width= 70, angle= 180, tags="city_text")
                    self.create_text(pos['x'], pos['y'] - 50, text=pos['price'], anchor='center', width= 70, angle= 180, tags="price_text")
                if city in ['Connecticut Avenue', 'Vermont Avenue', 'Oriental Avenue']:
                    self.create_rectangle(pos['x'] - 50, pos['y'] - 75, pos['x'] + 50, pos['y'] - 40, outline='black', width=2, fill=pos['color'], tags="city_color")
                    self.create_text(pos['x'], pos['y'] - 15, text=city, anchor='center', width= 70, tags="city_text")
                    self.create_text(pos['x'], pos['y'] + 50, text=pos['price'], anchor='center', width= 70, tags="price_text")
        
        self.create_text(600,350,text='Player', anchor = 'w')
        self.create_text(600,380,text='Roll Value', anchor = 'w')
        self.create_text(600,410,text='Action', anchor = 'w')

        self.create_text(830,540, text='   COLLECT \n$200 SALARY\nAS YOU PASS', anchor='center', angle= 45)
        my_font = font.Font(family="Kabel", size=45, weight="bold")
        self.create_text(870,570, text='GO', font=my_font, angle=45)

        self.arrow_icon = tk.PhotoImage(file="arrow.png")
        self.create_image(866, 620, image=self.arrow_icon, anchor=tk.CENTER, tags="arrow")
        self.kite_icon = tk.PhotoImage(file="kite.png")
        self.create_image(855, 560, image=self.kite_icon, anchor=tk.CENTER, tags="current_position1")
        self.star_icon = tk.PhotoImage(file="star.png")
        self.create_image(855, 590, image=self.star_icon, anchor=tk.CENTER, tags="current_position2")

        self.update_pass()

    def create_star(self, x, y, size, **kwargs):
        # Calculate coordinates for a 5-point star
        points = [
            (x, y - size),  # Top point
            # (x + size * 0.951, y - size * 0.309),  # Right top point
            # (x + size * 0.588, y + size * 0.809),  # Right bottom point
            # (x - size * 0.588, y + size * 0.809),  # Left bottom point
            # (x - size * 0.951, y - size * 0.309)   # Left top point
            (x + size * 0.224, y - size * 0.309),        # Upper-right point
            (x + size * 0.951, y - size * 0.309),        # Upper-right point (tip)
            (x + size * 0.309, y + size * 0.118),        # Right middle point
            (x + size * 0.588, y + size * 0.809),        # Lower-right point
            (x, y + size * 0.382),                       # Lower point
            (x - size * 0.588, y + size * 0.809),        # Lower-left point
            (x - size * 0.309, y + size * 0.118),        # Left middle point
            (x - size * 0.951, y - size * 0.309),        # Upper-left point (tip)
            (x - size * 0.224, y - size * 0.309)         # Upper-left point
        ]
        
        self.create_polygon(points, **kwargs)


    def create_pentagon(self, x, y, size, **kwargs):
        # Calculate coordinates for a 5-point star
        points = [
            (x, y - size),  # Top point
            (x + size * 0.951, y - size * 0.309),  # Right top point
            (x + size * 0.588, y + size * 0.809),  # Right bottom point
            (x - size * 0.588, y + size * 0.809),  # Left bottom point
            (x - size * 0.951, y - size * 0.309)   # Left top point
        ]
        
        self.create_polygon(points, **kwargs)

    def update_pass(self):
        if self.current_pass < len(self.pass_data):
            self.delete("player_circle")
            self.delete("player_num")
            self.delete("roll_val")
            self.delete("random_action")
            self.delete("current_position1")
            self.delete("current_position2")
            pass_data = self.pass_data[self.current_pass]
            print(pass_data)
            for city, player in pass_data:
                print(pass_data)
                if player in self.players:
                    pos = self.cities[city]
                    if city in ['Kentucky Avenue', 'Mediterranean Avenue', 'Baltic Avenue',
                    'Virginia Avenue', 'States Avenue', 'St. Charles Place']:
                        self.create_rectangle(pos['x'] - 75, pos['y'] - 50, pos['x'] + 75, pos['y'] + 50, outline='black', width=2, fill=self.players[player]['color'], stipple='gray50', tags="player_circle")
                        self.tag_raise("city_text")
                        self.tag_raise("price_text")
                        self.tag_raise("city_color")
                    else:
                        self.create_rectangle(pos['x'] - 50, pos['y'] - 75, pos['x'] + 50, pos['y'] + 75, outline='black', width=2, fill=self.players[player]['color'], stipple='gray50', tags="player_circle")
                        self.tag_raise("city_text")
                        self.tag_raise("price_text")
                        self.tag_raise("city_color")
                    # self.create_star(pos['x'], pos['y'] + 25, self.circle_size, fill=self.players[player]['color'], tags="player_circle")
                    # self.create_oval(pos['x'] - self.circle_size, pos['y'] - self.circle_size + 25,
                    #                  pos['x'] + self.circle_size, pos['y'] + self.circle_size + 25,
                    #                  fill=self.players[player]['color'], tags="player_circle")
            
            current_player = self.current_player_list[self.current_pass]
            self.create_text(710,350,text =current_player, anchor = 'w', tags = "player_num")
            current_roll_val = self.roll_val_list[self.current_pass]
            self.create_text(710,380,text =current_roll_val, anchor = 'w', tags = "roll_val")
            random_action = self.random_action_list[self.current_pass]
            self.create_text(710,410,text =random_action, anchor = 'w', tags = "random_action")
            player1_city = list(self.cities.keys())[self.appended_pos_list[self.current_pass][0]]
            player2_city  = list(self.cities.keys())[self.appended_pos_list[self.current_pass][1]]
            player1_pos = self.cities[player1_city]
            player2_pos = self.cities[player2_city]
            print("PLAYER1 CITY",player1_city)
            print("PLAYER2 CITY",player2_city)


            # self.kite_icon = tk.PhotoImage(file="kite.png")
            # self.create_image(player1_pos['x'], player1_pos['y'], image=self.kite_icon, anchor=tk.CENTER, tags="current_position1")
            # self.star_icon = tk.PhotoImage(file="star.png")
            # self.create_image(player2_pos['x'], player2_pos['y'], image=self.star_icon, anchor=tk.CENTER, tags="current_position2")

            # for city in pass_data:
            if player1_city in ['Kentucky Avenue', 'Mediterranean Avenue', 'Baltic Avenue']:
                self.kite_icon = tk.PhotoImage(file="kite.png")
                self.create_image(player1_pos['x']-57, player1_pos['y'], image=self.kite_icon, anchor=tk.CENTER, tags="current_position1")

            elif player1_city in ['Virginia Avenue', 'States Avenue', 'St. Charles Place']:
                self.kite_icon = tk.PhotoImage(file="kite.png")
                self.create_image(player1_pos['x']+57, player1_pos['y'], image=self.kite_icon, anchor=tk.CENTER, tags="current_position1")
            
            elif player1_city in ['Connecticut Avenue', 'Vermont Avenue', 'Oriental Avenue']:
                self.kite_icon = tk.PhotoImage(file="kite.png")
                self.create_image(player1_pos['x'], player1_pos['y']-57, image=self.kite_icon, anchor=tk.CENTER, tags="current_position1")

            else:
                self.kite_icon = tk.PhotoImage(file="kite.png")
                self.create_image(player1_pos['x'], player1_pos['y']+57, image=self.kite_icon, anchor=tk.CENTER, tags="current_position1")


            if player2_city in ['Kentucky Avenue', 'Mediterranean Avenue', 'Baltic Avenue']:
                self.star_icon = tk.PhotoImage(file="star.png")
                self.create_image(player2_pos['x']-57, player2_pos['y'], image=self.star_icon, anchor=tk.CENTER, tags="current_position2")

            elif player2_city in ['Virginia Avenue', 'States Avenue', 'St. Charles Place']:
                self.star_icon = tk.PhotoImage(file="star.png")
                self.create_image(player2_pos['x']+57, player2_pos['y'], image=self.star_icon, anchor=tk.CENTER, tags="current_position2")
            
            elif player2_city in ['Connecticut Avenue', 'Vermont Avenue', 'Oriental Avenue']:
                self.star_icon = tk.PhotoImage(file="star.png")
                self.create_image(player2_pos['x'], player2_pos['y']-57, image=self.star_icon, anchor=tk.CENTER, tags="current_position2")

            else:
                self.star_icon = tk.PhotoImage(file="star.png")
                self.create_image(player2_pos['x'], player2_pos['y']+57, image=self.star_icon, anchor=tk.CENTER, tags="current_position2")

            self.current_pass += 1
            print(self.current_pass)
            self.after(150, self.update_pass)

    def reset(self):
        self.delete("player_circle")
        self.delete("player_num")
        self.delete("roll_val")
        self.delete("random_action")
        self.delete("current_position1")
        self.delete("current_position2")
        self.kite_icon = tk.PhotoImage(file="kite.png")
        self.create_image(855, 560, image=self.kite_icon, anchor=tk.CENTER, tags="current_position1")
        self.star_icon = tk.PhotoImage(file="star.png")
        self.create_image(855, 590, image=self.star_icon, anchor=tk.CENTER, tags="current_position2")
        self.current_pass = 0

def main():
    root = tk.Tk()
    root.title("Monopoly Board")
    width= root.winfo_screenwidth()               
    height= root.winfo_screenheight() 
    print("WIDTH", width)
    print("Height", height)              
    root.geometry("%dx%d" % (width, height))

    board = MonopolyBoard(root, width=500, height=500)
    board.pack(fill=tk.BOTH, expand=True)

    def simulate_move():
        board.update_pass()


    def reset_game():
        board.reset()

    simulate_button = tk.Button(root, text="Simulate Move", command=simulate_move)
    simulate_button.pack()
    simulate_button.place(x=595, y=680)

    reset_button = tk.Button(root, text="Reset Game", command=reset_game)
    reset_button.pack()
    reset_button.place(x=605, y=710)
    appending_data=[]
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
            data_list = eval(line.strip())
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