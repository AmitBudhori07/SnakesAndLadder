import random
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

class SnakeLadders:
    def __init__(self, size=10, snakes=None, ladders=None, num_players=2):
        self.size = size
        self.players = ['Player 1', 'Player 2', 'Player 3', 'Player 4'][:num_players]
        self.player_positions = {player: 0 for player in self.players}
        self.snakes = snakes or {}
        self.ladders = ladders or {}
        self.history = []
        
        self.progress = {player: [] for player in self.players}
        
        self.fig, self.ax = plt.subplots(figsize=(10, 5))
        plt.ion()

    def roll_dice(self):
        return random.randint(1, 6)

    def move_player(self, player):
        roll = self.roll_dice()
        new_position = self.player_positions[player] + roll
        if new_position > self.size ** 2:
            new_position = self.size ** 2

        if new_position in self.ladders:
            new_position = self.ladders[new_position]
        elif new_position in self.snakes:
            new_position = self.snakes[new_position]

        self.player_positions[player] = new_position
        self.history.append((player, roll, new_position))
        self.progress[player].append(new_position)
        print(f"{player} rolled a {roll} and moved to {new_position}.")

    def plot_player_positions(self):
        self.ax.clear()
        positions = list(self.player_positions.values())
        sns.barplot(x=list(self.player_positions.keys()), y=positions, ax=self.ax)
        self.ax.set_ylim(0, self.size ** 2)
        self.ax.set_title('Current Player Positions')
        self.ax.set_xlabel('Players')
        self.ax.set_ylabel('Position on Board')
        plt.draw()
        plt.pause(1)

    def plot_history(self):
        data = pd.DataFrame(self.history, columns=['Player', 'Roll', 'Position'])
        
        self.ax.clear()
        sns.lineplot(data=data, x=data.index, y='Position', hue='Player', ax=self.ax, marker='o')
        self.ax.set_title('Player Movement Over Time')
        self.ax.set_xlabel('Turn Number')
        self.ax.set_ylabel('Position on Board')
        plt.draw()
        plt.pause(1)

    def plot_progress(self):
        self.ax.clear()
        for player in self.players:
            sns.lineplot(x=range(len(self.progress[player])), y=self.progress[player], label=player, marker='o', ax=self.ax)
        
        self.ax.set_title('Player Progress Over Time')
        self.ax.set_xlabel('Turn Number')
        self.ax.set_ylabel('Position on Board')
        self.ax.set_ylim(0, self.size ** 2)
        plt.draw()
        plt.pause(1)

    def play_game(self):
        while True:
            for player in self.players:
                self.move_player(player)
                self.plot_player_positions()
                self.plot_progress()
                
                if self.player_positions[player] == self.size ** 2:
                    print(f"{player} wins!")
                    plt.ioff()
                    plt.show()
                    return

if __name__ == "__main__":
    snakes = {17: 4, 54: 34, 62: 19, 64: 60}
    ladders = {3: 22, 5: 8, 11: 26, 20: 29}
    
    game = SnakeLadders(size=10, snakes=snakes, ladders=ladders, num_players=2)
    game.play_game()
