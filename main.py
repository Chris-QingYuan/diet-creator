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

PROTEIN_POWDER_CHOICE = {0: "NO",
                         1: "PRE-WORKOUT ONLY",
                         2: "POST-WORKOUT ONLY",
                         3: "BOTH PRE- AND POST-WORKOUT"}

DAILY_FIBRE = 30
DAILY_PROTEIN_UPPER_L = 205
DAILY_PROTEIN_LOWER_L = 140
CARB_PERCENTAGE_UPPER_L = 60
PROTEIN_POWDER_SERVING = 30
POST_WORKOUT_HONEY = 25
HIGH_CARB_LINE = 2000
CUP_VOLUME = 300

# global vars
daily_calories = 0
diet_type = (0, 0, 0)
daily_carb = 0
daily_fat = 0
daily_protein = 0
available_ingredients = []
supported_protein_num = 0
supported_proteins = list(DATAFRAME[DATAFRAME.category == 1].name)
protein_powder_choice = -1
juice_needed = -1
carb_per_meal = 0
protein_per_meal = 0
fat_pre_meal = 0

breakfast_menu = {}
meal_menu = {}
breakfast_carb = 0
breakfast_protein = 0
breakfast_fat = 0
meal_carb = 0
meal_protein = 0
meal_fat = 0

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


def main():
    """
    main function
    """
    # collect user inputs
    collect_req()

    # create meal plans
    create_meals()

    # output to a excel file
    meal_to_file()

    # test
    print(available_ingredients)


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

    # check if there is any special requirements, e.g. protein powder, juice or snack
    collect_special_req()

    # mark the completion of info collecting phase
    print("INFORMATION COLLECTION: \nOK!")


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

    global diet_type, daily_carb, daily_protein, daily_fat
    # display diet type
    display_diet_type()

    # get user input of calories breakdown or diet type choice and validate
    validate_cpf_percentage = collect_diet_type_input()

    # calculate the breakdowns and adjust, then assign to global vars
    diet_type = calculate_adjust_diet_type(validate_cpf_percentage)
    (daily_carb, daily_protein, daily_fat) = diet_type


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

    if (not sum(cpf_input_num_tuple) == 100) or cpf_input_num_tuple[0] > CARB_PERCENTAGE_UPPER_L:
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
    return tuple(map(lambda x: x / 100 * daily_calories, validate_cpf_percentage))


def adjust_diet_breakdown(cpf_values):
    """
    check if the volumes of the three nutrients are in bound, if not, adjust them
    :param cpf_values:
    :return:
    """
    if cpf_values[1] < DAILY_PROTEIN_LOWER_L * 4:
        return adjust_too_low_protein(cpf_values)
    elif cpf_values[1] > DAILY_PROTEIN_UPPER_L * 4:
        return adjust_too_high_protein(cpf_values)
    else:
        return cpf_values


def adjust_too_low_protein(cpf_values):
    adjusted_cpf_values = [0, 0, 0]
    adjusted_cpf_values[1] = DAILY_PROTEIN_LOWER_L * 4
    adjusted_cpf_values[0] = cpf_values[0] * (
            1 - (DAILY_PROTEIN_LOWER_L * 4 - cpf_values[1]) / (cpf_values[0] + cpf_values[2]))
    adjusted_cpf_values[2] = cpf_values[2] * (
            1 - (DAILY_PROTEIN_LOWER_L * 4 - cpf_values[1]) / (cpf_values[0] + cpf_values[2]))
    return tuple(adjusted_cpf_values)


def adjust_too_high_protein(cpf_values):
    adjusted_cpf_values = [0, 0, 0]
    adjusted_cpf_values[1] = DAILY_PROTEIN_UPPER_L * 4
    adjusted_cpf_values[0] = cpf_values[0] * (
            1 + (cpf_values[1] - DAILY_PROTEIN_UPPER_L * 4) / (cpf_values[0] + cpf_values[2]))
    adjusted_cpf_values[2] = cpf_values[2] * (
            1 + (cpf_values[1] - DAILY_PROTEIN_UPPER_L * 4) / (cpf_values[0] + cpf_values[2]))
    if adjusted_cpf_values[0] / daily_calories > (CARB_PERCENTAGE_UPPER_L / 100):
        adjusted_cpf_values[2] += adjusted_cpf_values[0] - daily_calories * CARB_PERCENTAGE_UPPER_L / 100
        adjusted_cpf_values[0] = daily_calories * CARB_PERCENTAGE_UPPER_L / 100
    return tuple(adjusted_cpf_values)


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


def collect_special_req():
    """
    check if there is any special requirements, e.g. protein powder, juice or snack
    :return:
    """
    # protein powder
    global protein_powder_choice
    protein_powder_choice = collect_protein_powder_req()

    # juice
    global juice_needed
    juice_needed = collect_juice_req()

    # snack
    #


def collect_protein_powder_req():
    print("please choose the volume of protein powder you want")
    for k, v in PROTEIN_POWDER_CHOICE.items():
        print(str(k) + "\t" + v)
    protein_req = input()
    try:
        protein_req_int = int(protein_req)
    except ValueError:
        protein_req_int = collect_protein_powder_req()

    if protein_req_int < 0 or protein_req_int >= len(PROTEIN_POWDER_CHOICE):
        protein_req_int = collect_protein_powder_req()

    return protein_req_int


def collect_juice_req():
    # if the calories from carbohydrate per day is too high, sak the user if they want to add juice into their meals
    if daily_carb > HIGH_CARB_LINE:
        juice_req = input(
            "the calories come from carbs is relatively high, which is " + str(
                daily_carb) + "[kCal], would you like to add a cup of juice to each of your meals?" +
            "\nNO: 0\nYES: any key slse")
        try:
            if int(juice_req) == 0:
                return 0
        except ValueError:
            return 1
    return 1


def create_meals():
    """
    calculate the different ingredients needed to form breakfast and meals menu
    """
    # calculate nutrition per meal
    calculate_nutrient_per_meal()

    # create breakfast menu
    create_breakfast()

    # create meal menu
    create_lunch_and_supper()


def calculate_nutrient_per_meal():
    # calculate nutrient from protein powder
    protein_powder_nutrient = calculate_protein_powder_nutrient()

    # calculate nutrient per meal after subtracting protein powder's


def calculate_protein_powder_nutrient():
    protein_powder_data = DATAFRAME[DATAFRAME.name == "protein powder"]
    (p_portuion, p_unit, p_carb, p_protein, p_fat) = (
        protein_powder_data.standard_portion, protein_powder_data.unit, protein_powder_data.carb,
        protein_powder_data.protein, protein_powder_data.protein.total_fat)

    # TODO


def init_nutrient_for_meals(protein_powder_nutrient):
    pass


def create_breakfast():
    pass


def create_lunch_and_supper():
    pass


def meal_to_file():
    """
    write the created meals to a xls file for later check and use
    """
    # TODO
    pass


# run the project

if __name__ == "__main__":
    main()
