#Imports
import asyncio
import time
import json
from Modules import AI_Player, MaxDamagePlayer, Team_Builder, format_JSON, load_team
from poke_env.player import RandomPlayer

#Create Teams
#team_1, team_2 = format_JSON()
team_1, team_2 = load_team()

#Create Team Builders
custom_builder1 = Team_Builder(team_1)
custom_builder2 = Team_Builder(team_2)

#Store Results
results_max = []
results_random = []
results_self = []

acuumulated_reward = []

#Function to save results JSON
def save_results(results, name):
    #Create JSON file.
    results_json = {
        "title": name,
        "results": results 
    }

    #Write to JSON file.
    json_results = json.dumps(results_json)

    with open(f'Results\{name}.json', 'w') as file:
        file.write(json_results)

#Main function
async def main():
    #Time taken to run.
    start = time.time()

    #Create players.

    #AI player
    AI = AI_Player(
        use_double=False,
        table_type=1,
        #csv="Results\Test.csv",
        battle_format="gen4anythinggoes",
        team=custom_builder1,
    )

    #Max damage player
    max_damage_player = MaxDamagePlayer(
        battle_format="gen4anythinggoes",
        team=custom_builder1,
    )

    #Random player
    random_player = RandomPlayer(
        battle_format="gen4anythinggoes",
        team=custom_builder1,
    )

    #Self play
    # AI_self = AI_Player(
    #     csv="Results\Q_Table.csv",
    #     battle_format="gen4anythinggoes",
    #     team=custom_builder1,
    # )
    
    #Number of battles
    n_battles = 100

    #Number of battels won
    previous_wins = 0

    #Evaluate the AI player
    for _ in range(1, n_battles + 1):
        #Battle against max damage player
        await AI.battle_against(max_damage_player, n_battles=1)
        results_max.append(AI.get_total_reward())
        #acuumulated_reward.append(AI.get_total_reward())

        #Battle against random player
        #await AI.battle_against(random_player, n_battles=1)
        #results_random.append(AI.get_total_reward())

        #Self play
        #await AI.battle_against(AI_self, n_battles=1)
        #results_self.append(AI.get_total_reward())

        #AI.set_team(custom_builder2)

        if _ % (n_battles / 10) == 0:
            print(f"Battle {_} finished")
            new_wins = AI.n_won_battles - previous_wins
            previous_wins = AI.n_won_battles
            #print(f"AI won {new_wins}")
            #results_max.append(new_wins)
            #results_random.append(new_wins)
            #results_self.append(new_wins)
            

        
    #AI.reset_battles()

    # Print the results
    battles_won = AI.n_won_battles
    time_taken = round(time.time() - start, 2) 
    print(f"\nAI player won {battles_won} / {n_battles * 1} battles [this took {time_taken} seconds]")

    #print(AI.q_learning.q_table.q_table[0:2])

    #Save the Q-table to a CSV file
    AI.to_CSV("Test")

    #Save results to a JSON file
    save_results(results_max, "VS Max Damage Player")
    #save_results(results_random, "VS Random Player")
    #save_results(results_self, "Self Play")
    #save_results(acuumulated_reward, "Accumulated Reward")

#Run main
if __name__ == "__main__":
    asyncio.run(main())
    #asyncio.get_event_loop().run_until_complete(main())