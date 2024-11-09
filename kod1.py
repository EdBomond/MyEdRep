from typing import Tuple
import pandas as pd
import matplotlib as plt
import math
from math import log
import time
from colorama import init, Fore

# Кожухотрубчатый холодильник

# Параметры сред
# Вода - в межтрубное пространство
# Бензол - в трубное пространство

print("Программа для расчёта ТО для воды в межтрубном пространстве и бензола в трубном")

# Данные по воде

t_mid_water_list = (10, 20, 30, 40, 50, 60, 70, 80, 90, 100) # град Цельсия Средняя температура воды
water_therm_conductivity_list = (0.575, 0.599, 0.618, 0.634, 0.648, 0.659, 0.668, 0.675, 0.68, 0.683) # Вт/м^2*К Теплопроводность
water_heat_capacity_list = (4190, 4190, 4180, 4180, 4180, 4180, 4190, 4190, 4190, 4230) # Дж/(кг×К) Темплоёмкость
water_viscous_list = (0.00131, 0.000804, 0.000657, 0.000549, 0.000470, 0.000406, 0.000355, 0.000355, 0.000315, 0.000282) # Па·с Вязкость

# Данные по бензолу

t_mid_benz_list = (10, 20, 30, 40, 50, 60, 70, 80, 90, 100) # град Цельсия
benz_therm_conductivity_list = (0.150, 0.145, 0.143, 0.140, 0.137, 0.133, 0.130, 0.127, 0.124, 0.121) # Вт/м^2*К
benz_heat_capacity_list = (1697, 1718, 1742, 1770, 1801, 1834, 1869, 1905, 1943, 1982) #Дж/(кг×К)
benz_viscous_list = (0.000755, 0.000649, 0.000559, 0.000489, 0.000434, 0.000389, 0.000347, 0.000318, 0.000286, 0.000261) # Па·с

# Константы
K_approximate = 195 # Приблизительный коэффициент теплопередачи от бензола к воде Вт/(м×К)
Re_approx = 10000 # Условное значение числа Рейнольдса
term_conductivity_dirty_pipe_outside = 1/4350 # Теплопроводность загрязнений стенок труб с внутренней стороны
term_conductivity_dirty_pipe_inside = 1/5800 # Теплопроводность загрязнений стенок труб с внешней стороны
const_term_conductivity_steelPipe = 46.5 # Rоэффициент теплопроводности стенки из стали, Вт/(м ×К)

t_start_water = float(input('Введите начальную температуру теплоносителя в межтрубном пространстве (Нагреваемый) в град. Цельсия: ') or "20")  # Начальная температура воды
t_fin_water = float(input('Введите конечную температуру теплоносителя в межтрубном пространстве (Нагреваемый) в град. Цельсия: ') or "38") # Конечная температура воды
t_start_benz = float(input('Введите начальную температуру теплоносителя в трубном пространстве (Охлаждаемый)) в град. Цельсия: ') or "100") # Начальная температура бензола
t_fin_benz = float(input('Введите конечную температуру теплоносителя в трубном пространстве (Охлаждаемый) в град. Цельсия: ') or "25") # Конечная температура бензола
G_benz = float(input('Введите расход жидкости (бензола) в трубном пространстве, т/ч. Если расход неизвестен введите 0: ') or "27") # Т/ч # Расход бензола Т/ч
G_water = float(input('Введите расход жидкости (воды) в межтрубном пространстве, т/ч. Если расход неизвестен? введите 0: ') or "0") # Т/ч

# —----------------------------------
# Данные для отладки
# Данные для отладки
# Данные для отладки

# t_start_water = 20
# t_fin_water = 38
# t_start_benz = 100
# t_fin_benz = 25
# G_benz = 27
# —-----------------------------------

# Функции для нахождения значения параметров сред интерполяцией

def find_water(a, b_list):
 if b_list == water_viscous_list:
  for i, a in enumerate(t_mid_water_list[0:-1]):
   if a == a_list[i]:
    b = b_list[i]
    return b
 elif (a > a_list[i]) and (a < a_list[i + 1]):
  b = b_list[i] - ((b_list[i] - b_list[i + 1]) / (a_list[i + 1] - a_list[i])) * (a - a_list[i])
  return b
 else:
  for i, a in enumerate(t_mid_water_list[0:-1]):
   if a == a_list[i]:
    b = b_list[i]
    return b
   elif (a > a_list[i]) and (a < a_list[i + 1]):
    b = b_list[i] + ((b_list[i + 1] - b_list[i]) / (a_list[i + 1] - a_list[i])) * (a - a_list[i])
    return b

