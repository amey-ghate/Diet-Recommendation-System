import streamlit as st
import pandas as pd
from random import uniform as rnd, choice
from streamlit_echarts import st_echarts

# Sample dataset of recipes
SAMPLE_RECIPES = {
    "breakfast": [
        {"Name": "Oatmeal", "Calories": 150, "FatContent": 3, "other_nutrients": "..."},
        {"Name": "Yogurt Parfait", "Calories": 200, "FatContent": 5, "other_nutrients": "..."}
    ],
    "lunch": [
        {"Name": "Grilled Chicken Salad", "Calories": 350, "FatContent": 10, "other_nutrients": "..."},
        {"Name": "Vegetable Stir Fry", "Calories": 300, "FatContent": 8, "other_nutrients": "..."}
    ],
    "dinner": [
        {"Name": "Spaghetti with Marinara Sauce", "Calories": 400, "FatContent": 12, "other_nutrients": "..."},
        {"Name": "Baked Salmon", "Calories": 450, "FatContent": 15, "other_nutrients": "..."}
    ],
}

st.set_page_config(page_title="Automatic Diet Recommendation", page_icon="💪", layout="wide")

nutritions_values = ['Calories', 'FatContent', 'SaturatedFatContent', 'CholesterolContent', 'SodiumContent', 'CarbohydrateContent', 'FiberContent', 'SugarContent', 'ProteinContent']

# Streamlit states initialization
if 'person' not in st.session_state:
    st.session_state.generated = False
    st.session_state.recommendations = None
    st.session_state.person = None
    st.session_state.weight_loss_option = None

