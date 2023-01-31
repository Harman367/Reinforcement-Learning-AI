#Imports
from poke_env.player import RandomPlayer, Gen8EnvSinglePlayer, ObservationType
import asyncio
import numpy as np
from poke_env.environment import AbstractBattle
from gym.spaces import Space, Box
from gym.utils.env_checker import check_env
import random
from IPython.display import clear_output

#Class to create AI Player.
class AiPlayer(Gen8EnvSinglePlayer):

    #Create Algorithm
    #q_learning = Q_Learning.Q_Learning()

    def calc_reward(self, last_battle, current_battle) -> float:
        return self.reward_computing_helper(
            current_battle, fainted_value=2.0, hp_value=1.0, victory_value=30.0
        )

    def embed_battle(self, battle: AbstractBattle) -> ObservationType:
        # -1 indicates that the move does not have a base power
        # or is not available
        moves_base_power = -np.ones(4)
        moves_dmg_multiplier = np.ones(4)

        for i, move in enumerate(battle.available_moves):
            moves_base_power[i] = (
                move.base_power / 100
            )  # Simple rescaling to facilitate learning
            if move.type:
                moves_dmg_multiplier[i] = move.type.damage_multiplier(
                    battle.opponent_active_pokemon.type_1,
                    battle.opponent_active_pokemon.type_2,
                )

        # We count how many pokemons have fainted in each team
        fainted_mon_team = len([mon for mon in battle.team.values() if mon.fainted]) / 6
        fainted_mon_opponent = (
            len([mon for mon in battle.opponent_team.values() if mon.fainted]) / 6
        )

        # Final vector with 10 components
        final_vector = np.concatenate(
            [
                moves_base_power,
                moves_dmg_multiplier,
                [fainted_mon_team, fainted_mon_opponent],
            ]
        )
        return np.float32(final_vector)


    def describe_embedding(self) -> Space:
        low = [-1, -1, -1, -1, 0, 0, 0, 0, 0, 0]
        high = [3, 3, 3, 3, 4, 4, 4, 4, 1, 1]
        return Box(
            np.array(low, dtype=np.float32),
            np.array(high, dtype=np.float32),
            dtype=np.float32,
        )    


#Main Method
async def main():

    # First test the environment to ensure the class is consistent
    # with the OpenAI API
    #test_env = AiPlayer(battle_format="gen8randombattle", start_challenging=True)
    #check_env(test_env)
    #test_env.close()


    # Create one environment for training and one for evaluation
    opponent = RandomPlayer(battle_format="gen8randombattle")
    train_env = AiPlayer(
        battle_format="gen8randombattle", opponent=opponent, start_challenging=True
    )

    opponent = RandomPlayer(battle_format="gen8randombattle")
    eval_env = AiPlayer(
        battle_format="gen8randombattle", opponent=opponent, start_challenging=True
    )


    # Compute dimensions
    n_action = train_env.action_space.n
    #input_shape = train_env.observation_space.n


    q_table = np.zeros([1000, n_action])

    # Hyperparameters
    alpha = 0.1
    gamma = 0.6
    epsilon = 0.1

    # For plotting metrics
    all_epochs = []
    all_penalties = []

    for i in range(1, 100):
        state = train_env.reset_env()

        epochs, penalties, reward, = 0, 0, 0
        done = False
        
        while not done:
            if random.uniform(0, 1) < epsilon:
                action = train_env.action_space.sample() # Explore action space
            else:
                action = np.argmax(q_table[state]) # Exploit learned values

            next_state, reward, done, info = train_env.step(action) 
            
            old_value = q_table[state, action]
            next_max = np.max(q_table[next_state])
            
            new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
            q_table[state, action] = new_value

            if reward == -10:
                penalties += 1

            state = next_state
            epochs += 1
            
        if i % 100 == 0:
            clear_output(wait=True)
            print(f"Episode: {i}")

    print("Training finished.\n")

#
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())