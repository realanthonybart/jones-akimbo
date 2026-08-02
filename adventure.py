#The Adventures of Jones Akimbo (Version 1.01)
#Created April 21st, 2023
#Last updated August 2nd, 2026
#By Anthony Bart
#This is a short text adventure heavily reliant on the easygui module.
#Interestingly enough, the idea for this concept came as a result of a login program I made
#while experimenting with easygui.
#Hope you enjoy!








from easygui import *
import random

money_found = False   #checks whether hiddenpath is done
drink_in_hole = False   #checks whether drink is being stored in the hole
drink_held = False  #checks whether drink is in inventory
store_done = False  #checks whether store is done
alley_first_visit = True #checks whether user has visited alley before




def randPass():  # generates a random password from this list at the beginning of a new play-through
    passwords = ["pineapple", "mojito", "applesauce", "mermaids", "fruitcakes", "fishsnacks"]
    keyword = random.choice(passwords)  # selects a random item from passwords list
    return keyword







def intro():     #intoductory message
    msgbox(
        msg="In this short game, you will take on the role of Jones Akimbo, an aspiring detective in the Western United States."
            "\nAfter years of vigorous investigation, you have finally found what you believe to be the headquarters "
            "of the Cannoli crime family. "
            "\n\nYour mission, should you choose to accept it, is to infiltrate the headquarters and subdue Al "
            "Cannoli, the criminal mastermind. "
            "\n\n\nUse any means necessary. Good luck, and Godspeed, Mr. Akimbo.",
        image="intro.gif",
        title="And so it begins...",
    )

    street(0)






def street(n):   #Main hub area -- the Street
    if n == 0:
        output = buttonbox(
            msg="In front of you are four paths. Which do you choose?",
            choices=["Alley", "Park", "Shady Door", "Store"],
            title="Street"
        )
    elif n > 0:
        output = buttonbox(
            msg="You return to the street. Which path do you choose?",
            choices=["Alley", "Park", "Shady Door", "Store"],
            title="Street"
        )
    if output == "Alley":
        alley()
    elif output == "Park":
        park()
    elif output == "Shady Door":
        doorKeeper(n)
    elif output == "Store":
        store()







def alley():  #Alley with password giver
    global alley_first_visit
    if alley_first_visit:
        output = buttonbox(
            msg="In the alley you see a mysterious man. What do you do?",
            title="Alley",
            choices=["Approach him", "Leave"],
            default_choice="Approach him"
        )

        if output == "Leave":
            street(1)
        elif output == "Approach him":
            msgbox(msg="'Mr. Akimbo. No need for introductions. I know what you're here for."
                       "\n\nYou wish to enter Al Cannoli's center of operations -- and for that, you'll need a password... "
                       "\n\nA password I'm willing to sell to you. For the right price of course..."
                       "\n\nBring me this limited edition Drappucino™, and the password is yours.'",
                   title="Mysterious Man")
            msgbox(msg="(The mysterious man passes you a photograph of the drink.)", image='drink.gif')
            if drink_held:
                msgbox(
                    msg="'Oh, you already have it? It seems you came prepared. In that case, the password is " + keyword + ".'",
                    title="Success!")
            alley_first_visit = False
            street(1)



    else:
        output = buttonbox(
            msg="You return to the mysterious man's mysterious alley.",
            title="Alley",
            choices=["Speak to the man", "Leave"],
        )
        if output == "Leave":
            street(1)
        elif output == "Speak to the man":
            if not drink_held:
                msgbox("'Hey man, no drink -- no password.'")
                street(1)


            elif drink_held and not alley_first_visit: #if drink is held, and visit is not first
                msgbox("'Thank you for the drink, my friend. The password is " + keyword + ".'")
                street(1)










def park():   #Hole in wall & leads to hiddenpath()
    global drink_in_hole
    global drink_held

    output = buttonbox(
        msg="You arrive at the park.",
        title="Park",
        choices=["???", "Hole in wall", "Leave"])

    if output == "???":
        hiddenpath()
    elif output == "Hole in wall":
        if drink_in_hole:
            msgbox("You retrieve the drink from the hole.")
            drink_in_hole = False
            drink_held = True
            park()
        else:
            msgbox("That hole in the wall seems to connect into the store.")
            park()
    elif output == "Leave":
        street(1)







def hiddenpath():  #location of secret money bag
    global money_found
    if money_found:
        msgbox("I took the money -- don't think I can do much else here.")
        park()
    else:
        output = buttonbox(
            msg="Off the beaten path, you find nothing but a large trash bin.",
            title="???",
            choices=["Examine", "Leave"],
            )

        if output == "Leave":
            park()

        elif output == "Examine":
            msgbox(
            msg="Inside, you find a hidden stash of money!",
            title="???")

            msgbox("You consider your bleak financial position, and decide to take the money.")
            money_found = True
            park()













