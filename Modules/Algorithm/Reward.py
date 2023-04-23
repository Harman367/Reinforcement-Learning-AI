#Imports
import re
from Modules.Agent import AI_Player

#Make into class

def get_reward(player: AI_Player, split_message: list):

    #Check if updating the Q-table.
    skip = False

    #Check if the AI attacked first
    atk_first = True

    #Reward
    reward = 0

    #Resisted damage
    resisted = False
    opponent_resisted = False

    #Super effective damage
    super_effective = False
    opponent_super_effective = False

    #Critical hit
    critical = False
    opponent_critical = False

    #Loop through message
    for count, msg in enumerate(split_message):
        #Check if move
        if msg[1] == "move":

            #Check which player used the move
            if msg[2][0:2] == "p1":
                
                player.current_pokemon = msg[2].split(": ")[1]
                player.move = re.sub('[^A-Za-z]', '', msg[3].lower().replace(" ", ""))

                #Check Q-table type.
                if player.table_type == 1:
                    player.current_pokemon = player.type_to_string(player.pokemon_types[player.current_pokemon])
                    player.move = player.move_types[player.move]

                #print("Move choosen: " + player.move)
                #print("Action choosen: " + str(player.act))

            elif msg[2][0:2] == "p2":
                player.opposing_pokemon = msg[2].split(": ")[1]

                #Check Q-table type.
                if player.table_type == 1:
                    player.opposing_pokemon = player.type_to_string(player.pokemon_types[player.opposing_pokemon])

                if count == 0 : atk_first = False

        #Check damage
        elif msg[1] in ["-damage", "-sethp", "-heal"]:

            #Check if fainted
            if msg[3][0:1] == "0":
                hp = 0
                #print(split_message)
            else:
                hp = int(msg[3].split("/")[0])

            #Check which player
            if msg[2][0:2] == "p1":
                player.previous_hp = player.current_hp
                #print("Previous hp: " + str(player.previous_hp))
                player.current_hp = hp
                #print("Current hp: " + str(player.current_hp))

                #print("p1 " + str(player.current_pokemon) + " hp lost:" + str(-(player.previous_hp - player.current_hp)))

                if hp == 0 and not atk_first:
                    #print("!!!!!!!!!!!!!Fainted before attack!!!!!!!!!!!!!")
                    #print(f"Action that was selected: {player.act}")
                    player.move = str(player.act)[:-14]
                    if "hiddenpower" in player.move:
                        player.move = "hiddenpower"

                    #Check Q-table type.
                    if player.table_type == 1:
                        player.move = player.move_types[player.move]

                    #print(player.move)
                    reward -= 75

            elif msg[2][0:2] == "p2":
                player.pre_opposing_hp = player.opposing_hp
                player.opposing_hp = hp

                if hp == 0 and atk_first:
                    reward += 75

                #print("p2 " + str(player.opposing_pokemon) + " hp lost:" + str(-(player.pre_opposing_hp - player.opposing_hp)))

        #Check switch
        elif msg[1] in ["switch", "drag"]:
            hp = int(msg[4].split("/")[0])
            skip = True

            if msg[2][0:2] == "p1":
                player.current_pokemon = msg[2].split(" ")[1]
                player.previous_hp = player.current_hp
                player.current_hp = hp

                #Check Q-table type.
                if player.table_type == 1:
                    player.current_pokemon = player.type_to_string(player.pokemon_types[player.current_pokemon])

                #print("Switch to: " + str(player.current_pokemon))
                #print("Switch hp: " + str(player.current_hp))
                
            elif msg[2][0:2] == "p2":
                player.opposing_pokemon = msg[2].split(" ")[1]
                player.pre_opposing_hp = player.opposing_hp
                player.opposing_hp = hp

                #Check Q-table type.
                if player.table_type == 1:
                    player.opposing_pokemon = player.type_to_string(player.pokemon_types[player.opposing_pokemon])

            #State
            player.state = (player.current_pokemon + "_" + player.opposing_pokemon).lower()
            #print("State: " + str(player.state))

        #Check boost
        elif msg[1] == "-boost":
            if msg[2][0:2] == "p1":
                reward += int(msg[-1]) * 10
            elif msg[2][0:2] == "p2":
                reward -= int(msg[-1]) * 5

        #Check unboost
        elif msg[1] == "-unboost":
            if msg[2][0:2] == "p1":
                reward -= int(msg[-1]) * 5
            elif msg[2][0:2] == "p2":
                reward += int(msg[-1]) * 2.5

        #Check move resistance
        elif msg[1] == "-resisted":
            if msg[2][0:2] == "p1":
                resisted = True
            elif msg[2][0:2] == "p2":
                opponent_resisted = True

        #Check move effectiveness
        elif msg[1] == "-supereffective":
            if msg[1][0:2] == "p1":
                super_effective = True
            elif msg[1][0:2] == "p2":
                opponent_super_effective = True

        #Check move immunity
        elif msg[1] == "-immune":
            if msg[1][0:2] == "p1":
                reward += player.current_hp
            elif msg[1][0:2] == "p2":
                reward -= player.opposing_hp * 2

        #Check move critical hit.
        elif msg[1] == "-crit":
            if msg[1][0:2] == "p1":
                critical = True
            elif msg[1][0:2] == "p2":
                opponent_critical = True

        #Check move miss.
        elif msg[1] in ["-miss", "cant"]:
            if msg[2][0:2] == "p1":
                reward -= player.opposing_hp
            elif msg[2][0:2] == "p2":
                reward += player.current_hp / 2

        #Check status effect.
        elif msg[1] == "-status":
            if msg[2][0:2] == "p1":
                reward -= 25
            elif msg[2][0:2] == "p2":
                reward += 50

        #Check move fail
        elif msg[1] == "-fail":
            if msg[2][0:2] == "p1":
                reward -= 100
            elif msg[2][0:2] == "p2":
                reward += 50
                
        #Ignore and skip reward calculation.
        elif msg[1] in ["init", "title", "j", "gametype", "player", "teamsize", "gen", "tier", "rule", "start"]:
            skip = True

        #Ignore but don't skip reward calculation.
        elif msg[1] in ["upkeep", "-singleturn", "-start", "-enditem", "-start", "-sidestart","-activate", "-sideend",
                         "-weather", "-anim", "-singlemove", "-endability", "-transform", "-notarget", "turn", "-hint",
                         "-item", '-clearallboost', '-cureteam', '-end', '-prepare', "deinit", "-ability", "faint", "-curestatus"]:
            pass

        #Handle
        else:
            print(10*"!" + "Unhandled Message Needs to be handled: " + msg[1] + " " + 10*"!")
            print(msg)
            skip = True


    #Rewards

    #Reward for damage dealt.
    reward += (player.pre_opposing_hp - player.opposing_hp)

    #Reward for damage taken.
    reward += (player.current_hp - player.previous_hp)

    #Reward for attacking first.
    if atk_first:
        reward += 100
    elif not atk_first:
        reward -= 50

    #Reward for resisting.
    if resisted:
        reward += (player.previous_hp - player.current_hp) * 0.5

    if opponent_resisted:
        reward -= (player.pre_opposing_hp - player.opposing_hp) * 0.5

    #Reward for super effective.
    if super_effective:
        reward -= (player.previous_hp - player.current_hp) * 0.5

    if opponent_super_effective:
        reward += (player.pre_opposing_hp - player.opposing_hp) * 0.5

    #Reward for critical hit.
    if critical:
        reward -= (player.previous_hp - player.current_hp) * 0.5

    if opponent_critical:
        reward += (player.pre_opposing_hp - player.opposing_hp) * 0.5

    #State
    player.previous_state = player.next_state
    player.next_state = player.state

    #Update Q-table
    if player.previous_state != None and player.move != None and not skip:
        player.q_learning.update_table(player.previous_state, player.next_state, player.move, reward)

    
    #Check turn
    #if split_message[-1][1] == "turn":
        #print("\nTurn: " + str(split_message[-1][2]))
        #pass