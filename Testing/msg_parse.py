#Imports
from typing import List
from Concept import TestPlayer

#Make into class

def msg_parse(player: TestPlayer, split_message: list):

    #Loop through message
    for msg in split_message:
        
        #Check if move
        if msg[1] == "move":
            if msg[2][0:2] == "p1":
                player.current_pokemon = msg[2].split(": ")[1]
                move = msg[3]
            elif msg[2][0:2] == "p2":
                player.opposing_pokemon = msg[2].split(": ")[1]

        #Check damage
        elif msg[1] == "-damage":

            if msg[3][0:1] == "0":
                hp = 0
                print("Fainted")
            else:
                hp = int(msg[3].split("/")[0])

            if msg[2][0:2] == "p1":
                player.previous_hp = player.current_hp
                print("Previous hp: " + str(player.previous_hp))
                player.current_hp = hp
                print("Current hp: " + str(player.current_hp))

                print("p1 " + str(player.current_pokemon) + " hp lost:" + str(-(player.previous_hp - player.current_hp)))
            elif msg[2][0:2] == "p2":
                player.pre_opposing_hp = player.opposing_hp
                player.opposing_hp = hp

        #Check switch
        elif msg[1] == "switch":
            hp = int(msg[4].split("/")[0])

            if msg[2][0:2] == "p1":
                player.current_pokemon = msg[2].split(" ")[1]
                player.previous_hp = player.current_hp
                player.current_hp = hp
                print("Switch hp: " + str(player.current_hp))
                
            elif msg[2][0:2] == "p2":
                player.opposing_pokemon = msg[2].split(" ")[1]
                player.pre_opposing_hp = player.opposing_hp
                player.opposing_hp = hp

    #State
    state = player.current_pokemon + "_" + player.opposing_pokemon
   
    #print("p2 " + str(opposing_pokemon) + " hp lost:" + str(-(pre_opposing_hp - opposing_hp)))
    reward = -(player.previous_hp - player.current_hp) + (player.pre_opposing_hp - player.opposing_hp)
    #print(state + str(reward))

