# created on: Oct 15, 2018
# Author: Win.thitiwat


"""
Text-Adventure-Game (This is an exercise from Python-for-DataScience Class)

-- Purpose --
    To demonstrate how to construct a structure-based on a game map

-- Introduction --
    In this game, there are 3 stages on our game's map.
    The map structure are hereafter:


                            win         win          win
        intro ----> stage1 ----> stage2 ----> stage3 ----> Win
                      |     |       |            |
                      `-----'        `-----------`------> Fail
                     continue              ^
                      stage2          if both stage 1 & 2 fail

          * In order to go to complete the game, player can either fail or pass the first 2 stages, but not fail both
          ** Then the player have to pass the last stage for winning the game.
-- Bugs not yet worked out --
    some defined ascii art variables displayed in a strange format in the terminal irrespective to its initial design

"""

import time
import sys
import os


# ****************************
#
# Start Defining Key Variables
#
# ****************************


COFFEE_ASCII_ART = """
                (  )   (   )  )
                 ) (   )  (  (
                 ( )  (    ) )
                 _____________
                <_____________> ___
                |             |/ _ \
                |               | | |
                |               |_| |
             ___|             |\___/
            /    \___________/    \
            \_____________________/
            
"""

ARCHER_ASCII_ART = """


                /`. 
               /   :. 
              /     \\ 
           ,;/,      ::                                 / __ \  
       ___:c/.(      ||                         /|     ( (  \ \
     ,'  _|:)>>>--,-'B)>                   |^v^v v|     \_\/ ) )
    (  '---'\--'` _,'||                    \ ____ /         / /
     `--.    \ ,-'   ;;                    ,Y`   `,        | |
         |    \|    //                     || * * )        { }
         |     \   ;'                      \\  _\ |        | |
         |_____|\,'                         \\/ _'\_      / / 
         :     :                            /|  ~ | ``\   | |
         |  ,  |                         ,_` \    |  \ \ _|_|
         | : \ :                        /     |   |  |  \/(_}
         | | : :                       |      |   |  | ' \| |   
         | | | |                       |     | \  |   \ _/ \ \
         | | |_`.
         '--`
         Assassin                             The King 

"""

TIMER = [
    """
            ██████╗ 
            ╚════██╗
             █████╔╝
             ╚═══██╗
            ██████╔╝
            ╚═════╝
     """,
    """
            ██████╗ 
            ╚════██╗
            █████╔╝
            ██╔═══╝ 
            ███████╗
            ╚══════╝
    """,
    """
             ██╗
            ███║
            ╚██║
             ██║
             ██║
             ╚═╝     
    """,
    """
        
        
    ███████╗████████╗ █████╗ ██████╗ ████████╗
    ██╔════╝╚══██╔══╝██╔══██╗██╔══██╗╚══██╔══╝
    ███████╗   ██║   ███████║██████╔╝   ██║   
    ╚════██║   ██║   ██╔══██║██╔══██╗   ██║   
    ███████║   ██║   ██║  ██║██║  ██║   ██║   
    ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
                                          
                                                                                        
    """]


INTRO = ["""
    You are a prisoner under the ID 24601 who just broke a windowpane and stole a loaf of bread 
    
    to feed your starving daughter. You were judged to be imprisoned for 15 years. Also, you know that your 
    
    daughter has been looked after by a shady hotel's owner and you cannot wait to take her out!!!. 


    Luckily, at the 9th year of your imprisonment, you are pardoned by the King of our city and you are given

    with a good job in the Hult Palace where the King is living.
""", """
    Welcome to Hult Palace, you are cordially invited by the king to his palace to be in charge of his private caretaker.

    !!! But you need to PASS our intensive training first before starting the job!!!
    
    The perk you will get from this job if you PASS our intensive training:
       
        1. Out of the prison without any parole
        2. Free Food/accommodation for your family in the Palace
        3. Personal guards when travelling
        4. Live like a king, but not
        5. Lastly, you will live with your DAUGHTER
        
    *** HOWEVER, if you FAIL our training's test, you will be sent to Alcatraz prison for LIFE IMPRISONMENT ***
    
                                __            ================================
                     ALCATRAZ  /__\            ||     ||<(.)>||<(.)>||     || 
                   ____________|  |            ||    _||     ||     ||_    || 
                   |_|_|_|_|_|_|  |            ||   (__D     ||     C__)   || 
                   |_|_|_|_|_|_|__|            ||   (__D     ||     C__)   ||
                  A@\|_|_|_|_|_|/@@Aa          ||   (__D     ||     C__)   ||
               aaA@@@@@@@@@@@@@@@@@@@aaaA      ||   (__D     ||     C__)   ||
              A@@@@@@@@@@@DWB@@@@@@@@@@@@A     ||     ||     ||     ||  dwb||
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  ================================         
""", """
    There will be 3 tests you need to take. 
    
    The first two tests you can either pass or fail one of them but not fail both.
    
    But the last one you must pass or you will fail immediately.
     
    In short, you need at least 2 out of 3 to get qualified in order to check your readiness, aptitude, and capability 
    before taking the serious job.
    """]

