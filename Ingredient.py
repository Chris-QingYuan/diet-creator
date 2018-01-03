import pandas as pd


class Ingredient:
    __name: str = ""
    __standard_portion: float = 0.0
    __unit: str = ""
    __calories: float = 0.0
    __total_fat: float = 0.0
    __sat_fat: float = 0.0
    __carb: float = 0.0
    __fibre: float = 0.0
    __protein: float = 0.0
    __morning: int = 0
    __meal: int = 0
    __snack: int = 0
    __category: int = 0

    def __init__(self, dataframe_record):
        self.__name = str(dataframe_record.values[0][0])
        self.__standard_portion = float(dataframe_record.values[0][1])
        self.__unit = str(dataframe_record.values[0][2])
        self.__calories = float(dataframe_record.values[0][3])
        self.__total_fat = float(dataframe_record.values[0][4])
        self.__sat_fat = float(dataframe_record.values[0][5])
        self.__carb = float(dataframe_record.values[0][6])
        self.__fibre = float(dataframe_record.values[0][7])
        self.__protein = float(dataframe_record.values[0][8])
        self.__morning = int(dataframe_record.values[0][9])
        self.__meal = int(dataframe_record.values[0][10])
        self.__snack = int(dataframe_record.values[0][11])
        self.__category = int(dataframe_record.values[0][12])

    def get_portion_and_nutrient(self):
        return float(self.__standard_portion), str(self.__unit), float(self.__carb), float(self.__protein), float(
            self.__total_fat)

    def get_name(self):
        return self.__name

    def get_standard_portion(self):
        return float(self.__standard_portion)

    def get_unit(self):
        return str(self.__unit)

    def get_calories(self):
        return float(self.__calories)

    def get_total_fat(self):
        return float(self.__total_fat)

    def get_sat_fat(self):
        return float(self.__sat_fat)

    def get_carb(self):
        return float(self.__carb)

    def get_fibre(self):
        return float(self.__fibre)

    def get_protein(self):
        return float(self.__protein)

    def get_morning(self):
        return int(self.__morning)

    def get_meal(self):
        return int(self.__meal)

    def get_snack(self):
        return int(self.__snack)

    def get_category(self):
        return int(self.__category)
