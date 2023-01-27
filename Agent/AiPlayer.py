#Imports
from poke_env.player import Player, RandomPlayer
import Algorithm.Q_Learning
import asyncio
import time

#Class to create AI Player.
class AiPlayer(Player):

    #Create Algorithm
    q_learning = Algorithm.Q_Learning.Q_Learning()

    #Method to take action.
    def choose_move(self, battle):
        action = self.q_learning.select_action(state, battle.available_moves)

        return self.create_order(action)


#Main Method
async def main():

    #Battle start time
    start = time.time()

    #Create Player
    AI_player = AiPlayer(
        battle_format = "gen4singlebattle"
    )

    #Create Random Player
    random_player = RandomPlayer(
        battle_format = "gen4singlebattle"
    )

    #Start battle
    await AI_player.battle_against(random_player, n_battles=100)

    print(
        "AI damage player won %d / 100 battles [this took %f seconds]"
        % (
            AI_player.n_won_battles, time.time() - start
        )
    )

#
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())