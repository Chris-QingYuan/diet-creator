# imports
import pandas as pd
import Ingredient as ingr
import utilities as util
import random
import numpy as np

# read in data from data.csv into a dataframe
DATAFRAME = pd.read_csv("data/data.csv")

# read in customized parameters
paras = util.text_to_dictionary(open("paras").read())

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

DAILY_FIBRE = int(paras['DAILY_FIBRE'])
DAILY_PROTEIN_UPPER_L = int(paras['DAILY_PROTEIN_UPPER_L'])
DAILY_PROTEIN_LOWER_L = int(paras['DAILY_PROTEIN_LOWER_L'])
CARB_PERCENTAGE_UPPER_L = int(paras['CARB_PERCENTAGE_UPPER_L'])
PROTEIN_POWDER_SERVING = int(paras['PROTEIN_POWDER_SERVING'])
STAPLE_FOOD_UPPER_L = int(paras['STAPLE_FOOD_UPPER_L'])
POST_WORKOUT_HONEY = int(paras['POST_WORKOUT_HONEY'])
HIGH_CARB_LINE = int(paras['HIGH_CARB_LINE'])
CUP_VOLUME = int(paras['CUP_VOLUME'])
SWEETENER_PER_MEAL_UPPER_L = int(paras['SWEETENER_PER_MEAL_UPPER_L'])

# global vars
daily_calories = 0
diet_type = (0, 0, 0)  # kCal,kCal,kCal
daily_carb = 0.0  # g
daily_protein = 0.0  # g
daily_fat = 0.0  # g
available_ingredients = []
supported_protein_names = list(DATAFRAME[DATAFRAME.category == 1].name)
supported_protein_num = len(supported_protein_names)
supported_staple_names = list(DATAFRAME[DATAFRAME.category == 2].name)
supported_staple_num = len(supported_staple_names)
supported_sweetener_names = list(DATAFRAME[DATAFRAME.category == 3].name)
supported_sweetener_num = len(supported_sweetener_names)
supported_nut_names = list(DATAFRAME[DATAFRAME.category == 4].name)
supported_nut_num = len(supported_nut_names)
supported_vegetable_names = list(DATAFRAME[DATAFRAME.category == 5].name)
supported_vegetable_num = len(supported_vegetable_names)
protein_powder_choice = -1
juice_needed = -1
carb_per_meal = 0  # g
protein_per_meal = 0  # g
fat_per_meal = 0  # g

breakfast_menu = {}
meal_menu = {}
breakfast_carb = 0  # g
breakfast_protein = 0  # g
breakfast_fat = 0  # g
meal_carb = 0  # g
meal_protein = 0  # g
meal_fat = 0  # g

"""
UTILITY FUNCTIONS
"""


def get_ingredient_by_name(ingre_name):
    return ingr.Ingredient(DATAFRAME[DATAFRAME.name == ingre_name])


'''
MAIN BODY
'''


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
    daily_calories = util.validate_input_type(input_cal, int)


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
    daily_carb = diet_type[0] / 4
    daily_protein = diet_type[1] / 4
    daily_fat = diet_type[2] / 9


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
    # print in rows with index
    for i in range(supported_protein_num):
        print(str(i) + "\t" + supported_protein_names[i])


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
    if daily_carb > HIGH_CARB_LINE / 4:
        juice_req = input(
            "the calories come from carbs is relatively high, which is " + str(
                daily_carb) + "[kCal], would you like to add a cup of juice to each of your meals?" +
            "\nNO: 0\nYES: any key else\n")
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


def subtract_orange_juice_nutrient_from_meals():
    if juice_needed == 1:
        orange_juice = get_ingredient_by_name('orange juice')
        factor = CUP_VOLUME / orange_juice.get_standard_portion()
        global carb_per_meal, fat_per_meal, protein_per_meal
        carb_per_meal -= orange_juice.get_carb() * factor
        protein_per_meal -= orange_juice.get_protein() * factor
        fat_per_meal -= orange_juice.get_total_fat() * factor


def calculate_nutrient_per_meal():
    # calculate nutrient from protein powder
    protein_powder_nutrient = calculate_protein_powder_nutrient()

    # calculate nutrient per meal after subtracting protein powder's
    subtract_protein_powder_nutrient_from_meals(protein_powder_nutrient)

    # calculate nutrient per meal after subtracting orange juice's
    subtract_orange_juice_nutrient_from_meals()


def calculate_protein_powder_nutrient():
    protein_powder = get_ingredient_by_name("protein powder")
    honey = get_ingredient_by_name("honey")

    pre_nutrient, post_nutrient = calculate_pre_and_post_workout_nutrient(protein_powder, honey)

    return calculate_protein_powder_nutrient_as_chosen(pre_nutrient, post_nutrient, protein_powder_choice)