def find_benz(a_benz, b_list):
  if b_list == benz_viscous_list:
    for i, a_benz in enumerate(t_mid_water_list[0:-1]):
      if a_benz == a_list[i]:
       b_benz = b_list[i]
       return b_benz
  elif (a_benz > a_list[i]) and (a_benz < a_list[i + 1]):
    b_benz = b_list[i] - (((b_list[i] - b_list[i + 1]) / (a_list[i + 1] - a_list[i])) * (a_benz - a_list[i]))
    return b_benz
  else:
    for i, a_benz in enumerate(t_mid_benz_list[0:-1]):
      if a_benz == a_list[i]:
        b_benz = b_list[i]
        return b_benz
      elif (a_benz > a_list[i]) and (a_benz < a_list[i + 1]):
        b_benz = b_list[i] + ((b_list[i + 1] - b_list[i]) / (a_list[i + 1] - a_list[i])) * (a_benz - a_list[i])
        return b_benz

# Функция для расчёт и введения поправочного коэффициента на среднюю логарифмическую температуру
def find_eps():
 try:
  t_1_start = t_start_water
  t_1_end = t_fin_water

  t_2_start = t_start_benz
  t_2_end = t_fin_benz

  R = (t_1_start - t_1_end) / (t_2_end - t_2_start)
  P = (t_2_end - t_2_start) / (t_1_start - t_2_start)

  n = math.sqrt(R**2 + 1)

  sig = (R+1)/ (math.log(((1-P)/(1-R*P))))
  eps_t = (n/sig) / (math.log((2-P*(1+R-n))/(2-P*(1+R+n))))
 except ValueError:
  print("Расчёт и введение поправочного коэффициента не представляется возможным из-за отрицательного подлогарифмического значения")
  eps_t = 1.5
  return eps_t
 else:
  print("Поправочный коэффициент равен =", eps_t)
  return eps_t

# Функция расчёта парметров выбранного аппарата
def calc_TO(F, n_z, i_d, o_d, S, depth_pipe, benz_viscous, water_viscous, water_heat_capacity, water_therm_conductivity, benz_heat_capacity, benz_therm_conductivity, G_benz):
 # Значение Рейнольдса для трубного пространства
 Re_benz = round((4 * G_benz) / (3.14 * n_z * benz_viscous * i_d), 2)

 print(" Число Рейнольдса для трубного пространства =", Re_benz)
 # print(benz_viscous)

 # Прандтль для трубного пространства
 Pr_benz = round((benz_heat_capacity * benz_viscous) / benz_therm_conductivity, 2)
 print("Число Прандтля для трубного пространства =", Pr_benz)

 # Коэффициент теплоотдачи от жидкости внутри труб к стенке
 alfa_benz = round((benz_therm_conductivity * 0.023 * (Re_benz ** 0.8) * (Pr_benz ** 0.4)) / i_d, 2)
 print("Коэффициент теплоотдачи от жидкости внутри труб к стенке =", alfa_benz)

 # Значение Рейнольдса для межтрубного пространства
 Re_water = round((G_water * o_d) / (S * water_viscous), 2)
 print()
 print("Вязкость воды =", water_viscous, "Па·с")
 print("Значение Рейнольдса для межтрубного пространства =", Re_water)

 # Прандтль для межтрубного пространства
 Pr_water = round((water_heat_capacity * water_viscous) / water_therm_conductivity, 2)
 print("Прандтль для межтрубного пространства", Pr_water)

 # Коэффициент теплоотдачи от труб к жидкости в межтрубном пространстве (вода)
 alfa_water = round((water_therm_conductivity * 0.24 * (Re_water ** 0.6) * (Pr_water ** 0.36)) / i_d, 2)
 print("Коэффициент теплоотдачи от труб к жидкости в межтрубном пространстве (вода) =", alfa_water)

 # Суммарное термическое сопротивление
 sum_term_resist_steelPipe = round((depth_pipe / const_term_conductivity_steelPipe) + term_conductivity_dirty_pipe_inside + term_conductivity_dirty_pipe_outside,6)

 # Коэффициент теплопередачи
 K = round(1 / (1/alfa_water + sum_term_resist_steelPipe + 1/alfa_benz), 2)
 print()
 print("Коэффициент теплопередачи =", K)
 return K

 t_mid_water = (t_fin_water + t_start_water)/2 # Средняя температура воды в аппарате

 t_mid_benz = (t_fin_benz + t_start_benz)/2 # Средняя температура бензола в аппарате

 G_benz = (G_benz*1000)/3600 # Расход бензола Кг/с

 # Расчёт теплопроводности воды при средней температуре
 a = t_mid_water
 a_list = t_mid_water_list
 b_list = water_therm_conductivity_list
 water_therm_conductivity = round(find_water(a, b_list), 2)
 # print("Теплопроводность воды при Т(воды)",t_mid_water,"=", water_therm_conductivity)

 # Расчёт теплоёмкость воды при средней температуре
 b_list = water_heat_capacity_list
 water_heat_capacity = round(find_water(a, b_list), 2)
 # print("Теплоёмкость воды при Т(воды)",t_mid_water,"=", water_heat_capacity)

 # Расчёт вязкости воды при средней температуре
 b_list = water_viscous_list
 water_viscous = round(find_water(a, b_list), 5)
 # print("Вязкость воды при Т(воды)",t_mid_water,"=",water_viscous)

 # Расчёт теплопроводности бензола при средней температуе
 a_benz = t_mid_benz
 a_benz_list = t_mid_benz_list
 b_list = benz_therm_conductivity_list
 benz_therm_conductivity = round(find_benz(a_benz, b_list), 2)
 # print("Теплопроводность бензола при Т(бензола)",t_mid_benz,"=",benz_therm_conductivity)

 # Расчёт теплоёмкость бензола при средней температуре
 b_list = benz_heat_capacity_list
 benz_heat_capacity = round(find_benz(a_benz, b_list), 2)
 # print("Теплоёмкость бензола при Т(бензола)",t_mid_benz,"=",benz_heat_capacity)

 # Расчёт вязкости бензола при средней температуре
 b_list = benz_viscous_list
 benz_viscous = round(find_benz(a_benz, b_list), 5)
 # print(benz_viscous)

 # Расчёт тепловой нагрузки аппарата и расход воды

 Q = round(G_benz * benz_heat_capacity * (t_start_benz - t_fin_benz), 2)
