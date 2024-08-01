from taipy import Gui
from taipy.gui import Markdown
import pandas as pd


#cmd + shift + G to open usr/local/bin and find python interpreter path

def bmi_calculation(feet, inches, weight):
        # calculates BMI
        bmi = (weight / 2.205) / ((((feet * 12) + inches) * 0.0254)**2)
        return bmi

def bmr_calculation(feet, inches, weight, age, sex):
    #calculates bmr based on sex to later be passed onto the users activity level
    global bmr
    height = (feet * 30.48) + (inches * 2.54) #converts from inches to cm
    if sex == 'Male':
        bmr = (10 * (weight/2.205)) + (6.25 * height) - (5 * age) + 5
        return bmr
    else: 
        bmr = (10 * (weight/2.205)) + (6.25 * height) - (5 * age) + 161
        return bmr

def calories_calculation(feet, inches, weight, age, sex, activity):
    # Calculates the calories for maintaining weight based on activity level
    if activity == "Little or no exercise":
        return round(bmr_calculation(feet, inches, weight, age, sex) * 1.2)
    elif activity == "Exercise 1-3 times/week":
        return round(bmr_calculation(feet, inches, weight, age, sex) * 1.375)
    elif activity == "Exercise 3-5 times/week":
        return round(bmr_calculation(feet, inches, weight, age, sex) * 1.55)
    elif activity == "Exercise 6-7 times/week":
        return round(bmr_calculation(feet, inches, weight, age, sex) * 1.725)
    elif activity == "Very intense exercise or 2x training":
        return round(bmr_calculation(feet, inches, weight, age, sex) * 1.9)


# Preset values to define parameters for calculations
sex = 'Male'
cal = 0
weight = 160
feet = 5
inches = 9
age = 18
activity = 'Little or no exercise'


# Data set for rendering table
bmi_data = pd.DataFrame({
  "BMI": ['< 18.5', '18.5 - 24.9', '25 - 29.9', '> 30'],
  "Categories": ['Underweight', 'Healthy', 'Overweight', 'Obese']
})


# Establishes Welcome message and navbar
main = Markdown("""
<|layout|class_name=main|
#Welcome, **Jhoon**{: .name }!
####BMI = Body Mass Index
<|navbar|>
|>
""")

# Allows user to input body metrics
metrics_page = Markdown("""
<|layout|class_name=metrics
<|{sex}|toggle|lov=Male;Female|>
<|{age}|number|label=Age|>
<|{feet}|number|label=Feet|>
<|{inches}|number|label=Inches|>
<|{weight}|number|label=Weight (lbs)|>
<|{activity}|selector|label=Activity level|lov=Little or no exercise;Exercise 1-3 times/week;Exercise 3-5 times/week;Exercise 6-7 times/week;Very intense exercise or 2x training|dropdown|>
|>
""")

# Embedded bmi_calculation into markdown so that bmi updates as soon as change is detected
bmi_page = Markdown("""
<|layout|class_name=bmi|
**BMI:**{: .name } 
<|{bmi_calculation(feet, inches, weight)}|text|format=%.1f|>
<|{bmi_data}|table|>
|>
""")

calories_page = Markdown("""
<|layout|class_name=calories|
####Maintenance: 
<|{calories_calculation(feet, inches, weight, age, sex, activity)}|> cal/day
                        
####Mild weight loss (0.5 lbs/week):
<|{calories_calculation(feet, inches, weight, age, sex, activity)-250}|> cal/day

####Weight loss (1 lb/week):
<|{calories_calculation(feet, inches, weight, age, sex, activity)-500}|> cal/day
                        
####Extreme weight loss (2 lbs/week): 
<|{calories_calculation(feet, inches, weight, age, sex, activity)-1000}|> cal/day
|>
""")

# Different pages for navbar to navigate to
pages = {
    "/": main,
    "Metrics": metrics_page,
    "BMI": bmi_page,
    "Calories": calories_page
}

# Runs the pages on a local port
# Links external css file
Gui(pages=pages, css_file='main.css').run(use_reloader='true', port=5001)