def calculate_pre_and_post_workout_nutrient(protein_powder, honey):
    (p_portion, p_unit, p_carb, p_protein, p_fat) = protein_powder.get_portion_and_nutrient()
    (h_portion, h_unit, h_carb, h_protein, h_fat) = honey.get_portion_and_nutrient()

    pre_nutrient = list(map(float, [e * PROTEIN_POWDER_SERVING / p_portion for e in [p_carb, p_protein, p_fat]]))
    honey_nutrient = list(map(float, [e * POST_WORKOUT_HONEY / h_portion for e in [h_carb, h_protein, h_fat]]))
    post_nutrient = [sum(e) for e in zip(pre_nutrient, honey_nutrient)]
    return pre_nutrient, post_nutrient


def calculate_protein_powder_nutrient_as_chosen(pre_nutrient, post_nutrient, _protein_powder_choice):
    if _protein_powder_choice == 0:
        return [0, 0, 0]
    elif _protein_powder_choice == 1:
        return pre_nutrient
    elif _protein_powder_choice == 2:
        return post_nutrient
    elif _protein_powder_choice == 3:
        return [sum(x) for x in zip(pre_nutrient, post_nutrient)]

    return [0, 0, 0]


def subtract_protein_powder_nutrient_from_meals(protein_powder_nutrient):
    global carb_per_meal, fat_per_meal, protein_per_meal
    carb_per_meal = (daily_carb - protein_powder_nutrient[0]) / 3
    protein_per_meal = (daily_protein - protein_powder_nutrient[1]) / 3
    fat_per_meal = (daily_fat - protein_powder_nutrient[2]) / 3


def create_breakfast():
    pass


def pick_ingredients_for_meal():
    selected_protein_ingredient = get_ingredient_by_name(supported_protein_names[random.choice(available_ingredients)])
    selected_staple_ingredient = get_ingredient_by_name(random.choice(supported_staple_names))
    selected_nut_ingredient = get_ingredient_by_name(random.choice(supported_nut_names))
    selected_sweetener_ingredient = get_ingredient_by_name(random.choice(supported_sweetener_names))
    return [selected_protein_ingredient, selected_staple_ingredient, selected_nut_ingredient,
            selected_sweetener_ingredient]


def create_meal_wo_sweetener(ingredients_list):
    vector_a = np.array(
        [[ingredients_list[0].get_carb(), ingredients_list[1].get_carb(), ingredients_list[2].get_carb()],
         [ingredients_list[0].get_protein(), ingredients_list[1].get_protein(), ingredients_list[2].get_protein()],
         [ingredients_list[0].get_total_fat(), ingredients_list[1].get_total_fat(), ingredients_list[2].get_total_fat()]
         ])
    vector_b = np.array([carb_per_meal, protein_per_meal, fat_per_meal])
    return np.linalg.solve(vector_a, vector_b)


def create_meal_with_sweetener(ingredients_list, tentative_meal):
    sweetener_portion = (ingredients_list[1].get_standard_portion() * tentative_meal[1] - STAPLE_FOOD_UPPER_L) * 5 / 4
    if sweetener_portion > SWEETENER_PER_MEAL_UPPER_L:
        sweetener_portion = SWEETENER_PER_MEAL_UPPER_L
    sweetener_factor = sweetener_portion / ingredients_list[3].get_standard_portion()
    vector_a = np.array(
        [[ingredients_list[0].get_carb(), ingredients_list[1].get_carb(), ingredients_list[2].get_carb()],
         [ingredients_list[0].get_protein(), ingredients_list[1].get_protein(), ingredients_list[2].get_protein()],
         [ingredients_list[0].get_total_fat(), ingredients_list[1].get_total_fat(),
          ingredients_list[2].get_total_fat()]])
    vector_b = np.array([carb_per_meal - ingredients_list[3].get_carb() * sweetener_factor,
                         protein_per_meal - ingredients_list[3].get_protein() * sweetener_factor,
                         fat_per_meal - ingredients_list[3].get_total_fat() * sweetener_factor])
    return np.append(np.linalg.solve(vector_a, vector_b), sweetener_factor)


def adjust_meal_proportion(ingredients_list, tentative_meal):
    if ingredients_list[1].get_standard_portion() * tentative_meal[1] > STAPLE_FOOD_UPPER_L:
        return create_meal_with_sweetener(ingredients_list, tentative_meal)
    else:
        return tentative_meal


def ingredients_portion_to_menu(ingredients_list, adjusted_meal):
    menu = {}
    for i in range(len(adjusted_meal)):
        menu[str(ingredients_list[i].get_name())] = str(
            adjusted_meal[i] * ingredients_list[i].get_standard_portion()) + str(ingredients_list[i].get_unit())
    if juice_needed == 1:
        menu['orange juice'] = str(CUP_VOLUME) + "ml"
    return menu


def create_lunch_and_supper():
    ingredients_list = pick_ingredients_for_meal()
    tentative_meal = create_meal_wo_sweetener(ingredients_list)
    adjusted_meal = adjust_meal_proportion(ingredients_list, tentative_meal)
    global meal_menu
    meal_menu = ingredients_portion_to_menu(ingredients_list, adjusted_meal)


def meal_to_file():
    """
    write the created meals to a xls file for later check and use
    """
    # TODO
    pass


# run the project

if __name__ == "__main__":
    main()