G_water = Q / (water_heat_capacity * (t_fin_water - t_start_water))

# Расчёт среднелогарифмичиской разницы между температурами теплоносителей и приближённого значения температуры

T_mid_log = ((t_start_benz - t_start_water) - (t_fin_water-t_fin_benz))/log((t_start_benz - t_start_water)/(t_fin_water-t_fin_benz))
# Введение поправки
eps_t = find_eps()
# Ориентировочное значение необходимой площади теплообмена
if 0 < eps_t <= 1:
T_mid_log_eps = T_mid_log * eps_t
F_approximate = Q / (K_approximate * T_mid_log_eps)
else:
F_approximate = Q / (K_approximate * T_mid_log)
F_approximate = round(F_approximate, 2)
print()
print("Ориентировочное значение необходимой площади теплообмена = ", F_approximate)

# D = 800 мм, dн = 25 × 2 мм, z = 4, n/z=101 F = 95 м2
F = 95
i_d = 0.021 # м внутренний диаметр
o_d = 0.025 # м внешний диаметр
n_z = 101 # n/z
S = 0.07 # м2 площадь сечения потока в межтрубном пространстве, между перегородками, м2
depth_pipe = i_d - o_d #Толщина стенки трубы

K = calc_TO(F, n_z, i_d, o_d, S, depth_pipe, benz_viscous, water_viscous, water_heat_capacity, water_therm_conductivity, benz_heat_capacity, benz_therm_conductivity, G_benz)

# Необходима площадь теплообмена
if 0 < eps_t <= 1:
T_mid_log_eps = T_mid_log * eps_t
F_required = round(Q/(K * T_mid_log_eps), 2)
else:
F_required = round(Q/(K * T_mid_log), 2)
print()
print('Необходима площадь теплообмена для данного аппарата и данных параметров сред =', F_required,"м^2")
print()
F_stock = round(((F - F_required)/F)*100, 2) # "Запас площади теплообмена"

if 30 > F_stock >= 10:
print("Выбранный аппарат с номинальной площадью", F, "м^2 обеспечивает", F_stock, "% запаса площади теплообмена")
print("Данный аппаарат может быть использован")
else:
print("Выбранный аппарат с номинальной площадью", F, "м^2 обеспечивает", F_stock, "% запаса площади теплообмена")
print("Данный аппаарат не может быть использован")

# D = 600 мм, dн = 20 × 2 мм, z = 2, n/z = 185 , F = 93 м2
F = 93
i_d = 0.016 #мм
n_z = 101

print()
print()
print("Программа завершит работу сама через 10 секунд")
print(Fore.RED + 'Продукт принадлежит ЗАО "Valerich INC".')
print('Коммерческое распространение запрещено. Все права защищены (R)')
time.sleep(10)
exit()