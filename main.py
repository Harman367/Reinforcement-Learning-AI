#Imports
import asyncio
import time
from Modules import AI_Player, MaxDamagePlayer

#Main function
async def main():
    #Time taken to run.
    start = time.time()

    # We create two players.

    #AI player
    AI_player = AI_Player(
        battle_format="gen4randombattle",
    )

    #Max damage player
    max_damage_player = MaxDamagePlayer(
        battle_format="gen4randombattle",
    )
    
    #Number of battles
    n_battles = 1

    # Now, let's evaluate our player
    await AI_player.battle_against(max_damage_player, n_battles=n_battles)

    # Print the results
    battles_won = AI_player.n_won_battles
    time_taken = round(time.time() - start, 2) 
    print(f"\nTest player won {battles_won} / {n_battles} battles [this took {time_taken} seconds]")

    #Save the Q table
    AI_Player.q_learning.q_table.to_CSV()

#Run main
if __name__ == "__main__":
    asyncio.run(main())
    #asyncio.get_event_loop().run_until_complete(main())