# [[question, number of choice]]
RIDDLES_QUESTIONS_LIST = [["""
    Mary's mother has 4 daughters: 1. Nana, 2. Nene, 3. Nini. What is the name of the fourth daughter?
        
        1) Nono
        
        2) Mary
        
        3) Nunu
        
        4) Mery
        
        5) Nino
        
""",  5], ["""
    You are participating in a race. You overtake the 3rd person. What position are you in?
       
        1) 1st
        
        2) 2nd
        
        3) 3rd
        
        4) 4th
    
    """, 4], ["""
     A farmer has 15 sheeps, and all but 9 die. How many sheep are left?
        
        1) 3
        
        2) 6
        
        3) 9
        
        4) 12
        
        5) 15
        """, 5]
                          ]
STAGE1_ANSWER = [2, 3, 4]

STAGE2_ANSWER = [1, 3, 4, 6]

STAGE3_ANSWER = [1]

KING_DRINK_RECIPE = ["Espresso", "Gingerbread syrup", "Milk", "Gingerbread spice"]

ALL_RECIPE = {1: "Espresso",
              2: "Red Wine",
              3: "Milk",
              4: "Gingerbread spice",
              5: "Cinnamon Stick",
              6: "Gingerbread syrup"
              }


# score 0 -> fail, 1 -> pass
player = {
    "player_name": "",
    "overall_current_score": []
}

# ****************************
#
# End Defining Key Variables
#
# ****************************

#########################################################################

# **************************
#
#  Start program controller
#
# ***************************


def clear_screen():
    """To clear the terminal screen"""

    if os.name == 'nt':
        return os.system('cls')
    else:
        return os.system('clear')


def ascii_art_gen_timer():
    """ this function is used to display timer in ascii art format before each game starts"""

    clear_screen()

    for each in TIMER:
        print("\n\n\n\t The game will start in ... ")
        print(each)
        time.sleep(1)
        clear_screen()


def set_player_name(name):
    """To set the player's name """

    player["player_name"] = name


def get_player_name():
    """To return the player's name """

    return player.get("player_name")


def get_player_score():
    """To get a list of player's score"""

    return player.get("overall_current_score")


def set_player_score(score):
    temp_list = get_player_score()
    temp_list.append(score)
    new_score = {"overall_current_score": temp_list}
    player.update(new_score)


# def get_player_info(info_type):
#     if info_type == "all":
#         return player
#     return player.get(info_type)


def get_element_amount_from_list(lst=list(), element=None):
    """To return number of element found in the lst list"""

    return lst.count(element)


def compare_answer(original, playerAnswer):
    """ this function is used to compare each element from two lists"""

    return original == playerAnswer


def result_check(original_ans, player_answer, stage_no):
    """To check result of each game's stage and return score value [0 or 1] and result"""

    feedback_score = 0
    question_ordinal = ""
    feedback = {0: "",
                1: ""}
    no_of_result = get_element_amount_from_list(list(map(compare_answer, original_ans, player_answer)), element=True)
    print("Number of correct: ", no_of_result)

    if stage_no == 1:
        if no_of_result >= 2:
            feedback_score = 1
        question_ordinal = "first"

    elif stage_no == 2:
        no_of_result = len(list(set(original_ans) & set(player_answer)))
        if no_of_result >= 3:
            feedback_score = 1
        question_ordinal = "second"

    else:
        if no_of_result == 1:
            feedback_score = 1

    good_result = "Congrat! you pass our "+question_ordinal+" test. You did a good job"
    bad_result = "Unfortunately, you failed the " + question_ordinal + " test. No worries, you still have " + str(
        3 - stage_no) + " tests left."
    if stage_no == 3:
        bad_result = "Unfortunately, you failed the" + question_ordinal + "test"

    feedback.update({0: bad_result, 1: good_result})

    return feedback_score, feedback.get(feedback_score)


