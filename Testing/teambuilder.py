import asyncio
import numpy as np
import time

from poke_env.player import RandomPlayer
from poke_env.teambuilder import Teambuilder


class RandomTeamFromPool(Teambuilder):
    def __init__(self, teams):
        self.teams = [self.join_team(self.parse_showdown_team(team)) for team in teams]

    def yield_team(self):
        return np.random.choice(self.teams)


team_1 = """
Roserade @ Focus Sash
Ability: Natural Cure
EVs: 4 Def / 252 Spd / 252 SpA
Timid Nature
- Grass Knot
- HP Fire
- Sleep Powder
- Toxic Spikes
"""

team_2 = """
Roserade @ Focus Sash
Ability: Natural Cure
EVs: 4 Def / 252 Spd / 252 SpA
Timid Nature
- Grass Knot
- HP Fire
- Sleep Powder
- Toxic Spikes
"""

custom_builder = RandomTeamFromPool([team_1, team_2])


async def main():
    #Time taken to run.
    start = time.time()

    # We create two players
    player_1 = RandomPlayer(
        battle_format="gen4anythinggoes",
        team=custom_builder,
        max_concurrent_battles=10,
    )
    player_2 = RandomPlayer(
        battle_format="gen4anythinggoes",
        team=custom_builder,
        max_concurrent_battles=10,
    )

    await player_1.battle_against(player_2, n_battles=1)

    # Print the results
    battles_won = player_1.n_won_battles
    time_taken = round(time.time() - start, 2) 
    print(f"\nAI player won {battles_won} / {1} battles [this took {time_taken} seconds]")


if __name__ == "__main__":
    asyncio.run(main())
    #asyncio.get_event_loop().run_until_complete(main())