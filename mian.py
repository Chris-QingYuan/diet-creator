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
DAILY_PROTEIN_UPPER_L = 205
DAILY_PROTEIN_LOWER_L = 140
CARB_PERCENTAGE_UPPER_L = 60

# global vars
daily_calories = 0
diet_type = (0, 0, 0)
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

    global diet_type
    # display diet type
    display_diet_type()

    # get user input of calories breakdown or diet type choice and validate
    validate_cpf_percentage = collect_diet_type_input()

    # calculate the breakdowns and adjust, then assign to global vars
    diet_type = calculate_adjust_diet_type(validate_cpf_percentage)


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


def collect_diet_type_input():
    """
    get and validate diet type input
    """
    diet_type_input = input(
        "please enter a valid choice number or three numbers that add up to 100, spilt in comma: \n")
    if "," in diet_type_input:
        return validate_customized_diet_type(diet_type_input)
    else:
        return validate_diet_type_selection(diet_type_input)


def validate_customized_diet_type(diet_type_input):
    """
    validate and parse user input if the user is intended to use customized diet breakdown
    :param diet_type_input:
    :return:
    """
    cpf_input_tuple = tuple(diet_type_input.split(","))
    try:
        cpf_input_num_tuple = tuple(map(float, cpf_input_tuple))
    except ValueError:
        cpf_input_num_tuple = collect_diet_type_input()

    if not sum(cpf_input_num_tuple) == 100:
        cpf_input_num_tuple = collect_diet_type_input()

    return cpf_input_num_tuple


def validate_diet_type_selection(diet_type_input):
    """
    validate and parse user input if the user is intended to use pre-defined diet breakdown
    :param diet_type_input:
    :return:
    """
    try:
        selection = int(diet_type_input)
        if selection < 0 or selection >= len(DIET_TYPE):
            return collect_diet_type_input()
        else:
            return list(DIET_TYPE.values())[selection]
    except ValueError:
        return collect_diet_type_input()


def calculate_adjust_diet_type(validate_cpf_percentage):
    """
    according to the diet breakdown calculate the values of different nutrition intake per day then adjust them
    :param validate_cpf_percentage:
    :return:
    """
    cpf_values = calculate_diet_breakdown(validate_cpf_percentage)

    adjusted_cpf_values = adjust_diet_breakdown(cpf_values)

    return adjusted_cpf_values


def calculate_diet_breakdown(validate_cpf_percentage):
    return tuple(map(lambda x: x/100*daily_calories, validate_cpf_percentage))


def adjust_diet_breakdown(cpf_values):
    pass


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
# __main__()

'''
UNIT TESTS!
'''
