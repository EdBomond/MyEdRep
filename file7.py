#from file6 import m_pizza as mp
#mp("ing1")
#mp("ing2","ing3","ing4")

class Dog():
    def __init__(self, name, age):
        self.name=name
        self.age=age
        self.korm='Karmy'
    def sit(self):
        print(f"{self.name} is now sitting.")
    def roll_over(self):
        print(f"{self.name} rolled over!")
    def Describe(self):
        print(f"Мою собаку зовут {self.name}.")
        print(f"Его возраст {round(self.age,1)} лет.") 
        print(f"Корм {self.korm}.")    
        
class Dog_robot(Dog):
    def __init__(self, name, age, motor):
        super().__init__(name, age)
        self.korm='None'
        self.motor=motor  
    def Describe(self):
        print(f"Мою собаку зовут {self.name}.")
        print(f"Его возраст {round(self.age,1)} лет.") 
        print(f"Корм {self.korm}.")    
        print(f"Тип мотора {self.motor}.")  

dog_alex=Dog("Алекс", 5/6)
dog_alma=Dog("Альма", 10)
print(f"Мою собаку зовут {dog_alex.name}.")
print(f"Его возраст {round(dog_alex.age,1)} лет.")
dog_alex.sit()
dog_alma.roll_over()
dog_robot_as=Dog_robot("As1",1,'electrik')
print(f"{dog_robot_as.name}-{dog_robot_as.motor}-{dog_robot_as.age}")
dog_robot_as.Describe()

