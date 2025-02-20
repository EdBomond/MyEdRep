from datetime import date
import calendar


days_m=31,28,31,30,31,30,31,31,30,31,30,31
names_m=("январь","февраль","март","апрель","май","июнь","июль","август","сентябрь","октябрь","ноябрь","декабрь")



def print_month(month, year):
  id_m=names_m.index(month)
  wd=date(year,id_m+1,1).weekday()
  days=days_m[id_m]
  if calendar.isleap(year) and id_m == 1:
    days += 1
  print(wd," ",days," ", id_m)
  print(f"{month} {year}".center(20))
  print("Пн Вт Ср Чт Пт Сб Вс")
  print('   ' * wd, end='')
  
  for day in range(days):
   wd = (wd + 1) % 7
   #print("_",wd,"_")
   eow = " " if wd % 7 else "\n" 
   print(f"{day+1:2}", end=eow)
      
  print()
  print("в месяце ", names_m[id_m], days, " дней")

print_month("август", 2057)
