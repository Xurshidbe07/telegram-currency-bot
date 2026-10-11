
def function(a, b, c):
    return a+b+c

a = int(input("Birinchi sonni kiriting: "))
b = int(input("Ikkinchi sonni kiriting: "))
c = int(input("Uchinchi sonni kiriting: "))


natija = function(a, b, c)
print("Natija: ", natija)

def number():
    a = int(input("Birinchi son: "))
    b = int(input("Ikkinchi son: "))

    if a > b:
        return a * a
    else:
        return b * b

natija = number()
print("Natija:", natija)

def yigindi(a, b):
   return a + b

natija = yigindi(5, 3)
print(natija)

def salom(ism):
    print(f"Salom, {ism}!")

salom("Ali")

def tekshir(son):
    if son > 0:
        print("Musbat son")
    else:
        print("Manfiy yoki nol")

tekshir(5)

def paroltekshir(parol):
    if parol == "12345":
        print("Kirishga ruxsat")
    else:
        print("Noto'g'ri parol")

paroltekshir("11111")

def jufttoq():
    son = int(input("Son kiriting: "))

    if son % 2 == 0:
        print("Juft son")
    else:
        print("Toq son")

jufttoq()

def kattason():
    a = int(input("Birinchi sonni kiriting: "))
    b = int(input("Ikkinchi sonni kiriting: "))

    if a > b:
        print("Katta son:", a)
    else:
        print("Katta son:", b)


kattason()