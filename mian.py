#constants
DIET_TYPE = {"HIGH CARB":(60,25,15),
             "MODERATE":(50,30,20),
             "ZONE DIET":(40,30,30),
             "LOW CARB":(25,45,30),
             "KETO":(10,15,75)}

#global vars





#main function
def main():
    #collect user inputs
    collect_req()

    #create meal plans
    create_meals()

    #output to a excel file
    meal_to_file()









#run the project