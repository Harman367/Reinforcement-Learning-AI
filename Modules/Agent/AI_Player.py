#Imports
from typing import List
import orjson
from Modules.Algorithm.Q_Learning import Q_Learning
from Modules.Algorithm.Double_Q_Learning import Double_Q_Learning
from Modules.Algorithm.Reward import get_reward
from poke_env.player import Player

#AI_Player
class AI_Player(Player):

    #Constructor
    def __init__(self, use_double, table_type, csv=None, alpha = 0.1, gamma = 0.6, epsilon = 0.1, **kwargs):
        super().__init__(**kwargs)

        #Pokemon types
        self.pokemon_types = {
            'Registeel': ['STEEL', 'None'], 'Tentacruel': ['WATER', 'POISON'], 'Tangrowth': ['GRASS', 'None'],
            'Metagross': ['STEEL', 'PSYCHIC'], 'Moltres': ['FIRE', 'FLYING'], 'Heracross': ['BUG', 'FIGHTING'],
            'Machamp': ['FIGHTING', 'None'], 'Blissey': ['NORMAL', 'None'], 'Feraligatr': ['WATER', 'None'],
            'Kingdra': ['WATER', 'DRAGON'], 'Togekiss': ['NORMAL', 'FLYING'], 'Mamoswine': ['ICE', 'GROUND']
        }

        #Move types
        self.move_types = {
            'swordsdance': 'NORMAL_STATUS', 'closecombat': 'FIGHTING_PHYSICAL', 'megahorn': 'BUG_PHYSICAL',
            'facade': 'NORMAL_PHYSICAL', 'waterfall': 'WATER_PHYSICAL', 'aquajet': 'WATER_PHYSICAL',
            'return': 'NORMAL_PHYSICAL', 'meteormash': 'STEEL_PHYSICAL', 'earthquake': 'GROUND_PHYSICAL',
            'explosion': 'NORMAL_PHYSICAL', 'bulletpunch': 'STEEL_PHYSICAL', 'poisonjab': 'POISON_PHYSICAL',
            'hydropump': 'WATER_SPECIAL', 'rest': 'PSYCHIC_STATUS', 'sleeptalk': 'NORMAL_STATUS',
            'dynamicpunch': 'FIGHTING_PHYSICAL', 'payback': 'DARK_PHYSICAL', 'encore': 'NORMAL_STATUS',
            'wish': 'NORMAL_STATUS', 'airslash': 'FLYING_SPECIAL', 'thunderwave': 'ELECTRIC_STATUS',
            'struggle': 'NORMAL_PHYSICAL', 'nightslash': 'DARK_PHYSICAL', 'iceshard': 'ICE_PHYSICAL',
            'lowkick': 'FIGHTING_PHYSICAL', 'shadowball': 'GHOST_SPECIAL', 'willowisp': 'FIRE_STATUS',
            'substitute': 'NORMAL_STATUS', 'leechseed': 'GRASS_STATUS', 'spore': 'GRASS_STATUS',
            'focuspunch': 'FIGHTING_PHYSICAL', 'stealthrock': 'ROCK_STATUS', 'taunt': 'DARK_STATUS',
            'uturn': 'BUG_PHYSICAL', 'reflect': 'PSYCHIC_STATUS', 'lightscreen': 'PSYCHIC_STATUS',
            'softboiled': 'NORMAL_STATUS', 'flamethrower': 'FIRE_SPECIAL', 'toxic': 'POISON_STATUS',
            'rapidspin': 'NORMAL_PHYSICAL', 'earthpower': 'GROUND_SPECIAL', 'trick': 'PSYCHIC_STATUS',
            'fakeout': 'NORMAL_PHYSICAL', 'counter': 'FIGHTING_PHYSICAL', 'icepunch': 'ICE_PHYSICAL',
            'leafstorm': 'GRASS_SPECIAL', 'hiddenpower': 'DARK_SPECIAL', 'batonpass': 'NORMAL_STATUS',
            'meanlook': 'NORMAL_STATUS', 'protect': 'NORMAL_STATUS', 'roost': 'FLYING_STATUS',
            'superfang': 'NORMAL_PHYSICAL', 'endeavor': 'NORMAL_PHYSICAL', 'dracometeor': 'DRAGON_SPECIAL',
            'surf': 'WATER_SPECIAL', 'dragonpulse': 'DRAGON_SPECIAL', 'aromatherapy': 'GRASS_STATUS',
            'seismictoss': 'FIGHTING_PHYSICAL', 'sleeppowder': 'GRASS_STATUS', 'knockoff': 'DARK_PHYSICAL',
            'grassknot': 'GRASS_SPECIAL', 'icebeam': 'ICE_SPECIAL', 'thunderbolt': 'ELECTRIC_SPECIAL',
            'superpower': 'FIGHTING_PHYSICAL', 'haze': 'ICE_STATUS', 'recover': 'NORMAL_STATUS',
            'whirlwind': 'NORMAL_STATUS', 'rockslide': 'ROCK_PHYSICAL', 'psychic': 'PSYCHIC_SPECIAL',
            'psychocut': 'PSYCHIC_PHYSICAL', 'stoneedge': 'ROCK_PHYSICAL'
        }

        #Table type
        self.table_type = table_type

        #Use double Q-learning
        self.use_double = use_double

        #Setup doubele Q-Learning
        if self.use_double:
            self.q_learning = Double_Q_Learning(table_type, self.move_types, alpha = alpha, gamma = gamma, epsilon = epsilon,)
        else:
            self.q_learning = Q_Learning(table_type, self.move_types, alpha = alpha, gamma = gamma, epsilon = epsilon)

        #Table Type 0: State: Pokemon, Action: Move
        #Table Type 1: State: Pokemon Type, Action: Move Type

        #Load Q-table from CSV file
        if csv != None:
            self.load(csv)

        #Array to store the state of the battle
        self.msg_state = []

        #Current pokemon in play. Used to check if the pokemon has changed.
        self.current_pokemon = "CurrentPokemon"
        self.opposing_pokemon = "OpposingPokemon"
        self.state = None
        self.next_state = None
        self.previous_state = None

        #Current pokemon hp.
        self.current_hp = 0
        self.opposing_hp = 0
        self.previous_hp = 0
        self.pre_opposing_hp = 0

        #Current move in play. Used to check if the move has changed.
        self.move = None
        self.act = None

        #Skip reward calculation.
        self.skip = True


    #Function to choose a move.
    def choose_move(self, battle):

        #Check Q-table type.
        if self.q_learning.table_type == 1:
            active_types = battle.active_pokemon._species.capitalize()
            opponent_types = battle.opponent_active_pokemon._species.capitalize()

            #Check if pokemon type is in dictionary.
            if active_types not in self.pokemon_types:
                self.pokemon_types[active_types] = list(map(lambda value: str(value).split(" ")[0], list(battle.active_pokemon.types)))
                #print(active_types)
                #print(self.pokemon_types[active_types])

            #Check if pokemon type is in dictionary.
            if opponent_types not in self.pokemon_types:
                self.pokemon_types[opponent_types] = list(map(lambda value: str(value).split(" ")[0], list(battle.opponent_active_pokemon.types)))
                #print(opponent_types)
                #print(self.pokemon_types[opponent_types])

            #Get state
            self.state = (self.type_to_string(self.pokemon_types[active_types]) + "_" + self.type_to_string(self.pokemon_types[opponent_types])).lower()

        elif self.q_learning.table_type == 0:
            #Get state
            self.state = (battle.active_pokemon._species + "_" + battle.opponent_active_pokemon._species).lower()

        # If the player can attack, it will
        if battle.available_moves:
            self.act = self.q_learning.select_action(self.state, battle.available_moves)
            return self.create_order(self.act)

        # If no attack is available, a random switch will be made
        else:
            return self.choose_random_move(battle)
        
    #Funtion to load the Q-table from a CSV file.
    def load(self, csv):
        if len(csv) == 1 and not self.use_double:
            self.q_learning.q_table.load(csv[0])
        elif len(csv) == 2 and self.use_double:
            self.q_learning.A_q_table.load(csv[0])
            self.q_learning.B_q_table.load(csv[1])
        else:
            raise Exception("Invalid number of CSV files.")
        
    #Function to save the Q-table to a CSV file
    def to_CSV(self, name):
        self.q_learning.to_CSV(name)

    #Function return the accumulated reward.
    def get_total_reward(self):
        return self.q_learning.get_sum()
    
    #Function to update team.
    def set_team(self, team):
        self._team = team

    #Function to convert Pokemon type to string.
    def type_to_string(self, pokemon_types):
        types = ""
        for type in pokemon_types:
            if type != 'None':
                types += type + "&"
        return types[:-1]

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