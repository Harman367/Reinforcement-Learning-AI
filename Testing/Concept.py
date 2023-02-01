import asyncio
import time
import random
from typing import List
import orjson
import msg_parse

from poke_env.player import Player, RandomPlayer
from poke_env.player.battle_order import BattleOrder


class TestPlayer(Player):

    msg_turn = None
    msg_state = []
    msg_win = "continue"

    #Current pokemon
    current_pokemon = ""
    opposing_pokemon = ""
    move = ""
    current_hp = 0
    opposing_hp = 0
    previous_hp = 0
    pre_opposing_hp = 0

    def choose_move(self, battle):

        #if battle._turn == 1:
            #print("Test")
        print("Choose Move!!!")
        #print(self.msg_turn)
        #print(self.msg_state)
        #self.msg_state = []
        #print(self.msg_win)
        
        # If the player can attack, it will
        if battle.available_moves:
            # Finds the best move among available ones
            available_orders = [BattleOrder(move) for move in battle.available_moves]
            available_orders.extend(
                [BattleOrder(switch) for switch in battle.available_switches]
            )

            return available_orders[int(random.random() * len(available_orders))]

        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)


    #_handle_battle_message
    async def _handle_battle_message(self, split_messages: List[List[str]]) -> None:
        """Handles a battle message.

        :param split_message: The received battle message.
        :type split_message: str
        """

        self.msg_state = []

        # Battle messages can be multiline
        if (
            len(split_messages) > 1
            and len(split_messages[1]) > 1
            and split_messages[1][1] == "init"
        ):
            battle_info = split_messages[0][0].split("-")
            battle = await self._create_battle(battle_info)
        else:
            battle = await self._get_battle(split_messages[0][0])

        for split_message in split_messages[1:]:
            if len(split_message) <= 1:
                continue
            elif split_message[1] in self.MESSAGES_TO_IGNORE:
                pass
            elif split_message[1] == "request":
                if split_message[2]:
                    request = orjson.loads(split_message[2])
                    battle._parse_request(request)
                    if battle.move_on_next_request:
                        await self._handle_battle_request(battle)
                        battle.move_on_next_request = False
            elif split_message[1] == "win" or split_message[1] == "tie":
                #print(split_message)
                #print("Final Turn")
                #print(self.msg_state)
                self.msg_win = split_message
                if split_message[1] == "win":
                    battle._won_by(split_message[2])
                else:
                    battle._tied()
                await self._battle_count_queue.get()
                self._battle_count_queue.task_done()
                self._battle_finished_callback(battle)
                async with self._battle_end_condition:
                    self._battle_end_condition.notify_all()
            elif split_message[1] == "error":
                self.logger.log(
                    25, "Error message received: %s", "|".join(split_message)
                )
                if split_message[2].startswith(
                    "[Invalid choice] Sorry, too late to make a different move"
                ):
                    if battle.trapped:
                        await self._handle_battle_request(battle)
                elif split_message[2].startswith(
                    "[Unavailable choice] Can't switch: The active Pokémon is "
                    "trapped"
                ) or split_message[2].startswith(
                    "[Invalid choice] Can't switch: The active Pokémon is trapped"
                ):
                    battle.trapped = True
                    await self._handle_battle_request(battle)
                elif split_message[2].startswith(
                    "[Invalid choice] Can't switch: You can't switch to an active "
                    "Pokémon"
                ):
                    await self._handle_battle_request(battle, maybe_default_order=True)
                elif split_message[2].startswith(
                    "[Invalid choice] Can't switch: You can't switch to a fainted "
                    "Pokémon"
                ):
                    await self._handle_battle_request(battle, maybe_default_order=True)
                elif split_message[2].startswith(
                    "[Invalid choice] Can't move: Invalid target for"
                ):
                    await self._handle_battle_request(battle, maybe_default_order=True)
                elif split_message[2].startswith(
                    "[Invalid choice] Can't move: You can't choose a target for"
                ):
                    await self._handle_battle_request(battle, maybe_default_order=True)
                elif split_message[2].startswith(
                    "[Invalid choice] Can't move: "
                ) and split_message[2].endswith("needs a target"):
                    await self._handle_battle_request(battle, maybe_default_order=True)
                elif (
                    split_message[2].startswith("[Invalid choice] Can't move: Your")
                    and " doesn't have a move matching " in split_message[2]
                ):
                    await self._handle_battle_request(battle, maybe_default_order=True)
                elif split_message[2].startswith(
                    "[Invalid choice] Incomplete choice: "
                ):
                    await self._handle_battle_request(battle, maybe_default_order=True)
                elif split_message[2].startswith(
                    "[Unavailable choice]"
                ) and split_message[2].endswith("is disabled"):
                    battle.move_on_next_request = True
                elif split_message[2].startswith(
                    "[Invalid choice] Can't move: You sent more choices than unfainted"
                    " Pokémon."
                ):
                    await self._handle_battle_request(battle, maybe_default_order=True)
                else:
                    self.logger.critical("Unexpected error message: %s", split_message)
            elif split_message[1] == "turn":
                print(split_message)
                #self.msg_turn = split_message
                self.msg = split_message
                battle._parse_message(split_message)
                await self._handle_battle_request(battle)
            elif split_message[1] == "teampreview":
                battle._parse_message(split_message)
                await self._handle_battle_request(battle, from_teampreview_request=True)
            elif split_message[1] == "bigerror":
                self.logger.warning("Received 'bigerror' message: %s", split_message)
            else:
                print(split_message)
                self.msg_state.append(split_message)
                #msg_parse.msg_parse(split_message)
                battle._parse_message(split_message)

        #msg_parse
        msg_parse.msg_parse(self, self.msg_state)


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

async def main():
    start = time.time()

    # We create two players.
    random_player = MaxDamagePlayer(
        battle_format="gen8randombattle",
    )
    max_damage_player = TestPlayer(
        battle_format="gen8randombattle",
    )

    # Now, let's evaluate our player
    await max_damage_player.battle_against(random_player, n_battles=1)

    print(
        "Max damage player won %d / 100 battles [this took %f seconds]"
        % (
            max_damage_player.n_won_battles, time.time() - start
        )
    )

    #for k, v in max_damage_player.battles.items():
        #print(k, v)
        #print(v._replay_data)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())