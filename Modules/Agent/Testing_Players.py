#Imports
from poke_env.player import Player

# This class is a player that always chooses the move that does the most damage.
# Source: https://poke-env.readthedocs.io/en/latest/max_damage_player.html
class MaxDamagePlayer(Player):
    def choose_move(self, battle):
        # If the player can attack, it will
        if battle.available_moves:
            # Finds the best move among available ones
            best_move = max(battle.available_moves, key=lambda move: move.base_power)
            return self.create_order(best_move)

        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)