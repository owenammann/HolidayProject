# Owen Ammann
# 12/30/15
# Holiday Fun: Santa's Workshop Simulator


# Notes: Each elf will produce more toys the happier they are
# Each elf will be happier with more cookies (wage)
# elves use sugar to create the toys
# each toy will yield higher cookies for christmas
# the manager will have 7 days to prepare for christmas
# if elves are unhappy, they will quit.
# if elves are happy, more will join and the player will have to
# split the budget more evenly

# Game counts toys in hundreds

# There is a dictionary to explain all the vocab for this game
# This game is designed to teach the concept of linear programming, and diminished returns.


# imports
import random


def introduction():
    """Introduction"""
    print(
        """
Welcome to the Santa's Workshop Simulator!

Santa has put you in charge of his magical workshop
and it's only 7 days until Christmas Eve!
You're in charge of setting the wage for each elf in cookies,
and making sure they are supplied with sugar to make the toys!

Your goal is to make as many toys as possible in the 7 day period!
"""
    )


def runProgramPrompt():
    """Asks the user if they would like to play again"""
    response = ""
    while response.lower() not in ("yes", "no"):
        response = input("Would you like to play again?\n")
        if response.lower() not in ("yes", "no"):
            print("Invalid response.")

    if response.lower() == "yes":
        runProgram = True
    elif response.lower() == "no":
        runProgram = False

    return runProgram


class Elf(object):
    """A virtual elf worker"""
    elves = 20  # starting amount of elves

    def sendElves():
        # sends elves to the game
        return elf.elves

    def mood(game):
        """the mood of the elf based off wage"""
        # A low wage will make a large percentage quit

        wage = game.sendWage()
        # string values for each mood
        angryMoods1 = ["Infuriated", "On-strike", "Belligerent", "In uproar"]
        angryMoods2 = ["Depressed", "Barely scraping by"]
        angryMoods3 = ["Facing hard times", "sad"]
        neutralMoods = ["Meh", "Been better", "Working the 9-5 grind"]
        happyMoods1 = ["Pretty good", "happy", "pleased"]
        happyMoods2 = ["Joyous", "Celebrating", "Euphoric"]

        if 0 <= wage < 1:
            mood = 0
            text = random.choice(angryMoods1)
        elif 1 <= wage < 3:
            mood = 1
            text = random.choice(angryMoods2)
        elif 3 <= wage < 6:
            text = random.choice(angryMoods3)
            mood = 2
        elif 6 <= wage < 8:
            mood = 3
            text = random.choice(neutralMoods)
        elif 8 <= wage < 10:
            mood = 4
            text = random.choice(happyMoods1)
        elif wage >= 10:
            mood = 5
            text = random.choice(happyMoods2)

        print("\nThe elves are: ", text)
        return mood

    def __toyRateSet(mood):
        """Determines the rate per elf based off the mood"""
        # diminished returns
        if mood == 0:
            toyRate = 0
        elif mood == 1:
            toyRate = random.randrange(1, 3)
        elif mood == 1:
            toyRate = random.randrange(3, 5)
        elif mood == 2:
            toyRate = random.randrange(5, 6)
        elif mood == 3:
            toyRate = random.randrange(6, 7)
        elif mood == 4:
            toyRate = random.randrange(7, 8)
        elif mood == 5:
            toyRate = 8

        return toyRate

    def elfChange(mood):
        """Decides the amount of elves that quit or are hired"""
        # randomly chooses based off mood
        if mood == 0:
            hireFactor = random.randrange(-4, -1)
        elif mood == 1:
            hireFactor = random.randrange(-2, 0)
        elif mood == 2:
            hireFactor = random.randrange(-1, 1)
        elif mood == 3:
            hireFactor = random.randrange(0, 2)
        elif mood == 4:
            hireFactor = random.randrange(0, 3)
        elif mood == 5:
            hireFactor = random.randrange(1, 4)

        return hireFactor

    def produce(sugar):
        wage = game.sendWage()
        cookies = game.sendCookies()
        # Checks if player has enough cookies
        if elf.elves * wage > cookies:
            print("Not enough cookies to pay each elf!")
            produceVar = False  # doesn't let game go to the next day
            toysMade = 0
            sugar = game.sugar
            return produceVar, toysMade, sugar
        # enough cookies, begin working!!
        else:
            produceVar = True  # gives game green light
            # determines mood
            mood = elf.mood(game)

            # toys per elf
            toyRate = elf.__toyRateSet(mood)

            # produces toys until the elves are out of sugar

            # each elf makes toys
            toysMade = 0
            for i in range(elf.elves):
                # for each 100 toys each elf makes, game subtracts 20 sugar
                for i in range(toyRate):
                    # checks if there's enough sugar
                    if sugar >= 20:
                        sugar -= 20
                        toysMade += 1
            return produceVar, toysMade, sugar

    def hire():
        # adds or deletes elves based off mood at end of day
        mood = elf.mood(game)
        hireFactor = elf.elfChange(mood)

        # prints how many elves quit/hired

        # determines whether the game prints "elf" or "elves"
        elfWord = ""
        if abs(hireFactor) == 1:
            elfWord = "elf"
        else:
            elfWord = "elves"
        if hireFactor < 0 and elf.elves + hireFactor >= 0:
            print("\n", 0 - hireFactor, elfWord, " quit today!")
            # make it positive
            elf.elves += hireFactor
        # defines new hirefactor in case elves goes negative
        elif hireFactor < 0 and elf.elves + hireFactor < 0:
            print("\n", elf.elves, " elves quit!")
            elf.elves = 0

        # incase there's one more elf and they go negative
        elif elf.elves == 1 and hireFactor < 0:
            print("\n1 elf has quit!")
            elf.elves = 0
        # in case there's no more elves and they go negative
        elif elf.elves == 0 and hireFactor < 0:
            print("\n 0 elves have been hired!")
            elf.elves = 0
        elif hireFactor >= 0:
            print("\nYou hired", hireFactor, elfWord, " today!")
            elf.elves += hireFactor
        return elf.elves


