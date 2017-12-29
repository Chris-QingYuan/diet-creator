# imports
import pandas as pd

# read in data from data.csv into a dataframe
DATAFRAME = pd.read_csv("data/data.csv")

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
supported_protein_num = 0
supported_proteins = list(DATAFRAME[DATAFRAME.category == 1].name)

'''
UTILITY FUNCTIONS
'''


def validate_input_type(input_val, expected_t):
    try:
        valid_val = expected_t(input_val)
    except ValueError:
        valid_val = validate_input_type(input("the type of the input value is not right, please try again:"),
                                        expected_t)
    return valid_val


def __main__():
    """
    main function
    """
    # collect user inputs
    collect_req()

    # create meal plans
    create_meals()

    # output to a excel file
    meal_to_file()

    print(DATAFRAME)


def collect_req():
    """
    collect user requirements, including the daily calories intake ,diet type and the available ingredients
    """
    # ask for the daily calories intake
    collect_daily_cal()

    # get the diet type to use
    collect_diet_type()

    # check the ingredients available right now
    collect_ingredients()


def collect_daily_cal():
    """
    ask the user for the desired daily calories intake value
    """
    # get user input
    input_cal = input("please tell me how much calories you want to take per day: ")
    # validation
    global daily_calories
    daily_calories = validate_input_type(input_cal, int)


def collect_diet_type():
    """
    ask the user for the desired diet type
    """
    # display diet type
    display_diet_type()

    # get and validate diet type
    global diet_type
    diet_type = get_validate_diet_type()


def display_diet_type():
    """
    display the supported diet types
    """
    print("please choose one diet type to use:\n" + "\t" * 6 + "CARB\t\tPROTEIN\t\tFAT")
    i = 0
    for key in DIET_TYPE.keys():
        print(str(i) + "\t" + key, end="")
        for v in DIET_TYPE[key]:
            print("\t" * 3 + str(v), end="")
        print()
        i += 1


def get_validate_diet_type():
    """
    get and validate diet type
    """
    selection = int(input("please enter a valid choice number: "))
    if selection < 0 or selection >= len(DIET_TYPE):
        selection = get_validate_diet_type()
    return selection


def collect_ingredients():
    """
    ask the user for the ingredients available,
    only check the proteins
    """
    # read the list of proteins from the DATAFRAME and display them
    display_supported_protein()

    # accept user input and parse into list, then append to available_ingredients
    global available_ingredients
    available_ingredients += list(set(get_validate_available_ingredient()))


def display_supported_protein():
    """
    read the list of proteins from the DATAFRAME and display them
    """
    # get the list of supported proteins

    global supported_protein_num
    supported_protein_num = len(supported_proteins)
    # print in rows with index
    for i in range(supported_protein_num):
        print(str(i) + "\t" + supported_proteins[i])


def get_validate_available_ingredient():
    """
    accept user input and parse into list, then append to available_ingredients
    :return:
    """
    # get user input, the index of the available proteins
    available_ingredients_index = input("please indicate the index of available proteins, separate with comma: ")
    # validate, if fail then recurse
    try:
        available_ingredients_list = list(map(int, available_ingredients_index.split(",")))
    except ValueError:
        available_ingredients_list = get_validate_available_ingredient()

    for v in available_ingredients_list:
        if v >= supported_protein_num:
            print("input number too large, out of bounce")
            available_ingredients_list = get_validate_available_ingredient()
    return available_ingredients_list

def create_meals():
    """
    calculate the different ingredients needed
    """
    pass


def meal_to_file():
    """
    write the created meals to a xls file for later check and use
    """
    pass


# run the project
__main__()


'''
UNIT TESTS!
'''
