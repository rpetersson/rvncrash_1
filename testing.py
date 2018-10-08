import random
import time

def game_engine():
    counter = 1
    initial_chance = 100
    multipel_increment = 0.01
    game_crash = False

    while not game_crash:

        #round start
        initial_chance = initial_chance - multipel_increment
        counter = counter + multipel_increment
        print(round(counter,2))
        time.sleep(0.01)
        if random.uniform(0.01,100) > initial_chance:
            game_crash = True
            print("GAME CRASHED @ "+str(counter))
            print("New round starting")
            time.sleep(1)
            print("1")
            time.sleep(1)
            print("2")
            time.sleep(1)
            print("3")
            game_crash = False
            game_engine()


game_engine()