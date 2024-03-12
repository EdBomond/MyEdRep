cars=['audi','bmw','lada','sangyong','fiat','seat','tatra','kamaz']
for car in sorted(cars[0:3]):
    if car=='bmw':
      print(car.upper())
    else: 
      print(car.title())	
if 'audi1' in cars:
    print('Да, это автомобиль')
else:
    print('Нет, это не автомобиль')
if 'audi1' in cars:
	print("Yes")
elif 'bmw' in cars:
    print("Bmw")
elif 'lada' in cars:
    print("lada")    
else:
    print("No")    	