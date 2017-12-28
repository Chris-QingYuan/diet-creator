# constants
DIET_TYPE = {"HIGH CARB": (60, 25, 15),
             "MODERATE": (50, 30, 20),
             "ZONE DIET": (40, 30, 30),
             "LOW CARB": (25, 45, 30),
             "KETO": (10, 15, 75)}

DAILY_FIBRE = 30

# global vars
daily_calories = 0
diet_type = -1
daily_carb = 0
daily_fat = 0
daily_protein = 0
available_ingredients = []


'''
UTILITY FUNCTIONS
'''


def validate_input_type(input_val, expected_t):
    try:
        valid_val = expected_t(input_val)
    except ValueError:
        valid_val = validate_input_type(input("the type of the input value is not right, please try again:"), expected_t)
    return valid_val


'''
main function
'''


def __main__():
    # collect user inputs
    collect_req()

    # create meal plans
    create_meals()

    # output to a excel file
    meal_to_file()

    print()


'''
collect user requirements, including the daily calories intake ,diet type and the available ingredients
'''


def collect_req():
    # ask for the daily calories intake
    collect_daily_cal()

    # get the diet type to use
    collect_diet_type()

    # check the ingredients available right now
    collect_ingredients()


'''
ask the user for the desired daily calories intake value
'''


def collect_daily_cal():
    # get user input
    input_cal = input("please tell me how much calories you want to take per day: ")
    # validation
    global daily_calories
    daily_calories = validate_input_type(input_cal, int)


'''
ask the user for the desired diet type
'''


def collect_diet_type():
    # display diet type
    display_diet_type()

    # get and validate diet type
    global diet_type
    diet_type = get_validate_diet_type()




'''
display the supported diet types
'''


def display_diet_type():
    print("please choose one diet type to use:\n" + "\t"*6 + "CARB\t\tPROTEIN\t\tFAT")
    i = 0
    for key in DIET_TYPE.keys():
        print(str(i) + "\t" + key, end="")
        for v in DIET_TYPE[key]:
            print("\t"*3 + str(v), end="")
        print()
        i += 1


'''
get and validate diet type
'''


def get_validate_diet_type():
    selection = int(input("please enter a valid choice number: "))
    if selection < 0 or selection >= len(DIET_TYPE):
        selection = get_validate_diet_type()
    return selection


'''
ask the user for the ingredients available
'''


def collect_ingredients():
    pass


'''
calculate the different ingredients needed
'''


def create_meals():
    pass


'''
write the created meals to a xls file for later check and use
'''


def meal_to_file():
    pass


# run the project
# __main__()




'''
UNIT TESTS!
'''

