#Imports
import asyncio
import time
import json
import random
import numpy as np
from random import randrange
from Modules import AI_Player, MaxDamagePlayer, Team_Builder, create_random_teams, load_team
from poke_env.player import RandomPlayer

#Create Teams
#create_random_teams(5, "Teams")
teams = load_team("Teams.json")

#Create Team Builders
team_builder = []
for team in teams:
    team_builder.append(Team_Builder(team))
random.shuffle(team_builder)

#Store Results
rewards = []
wins = []

#Function to save results JSON
def save_results(results, name):
    #Create JSON file.
    results_json = {
        "title": name,
        "results": results
    }

    #Write to JSON file.
    json_results = json.dumps(results_json)

    with open(f'Results/JSON/{name}.json', 'w') as file:
        file.write(json_results)

#Main function
async def main():
    #Create players.

    #AI player
    AI_s0 = AI_Player(
        use_double=False,
        table_type=0,
        csv=["pokemon_preset_0.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=0,
    )

    AI_s1 = AI_Player(
        use_double=False,
        table_type=1,
        csv=["type_preset_1.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=0,
    )

    AI_d0 = AI_Player(
        use_double=True,
        table_type=0,
        gamma=0.9,
        epsilon=0.5,
        alpha=0.5,
        csv=["pokemon_preset_0.csv", "pokemon_preset_0.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=0,
    )

    AI_d1 = AI_Player(
        use_double=True,
        table_type=1,
        epsilon=0.9,
        csv=["type_preset_1.csv", "type_preset_1.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=0,
    )

    #Max damage player
    max_damage_player = MaxDamagePlayer(
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=0,
    )

    #Random player
    random_player = RandomPlayer(
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=0,
    )

    #Store AI players
    AI_players = [AI_s0, AI_s1, AI_d0, AI_d1]
    #AI_players = [AI_s0]
    #AI_players = [AI_s1]
    #AI_players = [AI_d0]
    #AI_players = [AI_d1]

    #AI_players = [AI_d0, AI_d1]

    #Number of battles
    n_battles = 50
    concurrent_battles = 150

    #Average
    average = 5

    #Evaluate the AI player
    for i, AI in enumerate(AI_players):
        #Average rewards and wins
        average_rewards = []
        average_wins = []

        #Time taken to run.
        train_start = time.time()

        print(f"\nEvaluating AI player {i}")

        #Get average.
        for j in range(average):
            #Time taken to run.
            start = time.time()

            #Reset AI Q-table
            if AI.use_double:
                if AI.table_type == 0:
                    AI.load(["pokemon_preset_0.csv", "pokemon_preset_0.csv"])
                elif AI.table_type == 1:
                    AI.load(["type_preset_1.csv", "type_preset_1.csv"])
            elif not AI.use_double:
                if AI.table_type == 0:
                    AI.load(["pokemon_preset_0.csv"])
                elif AI.table_type == 1:
                    AI.load(["type_preset_1.csv"])

            #Number of battles won
            previous_wins = 0
            AI.reset_battles()

            #Store rewards and wins
            reward = []
            win = []

            for k in range(1, n_battles + 1):
                #Battle against max damage player
                await AI.battle_against(max_damage_player, n_battles=concurrent_battles)

                # #Battle against random player
                await AI.battle_against(random_player, n_battles=concurrent_battles)

                #Randomise team
                AI.set_team(team_builder[randrange(len(team_builder))])
                max_damage_player._team = team_builder[randrange(len(team_builder))]
                random_player._team = team_builder[randrange(len(team_builder))]

                #Store rewards and wins
                if k % (n_battles / n_battles) == 0:
                    #Store rewards
                    reward.append(AI.get_total_reward())

                    #Store wins
                    new_wins = AI.n_won_battles - previous_wins
                    previous_wins = AI.n_won_battles
                    win.append(new_wins)

                #Print training progress.
                if k % (n_battles / 25) == 0:
                    print(f"Battle {k * concurrent_battles * 2} finished")

            # Print the results
            battles_won = AI.n_won_battles
            time_taken = round(time.time() - start, 2) 
            print(f"\nAI player won {battles_won} / {n_battles * concurrent_battles * 2} battles [this took {time_taken} seconds] for loop {j+1}")

            #Store to average rewards and wins.
            average_rewards.append(reward)
            average_wins.append(win)

        #Calculate average rewards
        avg_reward = np.array(average_rewards[0])
        for x in range(1, len(average_rewards)):
            avg_reward += np.array(average_rewards[x])
        average_rewards = avg_reward / len(average_rewards)

        #Calculate average wins
        avg_win = np.array(average_wins[0])
        for x in range(1, len(average_wins)):
            avg_win += np.array(average_wins[x])
        average_wins = avg_win / len(average_wins)

        #Store average rewards and wins
        rewards.append(average_rewards.tolist())
        wins.append(average_wins.tolist())

        #Print time taken to train
        print(f"\nTime taken to train AI player {i}: {round(time.time() - train_start, 2)} seconds")

    #Save the Q-table to a CSV file
    AI_players[0].to_CSV("s0 Avg")
    AI_players[1].to_CSV("s1 Avg")
    AI_players[2].to_CSV("Final Model")
    AI_players[3].to_CSV("d1 e_0.9")

    # #Save results to a JSON file
    save_results(rewards[0], "Reward Avg Single Q-Learning Type 0")
    save_results(rewards[1], "Reward Avg Single Q-Learning Type 1")
    save_results(rewards[2], "Reward Final Model")
    save_results(rewards[3], "Reward E 0.9 Double Q-Learning Type 1")

    save_results(wins[0], "Wins Avg Single Q-Learning Type 0")
    save_results(wins[1], "Wins Avg Single Q-Learning Type 1")
    save_results(wins[2], "Wins Final Model")
    save_results(wins[3], "Wins E 0.9 Double Q-Learning Type 1")

#Run main
if __name__ == "__main__":
    asyncio.run(main())
    #asyncio.get_event_loop().run_until_complete(main())