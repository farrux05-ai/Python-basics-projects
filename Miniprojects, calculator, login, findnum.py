# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 06:45:27 2025

@author: U S E R
"""

#Lists
empty_lists = []
empty_lists.append('Jamol')
print('Jamol' in empty_lists)
empty_lists.insert(5, 'Jamol')
print(empty_lists)
empty_lists.remove('Jamol')
print(empty_lists)

#kalkulyator
print('Salom, men kalkulyatorman. Sizga biron sonni hisoblashda yordam beraman')
son1 = int(input('Birinchi sonni kiriting: '))
son2 = int(input('Ikkinchi sonni kiriting: '))
amal = input('Amalni tanlang(+, *, /, - ): ')
if amal == '+':
    print('Natija: ', son1 + son2)
elif amal == '*':
    print('Natija: ',son1 * son2)
elif amal == '/':
    if son1 != 0:
        print('Natija: ',son1 / son2)
    else:
        print("Nolga bo'lish mumkin meas")
    
elif amal =='-':
   print( 'Natija: ',son1 - son2)
else: 
    print('amal kiriting!')
    

#Login parol
users = {
    'Akrom': '455645',
    'ALi' : '123456',
    'Karim': '789456'
    }

print("login tizimiga xush kelibsiz")
#tekshiruv

for i in range(3):
    login = input("Loginni kiriting: ")
    parol  = input('Parolni kiriting: ')

    if login in users and users[login] == parol:
        print(f'Xush kelibsiz {login}')
        break

    else:
        print('Login yoki parol xato! Sizga kirishga ruxsat yoQ. qOLGAN URUNISHLAR SONI', 2-i)
else:
    print("3 marta xato kiritdingiz. Hisob bloklandi.")
    


    
#kompyuter son topish o'yini
import random
print("Men 1 dan 20 gacha tasodifiy son o'ylayman. Siz uni topishingiz kerak")
kompyuter_oylagan = random.randint(1,20)

for i in range(5):
      taxmin = int(input("Qanday son o'yaldim': "))
      if taxmin == kompyuter_oylagan:
          print('Topdingiz! ')
          break
      else:
          print('Topolmadingiz, sizda urunish qoldi', 5-i)
else:
    print('5 marttada ham topa olamdingiz', kompyuter_oylagan)
    
    
    
    
    
    
    
    
    
    
    