# ***************************
#
#  End program controller
#
# ***************************


#########################################################################


# ***************************
#
#  Start game functions implementation
#
# ***************************


# ---- Game Stage 1 ----
def game_stage1():
    """Calling this function will run the flow of stage1 and return the result of this stage to its function caller"""

    input(f"""
       In stage 1 ...
    
    There are 3 questions for this stage and you need to pass at least 2 out of 3 to pass the first test.
    
    If you are ready, press Enter to start the game...
    """)

    answer_s1 = list()

    ascii_art_gen_timer()

    for each_question in RIDDLES_QUESTIONS_LIST:
        print(each_question[0])
        answer = input("> ")
        while not answer.isdigit() or int(answer) not in range(1, each_question[1]+1):
            print(f"""
                Invalid entry. Please try again.
                {each_question[0]}""")
            answer = input("> ")

        answer_s1.append(int(answer))
        clear_screen()

    # numberOfCorrectAnswer = get_element_amount_from_list(list(map(compare_answer, , answer_s1)),True)

    return result_check(STAGE1_ANSWER, answer_s1, 1)


# ************************************


# ---- Game Stage 2 ----
def game_stage2():
    """Calling this function will run the flow of stage2 and return the result of this stage to its function caller"""

    print(f""" 
    
    In Stage 2 ...
    
        The king prefer drinking coffee and he loves a good memorable person because such person can respond quickly.
         
        So we would like to test your ability to memorize the recipe of one coffee.
        
    """)

    input("Press Enter to continue...")
    clear_screen()

    print(f"""
    cont'd...
                                {COFFEE_ASCII_ART}
    
        One of his favorite coffee is called 'Christmas Latte', which include mainly 4 ingredients
                
        You will be given a 2-second look of the Christmas Latte's recipes. 
        
        By putting correct 3 out of 4 ingredients will therefore result you to pass this test.
        """)

    input("If you are ready, press Enter to start looking the main 4 recipes...")

    # an empty list to save each player's answer for comparing with expected value
    answer_s2 = list()

    # start counting the time 3..2..1..start
    ascii_art_gen_timer()

    # -- display all recipe for the King's favorite drink --
    print()
    for each in KING_DRINK_RECIPE:
        print("\t" + each + "\n")

    print("""   Espresso", "Gingerbread syrup", "Milk", "Gingerbread spice
                __________________   __________________
            .-/|                  \ /                  |\-.
            ||||                   |                   ||||
            ||||    Espresso       | Gingerbread spice ||||
            ||||                                       ||||
            ||||                   |                   ||||
            |||| Gingerbread syrup |        Milk       ||||
            ||||                   |                   ||||
            ||||                   |                   ||||
            ||||                   |                   ||||
            ||||                   |                   ||||
            ||||                   |                   ||||
            ||||__________________ | __________________||||
            ||/===================\|/===================\||
            `--------------------~___~-------------------''
""")

    # count 2 sec to let player memorize and clear the screen to start playing game
    time.sleep(2)
    clear_screen()

    print(f"""
        How was it?  Can you remember which the main ingredient for the coffee are?
        
            ** select the number one by one ** 
        """)



    # creating counter to prompt user to select choices 4 times
    counter = 0

    # a copy of ALL_RECIPE to show remaining available choices
    temp_all_recipe = ALL_RECIPE

    # to display a dict of selected recipe to remind the player
    temp_selected_recipe = {}  #

    while counter < 4:  # start counting
        clear_screen()
        for key, value in temp_all_recipe.items():
            # print("\t",key ,") "+value + "\n")
            print(f"""
                {key}) {value}""")

        print("\n\n\tYour selected recipe "+str(list(temp_selected_recipe.values()))+"\n")
        answer = input("> ")

        # check user's input if they are digit, in between 1-6 and not exist in the previously selected list.
        while not answer.isdigit() or int(answer) not in range(1, 7) or int(answer) in answer_s2:
            print("Invalid entry. Please try again.\n")
            answer = input("> ")

        # save answer and make a copy of selected item and delete the selected for next show
        int_answer = int(answer)
        answer_s2.append(int_answer)
        answer_s2.sort()
        counter += 1
        temp_selected_recipe[int_answer] = ALL_RECIPE.get(int_answer)
        del temp_all_recipe[int_answer]

    clear_screen()

    print("\n\n\tYour selected recipe " + str(list(temp_selected_recipe.values())) + "\n")

    # if numbers of failure equal to 2, means player failed 2 out of 3 -> end of game
    return result_check(STAGE2_ANSWER, answer_s2, 2)


