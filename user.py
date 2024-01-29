

class User(object):
    
    def __init__(self, name, last_name, weight, height, age, sex, activity_level, diet_goal):
        """_summary_

        Args:
            name (String): name of the user
            last_name (String): last name of the user
            weight (Integer): weight of the user in kg
            height (Integer): height of the user in cm
            age (Integer): age of the user in years
            sex (Integer): sex of the user (0 for male / 1 for female)
            activity_level (Integer): activity level of the user (0 for sedentary / 
                                                                    1 for lightly active / 
                                                                    2 for moderately active / 
                                                                    3 for very active / 
                                                                    4 for extra active)
            diet_goal (Integer): diet goal of the user (0 for lose weight (-20% BMR) / 
                                                        1 for lose weight slowly (-10% BMR) / 
                                                        2 for maintain weight (BMR) / 
                                                        3 for gain weight slowly (+10% BMR) / 
                                                        4 for gain weight (+20% BMR))
        """
        self.name = name
        self.last_name = last_name
        self.weight = weight 
        self.height = height
        self.age = age
        self.sex = sex
        self.activity_level = activity_level
        self.diet_goal = diet_goal
        self.bmr = self.compute_bmr()
        self.calorie_need = self.compute_calorie_need()
        self.calorie_goal = self.calorie_goal()

    def compute_bmr(self):
        if self.sex == 0:
            return int(66.47 + (13.75 * self.weight) + (5.003 * self.height) - (6.755 * self.age))
        else:
            return int(655.1 + (9.563 * self.weight) + (1.85 * self.height) - (4.676 * self.age))
        
    def compute_calorie_need(self):
        if self.activity_level == 0:
            return int(self.bmr * 1.2)
        
        elif self.activity_level == 1:
            return int(self.bmr * 1.375)
        
        elif self.activity_level == 2:
            return int(self.bmr * 1.55)
        
        elif self.activity_level == 3:
            return int(self.calorie_need * 0.8)
        
        elif self.diet_goal == 1:
            return int(self.calorie_need * 0.9)
        
        elif self.diet_goal == 3:
            return int(self.calorie_need * 1.1)
        
        elif self.diet_goal == 4:
            return int(self.calorie_need * 1.2)
        
        else:
            return int(self.calorie_need)
        

user = User("John", "Doe", 80, 180, 30, 1, 3, 1)
print(user.calorie_need)
print(user.calorie_goal)
