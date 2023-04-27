#Imports
import asyncio
import random
import numpy as np
from random import randrange
from Modules import AI_Player, MaxDamagePlayer, Team_Builder, create_random_teams, load_team
from poke_env.player import RandomPlayer, cross_evaluate
from tabulate import tabulate

#Create Teams
#create_random_teams(5, "Teams")
teams = load_team("Teams.json")

#Create Team Builders
team_builder = []
for team in teams:
    team_builder.append(Team_Builder(team))
random.shuffle(team_builder)

#Main function
async def main():
    #Create players.

    #AI player
    AI_s0 = AI_Player(
        use_double=False,
        table_type=0,
        csv=["Results\CSV\Avg\s0 Avg.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=1,
    )

    AI_s1 = AI_Player(
        use_double=False,
        table_type=1,
        csv=["Results\CSV\Avg\s1 Avg.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=1,
    )

    AI_d0 = AI_Player(
        use_double=True,
        table_type=0,
        csv=["Results\CSV\Avg\A_d0 Avg.csv", "Results\CSV\Avg\B_d0 Avg.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=1,
    )

    AI_d1 = AI_Player(
        use_double=True,
        table_type=1,
        csv=["Results\CSV\Avg\A_d1 Avg.csv", "Results\CSV\Avg\B_d1 Avg.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=1,
    )

    AI_d0_a_05 = AI_Player(
        use_double=True,
        table_type=0,
        csv=["Results\CSV\A_d0 a_0.5.csv", "Results\CSV\B_d0 a_0.5.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=1,
    )

    AI_d0_a_09 = AI_Player(
        use_double=True,
        table_type=0,
        csv=["Results\CSV\A_d0 a_0.9.csv", "Results\CSV\B_d0 a_0.9.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=1,
    )

    AI_d0_e_05 = AI_Player(
        use_double=True,
        table_type=0,
        csv=["Results\CSV\A_d0 e_0.5.csv", "Results\CSV\B_d0 e_0.5.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=1,
    )

    AI_d0_e_09 = AI_Player(
        use_double=True,
        table_type=0,
        csv=["Results\CSV\A_d0 e_0.9.csv", "Results\CSV\B_d0 e_0.9.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=1,
    )

    AI_d0_g_02 = AI_Player(
        use_double=True,
        table_type=0,
        csv=["Results\CSV\A_d0 g_0.2.csv", "Results\CSV\B_d0 g_0.2.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=1,
    )

    AI_d0_g_09 = AI_Player(
        use_double=True,
        table_type=0,
        csv=["Results\CSV\A_d0 g_0.9.csv", "Results\CSV\B_d0 g_0.9.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=1,
    )

    AI_d1_a_05 = AI_Player(
        use_double=True,
        table_type=1,
        csv=["Results\CSV\A_d1 a_0.5.csv", "Results\CSV\B_d1 a_0.5.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=1,
    )

    AI_d1_a_09 = AI_Player(
        use_double=True,
        table_type=1,
        csv=["Results\CSV\A_d1 a_0.9.csv", "Results\CSV\B_d1 a_0.9.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=1,
    )

    AI_d1_e_05 = AI_Player(
        use_double=True,
        table_type=1,
        csv=["Results\CSV\A_d1 e_0.5.csv", "Results\CSV\B_d1 e_0.5.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=1,
    )

    AI_d1_e_09 = AI_Player(
        use_double=True,
        table_type=1,
        csv=["Results\CSV\A_d1 e_0.9.csv", "Results\CSV\B_d1 e_0.9.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=1,
    )

    AI_d1_g_02 = AI_Player(
        use_double=True,
        table_type=1,
        csv=["Results\CSV\A_d1 g_0.2.csv", "Results\CSV\B_d1 g_0.2.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=1,
    )

    AI_d1_g_09 = AI_Player(
        use_double=True,
        table_type=1,
        csv=["Results\CSV\A_d1 g_0.9.csv", "Results\CSV\B_d1 g_0.9.csv"],
        battle_format="gen4anythinggoes",
        team=team_builder[randrange(len(team_builder))],
        max_concurrent_battles=1,
    )


    #Set whether test against human or not.
    against_human = False
    
    if not against_human:
        #Reference: https://poke-env.readthedocs.io/en/latest/cross_evaluate_random_players.html

        #Store players
        players = [AI_s0, AI_s1, AI_d0, AI_d1, AI_d0_a_05, AI_d0_a_09, AI_d0_e_05, AI_d0_e_09, AI_d0_g_02, AI_d0_g_09, AI_d1_a_05, AI_d1_a_09, AI_d1_e_05, AI_d1_e_09, AI_d1_g_02, AI_d1_g_09]
        
        for i in range(1, 6):
            print(f"Round {i} of 5")

            #Cross Evaluation
            cross_evaluation = await cross_evaluate(players, n_challenges=10)

            #Player names
            results_table = [player.username for player in players]

            print(results_table)

            #Append results to table
            for p1, results in cross_evaluation.items():
                print([p1] + [cross_evaluation[p1][p2] for p2 in results])

            #Set random team for players
            for player in players:
                player._team = team_builder[randrange(len(team_builder))]

    else:

        #Store players
        players = [AI_s0, AI_s1, AI_d0, AI_d1]

        #Accept challenges
        for player in players:
            print(f"{player.username} is ready to accept challenges.")

            #For each team
            for i in range(10):
                print(f"Round {i} of {10}")
                player._team = team_builder[i]
                await player.send_challenges(n_challenges=2, opponent="Guest 44")

            #Print number of wins.
            print(f"{player.username} has {player.n_won_battles} wins out of {10} battles.")

#Run main
if __name__ == "__main__":
    asyncio.run(main())
    #asyncio.get_event_loop().run_until_complete(main())