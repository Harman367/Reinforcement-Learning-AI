import asyncio
import time
import random
from typing import List
import orjson
from Modules import AI_Player, MaxDamagePlayer

from poke_env.player import Player, RandomPlayer
from poke_env.player.battle_order import BattleOrder

async def main():
    start = time.time()

    # We create two players.
    max_damage_player = MaxDamagePlayer(
        battle_format="gen4randombattle",
    )
    test_player = AI_Player(
        battle_format="gen4randombattle",
    )

    # Now, let's evaluate our player
    await test_player.battle_against(max_damage_player, n_battles=1)

    print(
        "\nTest player won %d / 1 battles [this took %f seconds]"
        % (
            test_player.n_won_battles, time.time() - start
        )
    )

    #for k, v in max_damage_player.battles.items():
        #print(k, v)
        #print(v._replay_data)

    test_player.q_learning.q_table.to_CSV()


if __name__ == "__main__":
    asyncio.run(main())
    #asyncio.get_event_loop().run_until_complete(main())