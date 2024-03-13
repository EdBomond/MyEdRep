message="0"
while 1:
  message=int(input("Введите число: "))
  print(message)
  print(message%2)
  if message%2 == 0:
      break
print("End program!")