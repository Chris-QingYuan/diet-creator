import pandas as pd


class Ingredient:
    __name = ""
    __standard_portion = 0
    __unit = ""
    __calories = 0
    __total_fat = 0
    __sat_fat = 0
    __carb = 0
    __fibre = 0
    __protein = 0
    __morning = 0
    __meal = 0
    __snack = 0
    __category = 0

    def __init__(self, dataframe_record):
        self.__name = dataframe_record.name
        self.__standard_portion = dataframe_record.standard_portion
        self.__unit = dataframe_record.unit
        self.__calories = dataframe_record.calories
        self.__total_fat = dataframe_record.total_fat
        self.__sat_fat = dataframe_record.sat_fat
        self.__carb = dataframe_record.carb
        self.__fibre = dataframe_record.fibre
        self.__protein = dataframe_record.protein
        self.__morning = dataframe_record.morning
        self.__meal = dataframe_record.meal
        self.__snack = dataframe_record.snack
        self.__category = dataframe_record.category

    def get_portion_and_nutrient(self):
        return self.__standard_portion, self.__unit, self.__carb, self.__protein, self.__total_fat

    def get_name(self):
        return self.__name

    def get_standard_portion(self):
        return self.__standard_portion

    def get_unit(self):
        return self.__unit

    def get_calories(self):
        return self.__calories

    def get_total_fat(self):
        return self.__total_fat

    def get_sat_fat(self):
        return self.__sat_fat

    def get_carb(self):
        return self.__carb

    def get_fibre(self):
        return self.__fibre

    def get_protein(self):
        return self.__protein

    def get_morning(self):
        return self.__morning

    def get_meal(self):
        return self.__meal

    def get_snack(self):
        return self.__snack

    def get_category(self):
        return self.__category
