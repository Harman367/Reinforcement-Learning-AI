#Imports
import asyncio
import time
import json
import random
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
reward_s0 = []
reward_s1 = []
reward_d0 = []
reward_d1 = []
rewards = [reward_s0, reward_s1, reward_d0, reward_d1]

win_s0 = []
win_s1 = []
win_d0 = []
win_d1 = []
wins = [win_s0, win_s1, win_d0, win_d1]

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
        #csv="Results\Test.csv",
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
    )

    AI_s1 = AI_Player(
        use_double=False,
        table_type=1,
        #csv="Results\Test.csv",
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
    )

    AI_d0 = AI_Player(
        use_double=True,
        table_type=0,
        #csv="Results\Test.csv",
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
    )

    AI_d1 = AI_Player(
        use_double=True,
        table_type=1,
        #csv="Results\Test.csv",
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
    )

    #Max damage player
    max_damage_player = MaxDamagePlayer(
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
    )

    #Random player
    random_player = RandomPlayer(
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
    )

    #Store AI players
    AI_players = [AI_s0, AI_s1, AI_d0, AI_d1]

    #Number of battles
    n_battles = 2500

    #Number of battels won
    previous_wins = 0

    #Evaluate the AI player
    for i, AI in enumerate(AI_players):
        #Time taken to run.
        start = time.time()

        for _ in range(1, n_battles + 1):
            #Battle against max damage player
            await AI.battle_against(max_damage_player, n_battles=1)
            rewards[i].append(AI.get_total_reward())

            #Battle against random player
            await AI.battle_against(random_player, n_battles=1)
            rewards[i].append(AI.get_total_reward())


            AI.set_team(team_builder[randrange(len(team_builder))])
            max_damage_player._team = team_builder[randrange(len(team_builder))]
            random_player._team = team_builder[randrange(len(team_builder))]

            if _ % (n_battles / 100) == 0:
                print(f"Battle {_} finished")
                new_wins = AI.n_won_battles - previous_wins
                previous_wins = AI.n_won_battles
                wins[i].append(new_wins)

        # Print the results
        battles_won = AI.n_won_battles
        time_taken = round(time.time() - start, 2) 
        print(f"\nAI player won {battles_won} / {n_battles * 2} battles [this took {time_taken} seconds]")
        
        AI.reset_battles()


    #Save the Q-table to a CSV file
    AI_s0.to_CSV("s0")
    AI_s1.to_CSV("s1")
    AI_d0.to_CSV("d0")
    AI_d1.to_CSV("d1")

    #Save results to a JSON file
    save_results(reward_s0, "Reward Single Q-Learning Type 0")
    save_results(reward_s1, "Reward Single Q-Learning Type 1")
    save_results(reward_d0, "Reward Double Q-Learning Type 0")
    save_results(reward_d1, "Reward Double Q-Learning Type 1")

    save_results(win_s0, "Wins Single Q-Learning Type 0")
    save_results(win_s1, "Wins Single Q-Learning Type 1")
    save_results(win_d0, "Wins Double Q-Learning Type 0")
    save_results(win_d1, "Wins Double Q-Learning Type 1")

#Run main
if __name__ == "__main__":
    asyncio.run(main())
    #asyncio.get_event_loop().run_until_complete(main())