'''
    if split_message[1] in ["drag", "switch"]:
        pokemon, details, hp_status = split_message[2:5]
        self._switch(pokemon, details, hp_status)
    elif split_message[1] == "-damage":
        pokemon, hp_status = split_message[2:4]
        self.get_pokemon(pokemon)._damage(hp_status)
        self._check_damage_message_for_item(split_message)
        self._check_damage_message_for_ability(split_message)
    elif split_message[1] == "move":
        failed = False
        override_move = None
        reveal_other_move = False

        for move_failed_suffix in ["[miss]", "[still]", "[notarget]"]:
            if split_message[-1] == move_failed_suffix:
                split_message = split_message[:-1]
                failed = True

        if split_message[-1] == "[notarget]":
            split_message = split_message[:-1]

        if split_message[-1] in {"[from]lockedmove", "[from]Pursuit", "[zeffect]"}:
            split_message = split_message[:-1]

        if split_message[-1].startswith("[anim]"):
            split_message = split_message[:-1]

        if split_message[-1] == "null":
            split_message = split_message[:-1]

        if split_message[-1].startswith("[from]move: "):
            override_move = split_message.pop()[12:]

            if override_move == "Sleep Talk":
                # Sleep talk was used, but also reveals another move
                reveal_other_move = True
            elif override_move == "Copycat":
                pass
            else:
                self.logger.warning(
                    "Unmanaged [from]move message received - move %s in cleaned up "
                    "message %s in battle %s turn %d",
                    override_move,
                    split_message,
                    self.battle_tag,
                    self.turn,
                )

        if split_message[-1].startswith("[from]ability: "):
            revealed_ability = split_message.pop()[15:]
            pokemon = split_message[2]
            self.get_pokemon(pokemon).ability = revealed_ability

            if revealed_ability == "Magic Bounce":
                return
            elif revealed_ability == "Dancer":
                return
            else:
                self.logger.warning(
                    "Unmanaged [from]ability: message received - ability %s in "
                    "cleaned up message %s in battle %s turn %d",
                    revealed_ability,
                    split_message,
                    self.battle_tag,
                    self.turn,
                )
        if split_message[-1] == "[from]Magic Coat":
            return

        if split_message[-1].startswith("[spread]"):
            split_message = split_message[:-1]

        while split_message[-1] == "[still]":
            split_message = split_message[:-1]

        if split_message[-1] == "":
            split_message = split_message[:-1]

        if len(split_message) == 4:
            pokemon, move = split_message[2:4]
        elif len(split_message) == 5:
            pokemon, move, presumed_target = split_message[2:5]

            if len(presumed_target) > 4 and presumed_target[:4] in {
                "p1: ",
                "p2: ",
                "p1a:",
                "p1b:",
                "p2a:",
                "p2b:",
            }:
                pass
            else:
                self.logger.warning(
                    "Unmanaged move message format received - cleaned up message %s"
                    " in battle %s turn %d",
                    split_message,
                    self.battle_tag,
                    self.turn,
                )
        else:
            pokemon, move, presumed_target = split_message[2:5]
            self.logger.warning(
                "Unmanaged move message format received - cleaned up message %s in "
                "battle %s turn %d",
                split_message,
                self.battle_tag,
                self.turn,
            )

        # Check if a silent-effect move has occurred (Minimize) and add the effect

        if move.upper().strip() == "MINIMIZE":
            temp_pokemon = self.get_pokemon(pokemon)
            temp_pokemon._start_effect("MINIMIZE")

        if override_move:
            self.get_pokemon(pokemon)._moved(override_move, failed=failed)
        if override_move is None or reveal_other_move:
            self.get_pokemon(pokemon)._moved(
                move, failed=failed, use=not reveal_other_move
            )
    elif split_message[1] == "cant":
        pokemon, _ = split_message[2:4]
        self.get_pokemon(pokemon)._cant_move()
    elif split_message[1] == "turn":
        self.end_turn(int(split_message[2]))
    elif split_message[1] == "-heal":
        pokemon, hp_status = split_message[2:4]
        self.get_pokemon(pokemon)._heal(hp_status)
        self._check_heal_message_for_ability(split_message)
        self._check_heal_message_for_item(split_message)
    elif split_message[1] == "-boost":
        pokemon, stat, amount = split_message[2:5]
        self.get_pokemon(pokemon)._boost(stat, int(amount))
    elif split_message[1] == "-weather":
        weather = split_message[2]
        if weather == "none":
            self._weather = {}
            return
        else:
            self._weather = {Weather.from_showdown_message(weather): self.turn}
    elif split_message[1] == "faint":
        pokemon = split_message[2]
        self.get_pokemon(pokemon)._faint()
    elif split_message[1] == "-unboost":
        pokemon, stat, amount = split_message[2:5]
        self.get_pokemon(pokemon)._boost(stat, -int(amount))
    elif split_message[1] == "-ability":
        pokemon, ability = split_message[2:4]
        self.get_pokemon(pokemon).ability = ability
    elif split_message[1] == "-start":
        pokemon, effect = split_message[2:4]
        pokemon = self.get_pokemon(pokemon)
        pokemon._start_effect(effect)

        if pokemon.is_dynamaxed:
            if pokemon in set(self.team.values()) and self._dynamax_turn is None:
                self._dynamax_turn = self.turn
            # self._can_dynamax value is set via _parse_request()
            elif (
                pokemon in set(self.opponent_team.values())
                and self._opponent_dynamax_turn is None
            ):
                self._opponent_dynamax_turn = self.turn
                self.opponent_can_dynamax = False
    elif split_message[1] == "-activate":
        target, effect = split_message[2:4]
        if target:
            self.get_pokemon(target)._start_effect(effect)
    elif split_message[1] == "-status":
        pokemon, status = split_message[2:4]
        self.get_pokemon(pokemon).status = status
    elif split_message[1] == "rule":
        self._rules.append(split_message[2])

    elif split_message[1] == "-clearallboost":
        self._clear_all_boosts()
    elif split_message[1] == "-clearboost":
        pokemon = split_message[2]
        self.get_pokemon(pokemon)._clear_boosts()
    elif split_message[1] == "-clearnegativeboost":
        pokemon = split_message[2]
        self.get_pokemon(pokemon)._clear_negative_boosts()
    elif split_message[1] == "-clearpositiveboost":
        pokemon = split_message[2]
        self.get_pokemon(pokemon)._clear_positive_boosts()
    elif split_message[1] == "-copyboost":
        source, target = split_message[2:4]
        self.get_pokemon(target)._copy_boosts(self.get_pokemon(source))
    elif split_message[1] == "-curestatus":
        pokemon, status = split_message[2:4]
        self.get_pokemon(pokemon)._cure_status(status)
    elif split_message[1] == "-cureteam":
        pokemon = split_message[2]
        team = (
            self.team if pokemon[:2] == self._player_role else self._opponent_team
        )
        for mon in team.values():
            mon._cure_status()
    elif split_message[1] == "-end":
        pokemon, effect = split_message[2:4]
        self.get_pokemon(pokemon)._end_effect(effect)
    elif split_message[1] == "-endability":
        pokemon = split_message[2]
        self.get_pokemon(pokemon).ability = None
    elif split_message[1] == "-enditem":
        pokemon, item = split_message[2:4]
        self.get_pokemon(pokemon)._end_item(item)
    elif split_message[1] == "-fieldend":
        condition = split_message[2]
        self._field_end(condition)
    elif split_message[1] == "-fieldstart":
        condition = split_message[2]
        self._field_start(condition)
    elif split_message[1] in ["-formechange", "detailschange"]:
        pokemon, species = split_message[2:4]
        self.get_pokemon(pokemon)._forme_change(species)
    elif split_message[1] == "-invertboost":
        pokemon = split_message[2]
        self.get_pokemon(pokemon)._invert_boosts()
    elif split_message[1] == "-item":
        pokemon, item = split_message[2:4]
        self.get_pokemon(pokemon).item = to_id_str(item)
    elif split_message[1] == "-mega":
        if not split_message[2].startswith(self._player_role):  # pyre-ignore
            self._opponent_can_mega_evolve = False  # pyre-ignore
        pokemon, megastone = split_message[2:4]
        self.get_pokemon(pokemon)._mega_evolve(megastone)
    elif split_message[1] == "-mustrecharge":
        pokemon = split_message[2]
        self.get_pokemon(pokemon).must_recharge = True
    elif split_message[1] == "-prepare":
        try:
            attacker, move, defender = split_message[2:5]
            defender = self.get_pokemon(defender)
            if to_id_str(move) == "skydrop":
                defender._start_effect("Sky Drop")
        except ValueError:
            attacker, move = split_message[2:4]
            defender = None
        self.get_pokemon(attacker)._prepare(move, defender)
    elif split_message[1] == "-primal":
        pokemon = split_message[2]
        self.get_pokemon(pokemon)._primal()
    elif split_message[1] == "-setboost":
        pokemon, stat, amount = split_message[2:5]
        self.get_pokemon(pokemon)._set_boost(stat, int(amount))
    elif split_message[1] == "-sethp":
        pokemon, hp_status = split_message[2:4]
        self.get_pokemon(pokemon)._set_hp(hp_status)
    elif split_message[1] == "-sideend":
        side, condition = split_message[2:4]
        self._side_end(side, condition)
    elif split_message[1] == "-sidestart":
        side, condition = split_message[2:4]
        self._side_start(side, condition)
    elif split_message[1] == "-swapboost":
        source, target, stats = split_message[2:5]
        source = self.get_pokemon(source)
        target = self.get_pokemon(target)
        for stat in stats.split(", "):
            source._boosts[stat], target._boosts[stat] = (
                target._boosts[stat],
                source._boosts[stat],
            )
    elif split_message[1] == "-transform":
        pokemon, into = split_message[2:4]
        self.get_pokemon(pokemon)._transform(self.get_pokemon(into))
    elif split_message[1] == "-zpower":
        if not split_message[2].startswith(self._player_role):  # pyre-ignore
            self._opponent_can_mega_z_move = False  # pyre-ignore

        pokemon = split_message[2]
        self.get_pokemon(pokemon)._used_z_move()
    elif split_message[1] == "clearpoke":
        self._in_team_preview = True
    elif split_message[1] == "gen":
        self._format = split_message[2]
    elif split_message[1] == "inactive":
        if "disconnected" in split_message[2]:
            self._anybody_inactive = True
        elif "reconnected" in split_message[2]:
            self._anybody_inactive = False
            self._reconnected = True
    elif split_message[1] == "player":
        if len(split_message) == 6:
            player, username, avatar, rating = split_message[2:6]
        else:
            if not self._anybody_inactive:
                if self._reconnected:
                    self._reconnected = False
                else:
                    raise RuntimeError(f"Invalid player message: {split_message}")
            return
        if username == self._player_username:
            self._player_role = player
        return self._players.append(
            {
                "username": username,
                "player": player,
                "avatar": avatar,
                "rating": rating,
            }
        )
    elif split_message[1] == "poke":
        player, details = split_message[2:4]
        self._register_teampreview_pokemon(player, details)
    elif split_message[1] == "raw":
        username, rating_info = split_message[2].split("'s rating: ")
        rating = int(rating_info[:4])
        if username == self.player_username:
            self._rating = rating
        elif username == self.opponent_username:
            self._opponent_rating = rating
        else:
            self.logger.warning(
                "Rating information regarding an unrecognized username received. "
                "Received '%s', while only known players are '%s' and '%s'",
                username,
                self.player_username,
                self.opponent_username,
            )
    elif split_message[1] == "replace":
        pokemon = split_message[2]
        details = split_message[3]
        self._end_illusion(pokemon, details)
    elif split_message[1] == "start":
        self._in_team_preview = False
    elif split_message[1] == "swap":
        pokemon, position = split_message[2:4]
        self._swap(pokemon, position)
    elif split_message[1] == "teamsize":
        player, number = split_message[2:4]
        number = int(number)
        self._team_size[player] = number
    elif split_message[1] in {"message", "-message"}:
        self.logger.info("Received message: %s", split_message[2])
    elif split_message[1] == "-immune":
        if len(split_message) == 4:
            mon, cause = split_message[2:]

            if cause.startswith("[from] ability:"):
                ability = cause.replace("[from] ability:", "")
                self.get_pokemon(mon).ability = to_id_str(ability)
    elif split_message[1] == "-swapsideconditions":
        self._side_conditions, self._opponent_side_conditions = (
            self._opponent_side_conditions,
            self._side_conditions,
        )
    elif split_message[1] == "title":
        player_1, player_2 = split_message[2].split(" vs. ")
        self.players = player_1, player_2
    else:
        raise NotImplementedError(split_message)

'''