def doorKeeper(n):   #Locked door leading into the endgame
    #print(keyword)  # used for testing
    if n == 0:
        output = buttonbox(
            msg="In front of you is a suspiciously out of place door -- it almost seems like a plot device.",
            title="Door",
            choices=["Knock", "Leave"],
            default_choice="Knock"
        )
    elif n > 0:
        output = buttonbox(
            msg="You return to the clearly out-of-place door.",
            title="Door",
            choices=["Knock", "Leave"],
        )

    if output == "Leave":
        street(1)
    elif output == "Knock":
        msgbox(msg="Suddenly, a peephole slides open. You find a lone eye staring right at you.")
        msgbox(msg="'Got a password, kid?'", image="door.gif")
        guess = passwordbox(title="Password", msg=" 'Got a password, kid?' ")  # password program
        if guess is None or guess == "":  # if user exits out, or inputs nothing
            msgbox("'Cat got your tongue? That's what I thought.'")
            street(1)
        elif guess.lower() == keyword:  # if password is correct
            msgbox("'Come on in.'", "Success!")
            boss()
        elif guess.lower() != keyword:  # if password is wrong
            msgbox("'Get lost, kid.'", "No dice...")
            street(1)
        n + 1








def store():     #Where drink must be purchased or stolen // so many if statements....
    global store_done
    global drink_held
    global drink_in_hole
    if store_done:  #kicks player out after being done with the area
        msgbox ("Now that I'm done with that drink, I better get back to finding Cannoli.")
        street(1)


    else:
        output = buttonbox(
            msg="You're looking around the local store.",
            title="Store",
            choices=["Cashier", "Drink", "Hole", "Leave"])

        if output == "Leave":
            if drink_held:
                msgbox("'Hey, man -- you gonna pay for that?'")
                output = buttonbox(
                    msg="You are in the store, holding the drink.",
                    title="Store",
                    choices=["Cashier", "Drink", "Hole", "Leave"])
            else:
                street(1)


        elif output == "Cashier":
            msgbox("'Nice weather today, eh?'")
            store()

        elif output == "Hole":
            msgbox("That hole seems to connect to the park... maybe I could slip something in there?")
            store()

        elif output == "Drink":
            msgbox("You pick up the drink.")
            drink_held = True


            while drink_held:

                output = buttonbox(
                msg="You are in the store, holding the drink.",
                title="Store",
                choices=["Cashier", "Drink", "Hole", "Leave"])

                if output == "Leave":
                    msgbox("'Hey, man -- you gonna pay for that?'")
                    continue #will repeat the above buttonbox -- super useful

                elif output == "Drink":
                    msgbox("You put the drink back where you found it.")
                    drink_held = False
                    store()

                elif output == "Hole":
                    msgbox("You put the drink inside the hole, and head for the exit.")
                    drink_in_hole = True
                    drink_held = False
                    store_done = True
                    street(1)


                elif output == "Cashier":

                    if money_found:
                        msgbox("That'll be $9.95. Have a good day!")
                        store_done = True
                        street(1)

                    else:
                        msgbox("Sorry man, seems like you don't have enough money.")



def boss(): #Endgame
    global drink_held
    drink_held = False #the player no longer needs it -- also fixes some bugs
    msgbox(
        msg = "You enter the safehouse. In front of you is a shady, middle-aged Italian man.",
        image = "boss.gif"
        )
    
    msgbox(
        msg = "'So, Mr. Akimbo... You`ve finally made it. You kept me waiing, you know."
        "\n\nI'll cut to the chase. I'm an old man.... It`s time for me to retire. I know you`re here to arrest "
        "me, but just for you -- I have an offer you can't refuse. \n\n\nYou managed to track me down, "
        "so I figure you deserve to take the reins here. I`ll disappear into the night, and "
        "you`ll get the oppurtunity for a life more luxurious than you could ever imagine."
        "\n\n\n\nThink it through, Mr. Akimbo. It's all up to you.'",
        title = "In the belly of the beast..."
        )
        
    output = buttonbox(
            msg="'Think it through, Mr. Akimbo. It's all up to you.'",
            title="Decisions, decisions...",
            choices=["Take his place", "Arrest him"]
    )
    if output == "Take his place":
        forsaken()
    elif output == "Arrest him":
        saviour()








def forsaken():  #Ending 1
    msgbox(
        msg = "And that was the last I ever heard of Al Cannoli. He disappeared like a whisper in the night, "
        "never to resurface again. Though he never lied -- The city is under my complete control, and my life "
        "sure is lavish. But seeing the city in this disturbed state, not bringing justice to it anymore -- "
        "it makes me wonder if I made the right decision back then....", 
        title = "The end.",
        image = 'forsaken.gif'
        )










def saviour(): #Ending 2
    msgbox(
        msg ="But I wasn't buying any of that. I arrested Cannoli right then and there. No promises of "
        "luxury and grandeur will sway my sense of jusice -- and with Cannoli's generals still out there, "
        "I'm just getting started!",
        title = "More to come!",
        image = 'saviour.gif'
        )








keyword = randPass()   #initalizing a random password
randPass()
intro()   #running the game






msgbox("Thank you for playing."   #exit message
       "\n-Anthony")
exit()







# Scrapped goback() function idea for lack of efficiency
# Overall fun project; pleased with how this came out

