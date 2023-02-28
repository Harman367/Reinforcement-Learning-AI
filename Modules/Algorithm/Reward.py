#Imports
import re
from Modules.Agent import AI_Player

#Make into class

def get_reward(player: AI_Player, split_message: list):

    skip = False

    #Loop through message
    for msg in split_message:
        
        #Check if move
        if msg[1] == "move":

            #Chech which player
            if msg[2][0:2] == "p1":
                player.current_pokemon = msg[2].split(": ")[1]
                player.move = re.sub('[^A-Za-z]', '', msg[3].lower().replace(" ", ""))
                print("Move choosen: " + player.move)

            elif msg[2][0:2] == "p2":
                player.opposing_pokemon = msg[2].split(": ")[1]

        #Check damage
        elif msg[1] in ["-damage", "-sethp"]:

            #Check if fainted
            if msg[3][0:1] == "0":
                hp = 0
            else:
                hp = int(msg[3].split("/")[0])

            #Check which player
            if msg[2][0:2] == "p1":
                player.previous_hp = player.current_hp
                #print("Previous hp: " + str(player.previous_hp))
                player.current_hp = hp
                #print("Current hp: " + str(player.current_hp))

                #print("p1 " + str(player.current_pokemon) + " hp lost:" + str(-(player.previous_hp - player.current_hp)))

            elif msg[2][0:2] == "p2":
                player.pre_opposing_hp = player.opposing_hp
                player.opposing_hp = hp

                #print("p2 " + str(player.opposing_pokemon) + " hp lost:" + str(-(player.pre_opposing_hp - player.opposing_hp)))

        #Check switch
        elif msg[1] in ["switch", "drag"]:
            hp = int(msg[4].split("/")[0])
            skip = True

            if msg[2][0:2] == "p1":
                player.current_pokemon = msg[2].split(" ")[1]
                player.previous_hp = player.current_hp
                player.current_hp = hp
                #print("Switch to: " + str(player.current_pokemon))
                #print("Switch hp: " + str(player.current_hp))
                
            elif msg[2][0:2] == "p2":
                player.opposing_pokemon = msg[2].split(" ")[1]
                player.pre_opposing_hp = player.opposing_hp
                player.opposing_hp = hp

            #State
            player.state = (player.current_pokemon + "_" + player.opposing_pokemon).lower()
            print("State: " + str(player.state))

        #Check ability
        elif msg[1] == "-ability":
            if msg[2][0:2] == "p1":
                pass
            elif msg[2][0:2] == "p2":
                pass

        #Check boost
        elif msg[1] == "-boost":
            if msg[2][0:2] == "p1":
                pass
            elif msg[2][0:2] == "p2":
                pass

            if msg[-2] in ["atk", "def", "spd", "spe", "spa"]:
                pass
            else:
                print(10*"!" + " Needs to be handled: " + msg[-2] + 10*"!")
                print(msg)

        #Check unboost
        elif msg[1] == "-unboost":
            if msg[2][0:2] == "p1":
                pass
            elif msg[2][0:2] == "p2":
                pass


            if msg[-2] in ["atk", "def", "spd", "spe", "spa"]:
                pass
            else:
                print(10*"!" + " Needs to be handled: " + msg[-2] + 10*"!")
                print(msg)

        #Check move resistance
        elif msg[1] == "-resisted":
            if msg[1][0:2] == "p1":
                pass
            elif msg[1][0:2] == "p2":
                pass

        #Check move effectiveness
        elif msg[1] == "-supereffective":
            if msg[1][0:2] == "p1":
                pass
            elif msg[1][0:2] == "p2":
                pass

        #Check move immunity
        elif msg[1] == "-immune":
            if msg[1][0:2] == "p1":
                pass
            elif msg[1][0:2] == "p2":
                pass

        #Check move critical hit.
        elif msg[1] == "-crit":
            if msg[1][0:2] == "p1":
                pass
            elif msg[1][0:2] == "p2":
                pass

        #Check move miss.
        elif msg[1] == "-miss":
            if msg[2][0:2] == "p1":
                pass
            elif msg[2][0:2] == "p2":
                pass

        #Check move heal.
        elif msg[1] == "-heal":
            if msg[2][0:2] == "p1":
                pass
            elif msg[2][0:2] == "p2":
                pass

        #Check status effect.
        elif msg[1] == "-status":
            if msg[2][0:2] == "p1":
                pass
            elif msg[2][0:2] == "p2":
                pass

        #Check start of effect.
        elif msg[1] == "-start":
            if msg[2][0:2] == "p1":
                pass
            elif msg[2][0:2] == "p2":
                pass


        #Check end of effect.
        elif msg[1] == "-end":
            if msg[2][0:2] == "p1":
                pass
            elif msg[2][0:2] == "p2":
                pass

        #Check move cant
        elif msg[1] == "cant":
            if msg[2][0:2] == "p1":
                pass
            elif msg[2][0:2] == "p2":
                pass

        #Check move fail
        elif msg[1] == "-fail":
            if msg[2][0:2] == "p1":
                pass
            elif msg[2][0:2] == "p2":
                pass

        #Check cure status
        elif msg[1] == "-curestatus":
            if msg[2][0:2] == "p1":
                pass
            elif msg[2][0:2] == "p2":
                pass

        #Check move prepare
        elif msg[1] == "-prepare":
            if msg[2][0:2] == "p1":
                pass
            elif msg[2][0:2] == "p2":
                pass

        #Ignore and skip reward calculation.
        elif msg[1] in ["init", "title", "j", "gametype", "player", "teamsize", "gen", "tier", "rule", "start"]:
            skip = True

        #Ignore but don't skip reward calculation.
        elif msg[1] in ["upkeep", "faint", "-singleturn", "-start", "-enditem", "-start", "-sidestart","-activate", "-sideend",
                         "-weather", "-anim", "-singlemove", "-endability", "-transform", "-notarget", "turn"]:
            pass

        #Handle
        else:
            print(10*"!" + " Needs to be handled: " + msg[1] + " " + 10*"!")
            print(msg)
            skip = True

    #Reward
    reward = -(player.previous_hp - player.current_hp) + (player.pre_opposing_hp - player.opposing_hp)

    #Update Q-table
    if player.state != None and player.move != None and not skip:
        player.q_learning.update_table(player.state, player.move, reward)

    
    #Check turn
    if split_message[-1][1] == "turn":
        print("\nTurn: " + str(split_message[-1][2]))