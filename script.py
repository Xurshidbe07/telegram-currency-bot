
son = int(input("sonni kiriting: "))

def karajadval(son):
   while True:
      if son == 0:
         break
      if son >= 10:
         son = int(input("10 dan kichik bo'lgan sonni kiriting: "))
         continue

      for i in range(1, 10):
         print(f"{son} * {i} = {son * i}")

      son = int(input("sonni kiriting "))

karajadval(son)