# ---- Game Stage 3 ----
def game_stage3():
    """Calling this function will run the flow of stage3 and return the result of this stage to its function caller"""

    print(f"""
    In this last stage...
        
        We will test how sacrifice or trustworthy you are for the King.
        
        You will be in 3 scenarios where the Palace is invaded by a group of criminal gangs
        
        How would you respond to each scenario
        
        """)

    input("If you are ready, let's get the last stage done ")

    ascii_art_gen_timer()

    answer_s3 = list()

    print(f"""{ARCHER_ASCII_ART}
    
    
        You're seeing that the king is about to get assassinated by an assassin
        
        Do you think what is the best way according to the given choices?
        
            1. Help the King to survive
            2. Shout loud
            3. Run away
            4. Keep looking til assassination
            5. Help the assassin to kill the King
            
            """)
    answer = input("> ")
    while not answer.isdigit() or int(answer) not in range(1, 4):
        print(f"""
            Invalid entry. Please try again.
            """)
        answer = input("> ")

    answer_s3.append(int(answer))

    return result_check(STAGE3_ANSWER, answer_s3, 3)


# ---- Game fail ----
def game_fail():
    """To print that you are failed from the game"""
    print(f""" 
        Unluckily, you failed our test...

            ... Hope to see you in the Alcatraz... :D

     """)


def is_player_ready(question, answer_type):
    """To check if user is ready to continue or not
    Return True if user's input is in our scope (answer_type)
    Return False if user's input is out of scope
    """
    answer = str(input(question))
    return True if answer.lower() in answer_type else False


def start_story():
    """To run the storyline from the """
    for story in INTRO:
        clear_screen()
        print(f"\n\tWelcome ... {get_player_name()}\n")
        time.sleep(1)
        print(story)
        input("\nPress Enter to continue...\n")


def game_intro():
    """To show intro of the game with prompting user to enter user's name"""

    text = "Welcome to Python World\n"
    for each_char in text:
        print(each_char, end="")
        sys.stdout.flush()
        time.sleep(0.3)

    for i in range(3):
        print(". ", end="")
        sys.stdout.flush()
        time.sleep(0.3)

    print("\n\n\tExcuse me, what's your name...")
    player_name = str(input("I'm: "))

    while not player_name.isalpha():
        print("\n\n\tExcuse me, what's your name...")
        player_name = str(input("I'm: "))

    # set player's name to the player variable
    clear_screen()

    set_player_name(player_name)

    start_story()

    player_ready = is_player_ready(question=" Type 'y' or 'yes' if you are ready: ", answer_type=['y', 'yes'])

    while not player_ready:
        # print("Well, type 'y' when you're ready\n")
        player_ready = is_player_ready(question="Well, type 'y' or 'yes' when you're ready(y/n): ", answer_type=["y", "yes"])

    print("\nGreat, now let's get started...\n")


# check if player failed the test or not by checking their current number of failure
def is_player_failed():
    """Check if player's score if below our game's benchmark"""

    score_list = get_player_score()
    if get_element_amount_from_list(score_list, 0) == 2:
        return True
    return False


def game_start():
    """To start running to game's flow from intro->stage1->stage2->stage3->end"""

    game_intro()
    input("\nPress Enter to start the game")
    clear_screen()

    # store each games' function inside a list to iterate like a controller
    stage_list = [game_stage1, game_stage2, game_stage3]

    # game controller
    for each_game_stage in stage_list:
        score, result = each_game_stage()

        set_player_score(score)

        # check each stage if they really fail the test or not (2 fails out of 3)
        if is_player_failed():
            game_fail()
            break
        print(result)

    return

# ***************************
#
#  End game functions implementation
#
# ***************************


# main function
def main():

    while True:

        clear_screen()

        game_start()

        play_again = is_player_ready("\n\t Type 'y' or 'yes' if play again, else exit ", ["y", "yes", 'Y'])

        if play_again:
            continue
        else:
            sys.exit(0)


if __name__ == '__main__':
    main()