class Game(object):
    """The player's input"""
    # starting variables

    sugar = 6000  # supplies to make the toys, can buy more with cookies
    cookies = 2000  # currency to pay the elves
    toys = 0  # toys made
    wage = 0  # amount of cookies to pay the elves
    day = 1  # game ends when day reaches 7

    def __init__(self):
        introduction()  # prints the introduction when player starts

    def command(self):
        quitVar = False  # whether the plyaer quits
        run = True  # loop for gameplay
        while run == True:
            print("Good morning!")
            # warns player if it's the last day
            if game.day == 7:
                print("It's Christmas eve!")
            # the commands
            if game.day <= 7:
                # game automatically displays data
                game.__display()

                prompt = "\nType and enter any of the following commands to run your workshop:\n\
    \tWage (Sets the wage.)\n\
    \tProduce (The elves make the toys, and the next day begins.)\n\
    \tMood (Prints the mood of the elves.)\n\
    \tBuy (Buys sugar with cookies.)\n\
    \tSell (Sells sugar for cookies.)\n\
    \tHelp (Opens the dictionary.)\n\
    \tQuit (Quits the game.)\n"
                command = input(prompt)

                # the player's commands if statements
                # set the wage
                if command.lower() == "produce":

                    # ends the day and sets variables
                    game.__produce(elf)
                    elf.hire()
                elif command.lower() == "wage":
                    # sets the wage
                    game.__wage()

                elif command.lower() == "mood":
                    elf.mood(game)

                elif command.lower() == "buy":
                    game.__buy()

                elif command.lower() == "help":
                    game.__dictionary()

                elif command.lower() == "quit":
                    run = False
                elif command.lower() == "sell":
                    game.__sell()
                else:
                    print("Invalid input.")
            if game.day == 8:
                print(
                    """
Merry Christmas!!!
Santa ships all the toys.
"""
                )  # game counts toys in hundreds
                print("\nSanta delivers: ", game.toys * 100, " toys!")
                print("\nStats:")
                game.__display()
                print("Game over.")
                run = False

        if command.lower() == "quit":
            quitVar = True
            print("Day: ", game.day)
            print("Toys: ", game.toys * 100)

        return quitVar

    def __buy(self):
        print("\n1 gram of sugar costs .5 cookies.")
        buySet = False
        while buySet == False:
            while True:
                try:
                    buy = float(input("How many grams of sugar would you like?\n"))
                except ValueError:
                    print("Please enter a number for the grams of sugar.")
                    continue
                else:
                    break
            # if there aren't enough cookies
            if buy * .5 > game.cookies:
                print("Not enough cookies!")
                buySet = False

            else:
                game.sugar += buy
                game.cookies -= .5 * buy
                buySet = True

    def __sell(self):
        print("\n1 gram of sugar costs .5 cookies.")
        sellSet = False
        while sellSet == False:
            while True:
                try:
                    sell = float(input("How many grams of sugar would you like to sell?\n"))
                except ValueError:
                    print("Please enter a number for the grams of sugar.")
                    continue
                else:
                    break
            # if there isn't enough sugar
            if sell > game.sugar:
                print("Not enough sugar!")
                sellSet = False

            else:
                game.sugar -= sell
                game.cookies += .5 * sell
                sellSet = True

    def __dictionary(self):
        """A dictionary for the user"""
        dictionary = {"elf": "A tiny worker in Santa's workshop.\n\
Elves work most effieciently at 10 cookies per day.", \
                      "cookie": "The currency of the north pole.\n\
Can buy 2 grams of sugar with one cookie.", \
                      "sugar": "The building supplies for the toys.\n\
Each toy uses .2 grams of sugar.", \
                      "toy": "The product. Santa ships these on Christmas Eve.\n\
Can you make the most toys this year?", \
                      "wage": "Daily cookie salary per elf."}
        response = ""
        print("Words:")
        for i in dictionary:
            print("\t", i)
        while response != "exit":
            response = input("\nWhat word would you like a definition of?\n\
Input \"exit\" to exit.\n")
            if response.lower() not in dictionary and response.lower() != "exit":
                print("\n" and response.title() and " not in dictionary!")
            elif response.lower() in dictionary:
                print(dictionary[response.lower()])

    def __display(self):
        """displays these values before every command"""
        elves = elf.sendElves()
        print("\nSupplies:")
        print("\tSugar: ", game.sugar)
        print("\tCookies: ", game.cookies)
        print("\tWage: ", game.wage)
        print("\tDay: ", game.day)

        print("\nToys:", end="")
        print("\t", game.toys * 100)  # toys are counted in hundreds

        print("\nElves: ", end="")
        print("\t", elves)

    def __wage(self):
        """Set the day's wage for the elves"""
        elves = elf.sendElves()
        print("\nBudget: ", game.cookies, " cookies.")
        print("Elves: ", elves)
        # in case the wage will deplete the cookie supply

        wageSet = False
        while wageSet == False:
            while True:
                try:
                    game.wage = float(input("\nWhat is today's wage in cookies for each elf?\n"))
                except ValueError:
                    print("Please enter a number for the elves' wage.")
                    continue
                else:
                    break
            if game.cookies - game.wage * elves < 0:
                print("You don't have enough cookies!\n\
Choose a lower wage.")
                wageSet = False
            elif game.cookies < 0:
                print("Wage can't be negative!\n\
choose a positive wage.")
                wageSet = False
            else:
                wageSet = True

    def sendWage(self):
        # sends the wage to the elves
        return game.wage

    def sendCookies(self):
        # sends the cookies in total to calculate if there are enough
        return game.cookies

    def __produce(self, elf):

        # the elves work!
        elves = elf.sendElves()

        produceVar, toysMade, game.sugar = elf.produce(game.sugar)

        if produceVar == True:
            # Toys are counted in hundreds
            print("The elves made ", toysMade * 100, " toys today!")

            # toys added to the total
            game.toys += toysMade

            # deletes cookies based off wage and number of elves
            game.cookies -= game.wage * elves

            # changes day
            game.day += 1

        else:
            print("\nSet a lower wage for the elves to continue.")
            game.command()


# main
runProgram = True
while runProgram == True:
    # start the game
    elf = Elf
    game = Game()
    # player's commands
    quitVar = game.command()  # if the user quit the game, it won't prompt the user to play again
    # returns this value at end of game

    if quitVar == True:
        print("\nUntil next time!")
        runProgram = False
    else:
        runProgram = runProgramPrompt()

input("\nPress enter to exit.")