class Person:
    def __init__(self, age, height, weight, gender, activity, meals_calories_perc, weight_loss):
        self.age = age
        self.height = height
        self.weight = weight
        self.gender = gender
        self.activity = activity
        self.meals_calories_perc = meals_calories_perc
        self.weight_loss = weight_loss

    def calculate_bmi(self):
        bmi = round(self.weight / ((self.height / 100) ** 2), 2)
        return bmi

    def display_result(self):
        bmi = self.calculate_bmi()
        bmi_string = f'{bmi} kg/m²'
        if bmi < 18.5:
            category = 'Underweight'
            color = 'Red'
        elif 18.5 <= bmi < 25:
            category = 'Normal'
            color = 'Green'
        elif 25 <= bmi < 30:
            category = 'Overweight'
            color = 'Yellow'
        else:
            category = 'Obesity'
            color = 'Red'
        return bmi_string, category, color

    def calculate_bmr(self):
        if self.gender == 'Male':
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            bmr = 10 * self.weight + 6.25 * self.height - 5 * self.age - 161
        return bmr

    def calories_calculator(self):
        activities = ['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 'Extra active (very active & physical job)']
        weights = [1.2, 1.375, 1.55, 1.725, 1.9]
        weight = weights[activities.index(self.activity)]
        maintain_calories = self.calculate_bmr() * weight
        return maintain_calories

    def generate_recommendations(self):
        # Simplified recommendation generator
        recommendations = []
        for meal in self.meals_calories_perc.keys():
            recommendations.append(choice(SAMPLE_RECIPES[meal]))
        return recommendations

class Display:
    def __init__(self):
        self.plans = ["Maintain weight", "Mild weight loss", "Weight loss", "Extreme weight loss"]
        self.weights = [1, 0.9, 0.8, 0.6]
        self.losses = ['-0 kg/week', '-0.25 kg/week', '-0.5 kg/week', '-1 kg/week']

    def display_bmi(self, person):
        st.header('BMI CALCULATOR')
        bmi_string, category, color = person.display_result()
        st.metric(label="Body Mass Index (BMI)", value=bmi_string)
        new_title = f'<p style="font-family:sans-serif; color:{color}; font-size: 25px;">{category}</p>'
        st.markdown(new_title, unsafe_allow_html=True)
        st.markdown(
            """
            Healthy BMI range: 18.5 kg/m² - 25 kg/m².
            """
        )

    def display_calories(self, person):
        st.header('CALORIES CALCULATOR')
        maintain_calories = person.calories_calculator()
        st.write('The results show a number of daily calorie estimates that can be used as a guideline for how many calories to consume each day to maintain, lose, or gain weight at a chosen rate.')
        for plan, weight, loss, col in zip(self.plans, self.weights, self.losses, st.columns(4)):
            with col:
                st.metric(label=plan, value=f'{round(maintain_calories * weight)} Calories/day', delta=loss, delta_color="inverse")

    def display_recommendation(self, person, recommendations):
        st.header('DIET RECOMMENDATOR')
        with st.spinner('Generating recommendations...'):
            meals = person.meals_calories_perc
            st.subheader('Recommended recipes:')
            for meal_name, column, recommendation in zip(meals, st.columns(len(meals)), recommendations):
                with column:
                    st.markdown(f'##### {meal_name.upper()}')
                    recipe_name = recommendation['Name']
                    expander = st.expander(recipe_name)
                    nutritions_df = pd.DataFrame({value: [recommendation[value]] for value in nutritions_values})

                    expander.dataframe(nutritions_df)
                    # ... Add other details of the recipe as needed

    def display_meal_choices(self,person,recommendations):    
        st.subheader('Choose your meal composition:')
        # Display meal compositions choices
        if len(recommendations)==3:
            breakfast_column,launch_column,dinner_column=st.columns(3)
            with breakfast_column:
                breakfast_choice=st.selectbox(f'Choose your breakfast:',[recipe['Name'] for recipe in recommendations[0]])
            with launch_column:
                launch_choice=st.selectbox(f'Choose your launch:',[recipe['Name'] for recipe in recommendations[1]])
            with dinner_column:
                dinner_choice=st.selectbox(f'Choose your dinner:',[recipe['Name'] for recipe in recommendations[2]])  
            choices=[breakfast_choice,launch_choice,dinner_choice]     
        elif len(recommendations)==4:
            breakfast_column,morning_snack,launch_column,dinner_column=st.columns(4)
            with breakfast_column:
                breakfast_choice=st.selectbox(f'Choose your breakfast:',[recipe['Name'] for recipe in recommendations[0]])
            with morning_snack:
                morning_snack=st.selectbox(f'Choose your morning_snack:',[recipe['Name'] for recipe in recommendations[1]])
            with launch_column:
                launch_choice=st.selectbox(f'Choose your launch:',[recipe['Name'] for recipe in recommendations[2]])
            with dinner_column:
                dinner_choice=st.selectbox(f'Choose your dinner:',[recipe['Name'] for recipe in recommendations[3]])
            choices=[breakfast_choice,morning_snack,launch_choice,dinner_choice]                
        else:
            breakfast_column,morning_snack,launch_column,afternoon_snack,dinner_column=st.columns(5)
            with breakfast_column:
                breakfast_choice=st.selectbox(f'Choose your breakfast:',[recipe['Name'] for recipe in recommendations[0]])
            with morning_snack:
                morning_snack=st.selectbox(f'Choose your morning_snack:',[recipe['Name'] for recipe in recommendations[1]])
            with launch_column:
                launch_choice=st.selectbox(f'Choose your launch:',[recipe['Name'] for recipe in recommendations[2]])
            with afternoon_snack:
                afternoon_snack=st.selectbox(f'Choose your afternoon:',[recipe['Name'] for recipe in recommendations[3]])
            with dinner_column:
                dinner_choice=st.selectbox(f'Choose your  dinner:',[recipe['Name'] for recipe in recommendations[4]])
            choices=[breakfast_choice,morning_snack,launch_choice,afternoon_snack,dinner_choice] 
        
        # Calculating the sum of nutritional values of the choosen recipes
        total_nutrition_values={nutrition_value:0 for nutrition_value in nutritions_values}
        for choice,meals_ in zip(choices,recommendations):
            for meal in meals_:
                if meal['Name']==choice:
                    for nutrition_value in nutritions_values:
                        total_nutrition_values[nutrition_value]+=meal[nutrition_value]
  
        total_calories_chose=total_nutrition_values['Calories']
        loss_calories_chose=round(person.calories_calculator()*person.weight_loss)

        # Display corresponding graphs
        st.markdown(f'<h5 style="text-align: center;font-family:sans-serif;">Total Calories in Recipes vs {st.session_state.weight_loss_option} Calories:</h5>', unsafe_allow_html=True)
        total_calories_graph_options = {
    "xAxis": {
        "type": "category",
        "data": ['Total Calories you chose', f"{st.session_state.weight_loss_option} Calories"],
    },
    "yAxis": {"type": "value"},
    "series": [
        {
            "data": [
                {"value":total_calories_chose, "itemStyle": {"color":["#33FF8D","#FF3333"][total_calories_chose>loss_calories_chose]}},
                {"value": loss_calories_chose, "itemStyle": {"color": "#3339FF"}},
            ],
            "type": "bar",
        }
    ],
}
        st_echarts(options=total_calories_graph_options,height="400px",)
        st.markdown(f'<h5 style="text-align: center;font-family:sans-serif;">Nutritional Values:</h5>', unsafe_allow_html=True)
        nutritions_graph_options = {
    "tooltip": {"trigger": "item"},
    "legend": {"top": "5%", "left": "center"},
    "series": [
        {
            "name": "Nutritional Values",
            "type": "pie",
            "radius": ["40%", "70%"],
            "avoidLabelOverlap": False,
            "itemStyle": {
                "borderRadius": 10,
                "borderColor": "#fff",
                "borderWidth": 2,
            },
            "label": {"show": False, "position": "center"},
            "emphasis": {
                "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
            },
            "labelLine": {"show": False},
            "data": [{"value":round(total_nutrition_values[total_nutrition_value]),"name":total_nutrition_value} for total_nutrition_value in total_nutrition_values],
        }
    ],
}       
        st_echarts(options=nutritions_graph_options, height="500px",)
        

display=Display()
title="<h1 style='text-align: center;'>Automatic Diet Recommendation</h1>"
st.markdown(title, unsafe_allow_html=True)
with st.form("recommendation_form"):
    st.write("Modify the values and click the Generate button to use")
    age = st.number_input('Age',min_value=2, max_value=120, step=1)
    height = st.number_input('Height(cm)',min_value=50, max_value=300, step=1)
    weight = st.number_input('Weight(kg)',min_value=10, max_value=300, step=1)
    gender = st.radio('Gender',('Male','Female'))
    activity = st.select_slider('Activity',options=['Little/no exercise', 'Light exercise', 'Moderate exercise (3-5 days/wk)', 'Very active (6-7 days/wk)', 
    'Extra active (very active & physical job)'])
    option = st.selectbox('Choose your weight loss plan:',display.plans)
    st.session_state.weight_loss_option=option
    weight_loss=display.weights[display.plans.index(option)]
    number_of_meals=st.slider('Meals per day',min_value=3,max_value=5,step=1,value=3)
    if number_of_meals==3:
        meals_calories_perc={'breakfast':0.35,'lunch':0.40,'dinner':0.25}
    elif number_of_meals==4:
        meals_calories_perc={'breakfast':0.30,'morning snack':0.05,'lunch':0.40,'dinner':0.25}
    else:
        meals_calories_perc={'breakfast':0.30,'morning snack':0.05,'lunch':0.40,'afternoon snack':0.05,'dinner':0.20}
    generated = st.form_submit_button("Generate")
if generated:
    st.session_state.generated=True
    person = Person(age,height,weight,gender,activity,meals_calories_perc,weight_loss)
    with st.container():
        display.display_bmi(person)
    with st.container():
        display.display_calories(person)
    with st.spinner('Generating recommendations...'):     
        recommendations=person.generate_recommendations()
        st.session_state.recommendations=recommendations
        st.session_state.person=person

if st.session_state.generated:
    with st.container():
        display.display_recommendation(st.session_state.person,st.session_state.recommendations)
        st.success('Recommendation Generated Successfully !', icon="✅")
    with st.container():
        display.display_meal_choices(st.session_state.person,st.session_state.recommendations)


