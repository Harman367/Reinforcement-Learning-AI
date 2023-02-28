#Imports
from typing import List
import orjson
from Modules.Algorithm.Q_Learning import Q_Learning
from Modules.Algorithm.Reward import get_reward
from poke_env.player import Player

#AI_Player
class AI_Player(Player):

    #Setup Q-Learning
    q_learning = Q_Learning()

    #Array to store the state of the battle
    msg_state = []

    #Current pokemon in play. Used to check if the pokemon has changed.
    current_pokemon = "CurrentPokemon"
    opposing_pokemon = "OpposingPokemon"
    state = None

    #Current pokemon hp.
    current_hp = 0
    opposing_hp = 0
    previous_hp = 0
    pre_opposing_hp = 0

    #Current move in play. Used to check if the move has changed.
    move = None

    #Skip reward calculation.
    skip = True

    #Function to choose a move.
    def choose_move(self, battle):
        # If the player can attack, it will
        if battle.available_moves:
            self.state = (battle.active_pokemon._species + "_" + battle.opponent_active_pokemon._species).lower()
            act = self.q_learning.select_action(self.state, battle.available_moves)
            return self.create_order(act)

        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)
        
    #Function to save the Q-table to a CSV file
    def to_CSV(self):
        self.q_learning.q_table.to_CSV()

    #Function to handle the battle message.
    async def _handle_battle_message(self, split_messages: List[List[str]]) -> None:
        """Handles a battle message.

        :param split_message: The received battle message.
        :type split_message: str
        """

        #Reset the state array.
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
                #Append the message to the state array.
                self.msg_state.append(split_message)

                battle._parse_message(split_message)
                await self._handle_battle_request(battle)
            elif split_message[1] == "teampreview":
                battle._parse_message(split_message)
                await self._handle_battle_request(battle, from_teampreview_request=True)
            elif split_message[1] == "bigerror":
                self.logger.warning("Received 'bigerror' message: %s", split_message)
            else:
                #Append the message to the state array.
                self.msg_state.append(split_message)
                self.skip = False

                battle._parse_message(split_message)

        #Check if reward should be calculated.
        if not self.skip:
            self.skip = True

            #Calculate the reward.
            get_reward(self, self.msg_state)