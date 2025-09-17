# -*- coding: utf-8 -*-
"""
Created on Sun Apr 13 20:15:16 2025

@author: U S E R
"""

import random
import time
from collections import defaultdict

class Strategiya:
    def __init__(self):
        # Davlatlar va ularning kuch koeffitsientlari + bayroqlari
        self.davlatlar = {
            "AQSH": {
                "kuch": 100, 
                "egallovchi": None, 
                "ittifoqlar": [],
                "bayroq": "🇺🇸"
            },
            "Rossiya": {
                "kuch": 90, 
                "egallovchi": None, 
                "ittifoqlar": [],
                "bayroq": "🇷🇺"
            },
            "Fransiya": {
                "kuch": 70, 
                "egallovchi": None, 
                "ittifoqlar": [],
                "bayroq": "🇫🇷"
            },
            "Shimoliy Koreya": {
                "kuch": 60, 
                "egallovchi": None, 
                "ittifoqlar": [],
                "bayroq": "🇰🇵"
            },
            "O'zbekiston": {
                "kuch": 50, 
                "egallovchi": None, 
                "ittifoqlar": [],
                "bayroq": "🇺🇿"
            }
        }
        
        # Harakatlar va ularning stikerlari
        self.harakatlar = {
            "urush": "⚔️", 
            "ittifoq": "🤝", 
            "yordam": "🆘", 
            "savdo": "💹", 
            "neutralitet": "🏳️"
        }
        
        # Natija stikerlari
        self.natija_stikerlar = {
            "g'alaba": "🏆",
            "mag'lubiyat": "💥",
            "ittifoq_qabul": "✅",
            "ittifoq_rad": "❌",
            "ozod_qilindi": "🎉",
            "yordam_muvaffaqiyatsiz": "🚫",
            "savdo_muvaffaqiyatli": "📈",
            "kuch_oshdi": "💪"
        }
        
        # O'yinchilar va ularning balllari
        self.oyinchilar = {}
        self.ballar = defaultdict(int)
        
        # O'yin davomiyligi
        self.joriy_round = 0
        self.max_round = 5

    def o_yinchilarni_royxatga_olish(self):
        print("'Strategiya' o'yiniga xush kelibsiz! 🌍")
        print("Bu o'yinda 5 ta davlat uchun strategiya tanlaysiz.")
        print("Mavjud davlatlar:")
        
        for idx, davlat in enumerate(self.davlatlar, 1):
            bayroq = self.davlatlar[davlat]["bayroq"]
            print(f"{idx}. {bayroq} {davlat} (Kuch: {self.davlatlar[davlat]['kuch']})")
        
        for i in range(1, 6):
            while True:
                ism = input(f"{i}-o'yinchi ismingizni kiriting: ")
                if not ism.strip():
                    print("Ism bo'sh bo'lmasligi kerak! Qaytadan kiriting.")
                    continue
                
                while True:
                    try:
                        davlat_son = int(input(f"{ism}, qaysi davlatni tanlaysiz (1-5): "))
                        if 1 <= davlat_son <= 5:
                            davlat_nomi = list(self.davlatlar.keys())[davlat_son - 1]
                            if davlat_nomi in self.oyinchilar.values():
                               print(f"Bu davlat allaqachon tanlangan! Boshqa davlatni tanlang.")
                            else:
                                self.oyinchilar[ism] = davlat_nomi
                                bayroq = self.davlatlar[davlat_nomi]["bayroq"]
                                print(f"{ism} {bayroq} {davlat_nomi}ni tanladi!")
                                break
                        else:
                            print("Iltimos 1 dan 5 gacha raqam kiriting!")
                    except ValueError:
                        print("Iltimos raqam kiriting!")
                break

    def urush_natijasi(self, hujumchi_davlat, nishon_davlat):
        hujumchi_kuch = self.davlatlar[hujumchi_davlat]["kuch"]
        nishon_kuch = self.davlatlar[nishon_davlat]["kuch"]
        
        # Ittifoqlar kuchlarini qo'shish
        for ittifoqchi in self.davlatlar[hujumchi_davlat]["ittifoqlar"]:
            hujumchi_kuch += self.davlatlar[ittifoqchi]["kuch"] * 0.5
        
        for ittifoqchi in self.davlatlar[nishon_davlat]["ittifoqlar"]:
            nishon_kuch += self.davlatlar[ittifoqchi]["kuch"] * 0.5
        
        # Tasodifiy element (urushda omad ham rol o'ynaydi)
        hujumchi_kuch += random.randint(-10, 10)
        nishon_kuch += random.randint(-10, 10)
        
        # Natija
        if hujumchi_kuch > nishon_kuch:
            return True, hujumchi_kuch - nishon_kuch
        else:
            return False, nishon_kuch - hujumchi_kuch

    def yordam_natijasi(self, yordam_beruvchi, yordam_oluvchi):
        if self.davlatlar[yordam_oluvchi]["egallovchi"] is not None:
            egallovchi = self.davlatlar[yordam_oluvchi]["egallovchi"]
            yordam_beruvchi_kuch = self.davlatlar[yordam_beruvchi]["kuch"]
            egallovchi_kuch = self.davlatlar[egallovchi]["kuch"]
            
            # Ittifoqlar kuchlarini qo'shish
            for ittifoqchi in self.davlatlar[yordam_beruvchi]["ittifoqlar"]:
                yordam_beruvchi_kuch += self.davlatlar[ittifoqchi]["kuch"] * 0.3
            
            # Ozod qilish uchun yetarli kuch bormi?
            if yordam_beruvchi_kuch > egallovchi_kuch * 0.7:
                return True, yordam_beruvchi_kuch - egallovchi_kuch * 0.7
            else:
                return False, egallovchi_kuch * 0.7 - yordam_beruvchi_kuch
        else:
            return False, 0  # Davlat egallanmagan, yordam kerak emas

    def round_boshlash(self):
        self.joriy_round += 1
        print(f"\n---------- 🔄 {self.joriy_round}-ROUND 🔄 ----------")
        
        # Har bir o'yinchi harakatini tanlaydi
        for oyinchi, davlat in self.oyinchilar.items():
            bayroq = self.davlatlar[davlat]["bayroq"]
            print(f"\n{oyinchi} ({bayroq} {davlat}) harakatini tanlaydi:")
            
            # Harakatlar ro'yxatini ko'rsatish
            for idx, (harakat, stiker) in enumerate(self.harakatlar.items(), 1):
                print(f"{idx}. {stiker} {harakat}")
                
            # Harakatni tanlash
            while True:
                try:
                    harakat_son = int(input(f"Harakatni tanlang (1-{len(self.harakatlar)}): "))
                    if 1 <= harakat_son <= len(self.harakatlar):
                        tanlangan_harakat = list(self.harakatlar.keys())[harakat_son - 1]
                        tanlangan_stiker = self.harakatlar[tanlangan_harakat]
                        break
                    else:
                        print(f"Iltimos 1 dan {len(self.harakatlar)} gacha raqam kiriting!")
                except ValueError:
                    print("Iltimos raqam kiriting!")
            
            # Tanlangan harakatga qarab logikani bajarish
            if tanlangan_harakat == "urush":
                # Urush qilish uchun nishon davlatni tanlash
                mavjud_davlatlar = [d for d in self.davlatlar if d != davlat and self.davlatlar[d]["egallovchi"] != davlat]
                
                if not mavjud_davlatlar:
                    print("Urush qilish uchun boshqa davlat yo'q!")
                    continue
                
                print("Qaysi davlatga hujum qilmoqchisiz?")
                for idx, nishon in enumerate(mavjud_davlatlar, 1):
                    nishon_bayroq = self.davlatlar[nishon]["bayroq"]
                    print(f"{idx}. {nishon_bayroq} {nishon}")
                
                while True:
                    try:
                        nishon_son = int(input(f"Davlatni tanlang (1-{len(mavjud_davlatlar)}): "))
                        if 1 <= nishon_son <= len(mavjud_davlatlar):
                            nishon_davlat = mavjud_davlatlar[nishon_son - 1]
                            break
                        else:
                            print(f"Iltimos 1 dan {len(mavjud_davlatlar)} gacha raqam kiriting!")
                    except ValueError:
                        print("Iltimos raqam kiriting!")
                
                # Urush natijasini hisoblash
                nishon_bayroq = self.davlatlar[nishon_davlat]["bayroq"]
                print(f"\n{tanlangan_stiker} {bayroq} {davlat} {nishon_bayroq} {nishon_davlat}ga urush e'lon qildi!")
                yutdimi, farq = self.urush_natijasi(davlat, nishon_davlat)
                
                time.sleep(1)  # Kichik dramatik pauza
                
                if yutdimi:
                    print(f"{self.natija_stikerlar['g\'alaba']} {bayroq} {davlat} g'alaba qozondi va {nishon_bayroq} {nishon_davlat}ni egalladi! (Ustunlik: {farq:.1f})")
                    self.davlatlar[nishon_davlat]["egallovchi"] = davlat
                    self.ballar[oyinchi] += 2
                else:
                    print(f"{self.natija_stikerlar['mag\'lubiyat']} {bayroq} {davlat} mag'lubiyatga uchradi! {nishon_bayroq} {nishon_davlat} himoyalandi. (Ustunlik: {farq:.1f})")
                    self.ballar[oyinchi] -= 1
            
            elif tanlangan_harakat == "ittifoq":
                # Ittifoq qilish uchun davlatni tanlash
                mavjud_davlatlar = [d for d in self.davlatlar if d != davlat and d not in self.davlatlar[davlat]["ittifoqlar"]]
                
                if not mavjud_davlatlar:
                    print("Ittifoq tuzish uchun boshqa davlat yo'q!")
                    continue
                
                print("Qaysi davlat bilan ittifoq tuzmoqchisiz?")
                for idx, ittifoqchi in enumerate(mavjud_davlatlar, 1):
                    ittifoq_bayroq = self.davlatlar[ittifoqchi]["bayroq"]
                    print(f"{idx}. {ittifoq_bayroq} {ittifoqchi}")
                
                while True:
                    try:
                        ittifoq_son = int(input(f"Davlatni tanlang (1-{len(mavjud_davlatlar)}): "))
                        if 1 <= ittifoq_son <= len(mavjud_davlatlar):
                            ittifoq_davlat = mavjud_davlatlar[ittifoq_son - 1]
                            break
                        else:
                            print(f"Iltimos 1 dan {len(mavjud_davlatlar)} gacha raqam kiriting!")
                    except ValueError:
                        print("Iltimos raqam kiriting!")
                
                # Ittifoq taklifi
                ittifoq_bayroq = self.davlatlar[ittifoq_davlat]["bayroq"]
                print(f"\n{tanlangan_stiker} {bayroq} {davlat} {ittifoq_bayroq} {ittifoq_davlat}ga ittifoq taklif qildi!")
                
                # Ittifoq qabul qilinishini tekshirish (o'yinda bu avtomatik)
                qabul_ehtimoli = 0.7  # 70% qabul qilish ehtimoli
                if random.random() < qabul_ehtimoli:
                    print(f"{self.natija_stikerlar['ittifoq_qabul']} {ittifoq_bayroq} {ittifoq_davlat} taklifni qabul qildi!")
                    self.davlatlar[davlat]["ittifoqlar"].append(ittifoq_davlat)
                    self.davlatlar[ittifoq_davlat]["ittifoqlar"].append(davlat)
                    self.ballar[oyinchi] += 1
                else:
                    print(f"{self.natija_stikerlar['ittifoq_rad']} {ittifoq_bayroq} {ittifoq_davlat} taklifni rad etdi!")
            
            elif tanlangan_harakat == "yordam":
                # Yordam berish uchun davlatni tanlash
                egallangan_davlatlar = [d for d in self.davlatlar if self.davlatlar[d]["egallovchi"] is not None]
                
                if not egallangan_davlatlar:
                    print("Yordam berish uchun egallangan davlat yo'q!")
                    continue
                
                print("Qaysi davlatga yordam bermoqchisiz?")
                for idx, yordam_oluvchi in enumerate(egallangan_davlatlar, 1):
                    yordam_bayroq = self.davlatlar[yordam_oluvchi]["bayroq"]
                    egallovchi = self.davlatlar[yordam_oluvchi]["egallovchi"]
                    egallovchi_bayroq = self.davlatlar[egallovchi]["bayroq"]
                    print(f"{idx}. {yordam_bayroq} {yordam_oluvchi} (Egallovchi: {egallovchi_bayroq} {egallovchi})")
                
                while True:
                    try:
                        yordam_son = int(input(f"Davlatni tanlang (1-{len(egallangan_davlatlar)}): "))
                        if 1 <= yordam_son <= len(egallangan_davlatlar):
                            yordam_davlat = egallangan_davlatlar[yordam_son - 1]
                            break
                        else:
                            print(f"Iltimos 1 dan {len(egallangan_davlatlar)} gacha raqam kiriting!")
                    except ValueError:
                        print("Iltimos raqam kiriting!")
                
                # Yordam natijasini hisoblash
                yordam_bayroq = self.davlatlar[yordam_davlat]["bayroq"]
                print(f"\n{tanlangan_stiker} {bayroq} {davlat} {yordam_bayroq} {yordam_davlat}ga yordam bermoqchi!")
                yutdimi, farq = self.yordam_natijasi(davlat, yordam_davlat)
                
                time.sleep(1)  # Kichik dramatik pauza
                
                if yutdimi:
                    print(f"{self.natija_stikerlar['ozod_qilindi']} {bayroq} {davlat} muvaffaqiyatli yordam ko'rsatdi va {yordam_bayroq} {yordam_davlat} ozod bo'ldi! (Ustunlik: {farq:.1f})")
                    self.davlatlar[yordam_davlat]["egallovchi"] = None
                    self.ballar[oyinchi] += 3
                else:
                    print(f"{self.natija_stikerlar['yordam_muvaffaqiyatsiz']} {bayroq} {davlat} yordam berishda muvaffaqiyatsiz bo'ldi. (Ustunlik yetishmadi: {farq:.1f})")
                    self.ballar[oyinchi] -= 1
            
           
            elif tanlangan_harakat == "savdo":
                        davlat_kuch_oldin = self.davlatlar[davlat]["kuch"]
                        savdo_bonus = random.randint(5, 15)
                        self.davlatlar[davlat]["kuch"] += savdo_bonus
                        print(f"{self.natija_stikerlar['savdo_muvaffaqiyatli']} {bayroq} {davlat} savdodan foyda ko‘rdi! Kuch: {davlat_kuch_oldin} → {self.davlatlar[davlat]['kuch']}")
                        self.ballar[oyinchi] += 1
                
            if not mavjud_davlatlar:
                    print("Savdo qilish uchun boshqa davlat yo'q!")
                    continue
                
                    print("Qaysi davlat bilan savdo aloqalarini rivojlantirmoqchisiz?")
                    for idx, savdo_hamkor in enumerate(mavjud_davlatlar, 1):
                        savdo_bayroq = self.davlatlar[savdo_hamkor]["bayroq"]
                    print(f"{idx}. {savdo_bayroq} {savdo_hamkor}")
                
                    while True:
                        try:
                            savdo_son = int(input(f"Davlatni tanlang (1-{len(mavjud_davlatlar)}): "))
                            if 1 <= savdo_son <= len(mavjud_davlatlar):
                                savdo_davlat = mavjud_davlatlar[savdo_son - 1]
                                break
                            else:
                                print(f"Iltimos 1 dan {len(mavjud_davlatlar)} gacha raqam kiriting!")
                        except ValueError:
                                    print("Iltimos raqam kiriting!")
                
                # Savdo natijasi
                    savdo_bayroq = self.davlatlar[savdo_davlat]["bayroq"]
                    print(f"\n{tanlangan_stiker} {bayroq} {davlat} {savdo_bayroq} {savdo_davlat} bilan savdo aloqalarini rivojlantirmoqchi!")
                
                # Savdo muvaffaqiyati
                    savdo_foydasi = random.randint(5, 15)
                    self.davlatlar[davlat]["kuch"] += savdo_foydasi
                    print(f"{self.natija_stikerlar['savdo_muvaffaqiyatli']} Savdo muvaffaqiyatli! {bayroq} {davlat}ning kuchi {savdo_foydasi} punktga oshdi.")
                    print(f"{self.natija_stikerlar['kuch_oshdi']} {bayroq} {davlat}ning yangi kuch ko'rsatkichi: {self.davlatlar[davlat]['kuch']}")
                    self.ballar[oyinchi] += 1
            
            elif tanlangan_harakat == "neutralitet":
                print(f"\n{tanlangan_stiker} {bayroq} {davlat} bu raundda neytralitetni tanladi va o'z kuchini to'pladi.")
                kuch_oshishi = random.randint(3, 8)
                self.davlatlar[davlat]["kuch"] += kuch_oshishi
                print(f"{self.natija_stikerlar['kuch_oshdi']} {bayroq} {davlat}ning kuchi {kuch_oshishi} punktga oshdi.")
                print(f"{bayroq} {davlat}ning yangi kuch ko'rsatkichi: {self.davlatlar[davlat]['kuch']}")
                self.ballar[oyinchi] += 0.5  # Neytralitet kamroq ball beradi
        
        # Raund yakunida vaziyat to'g'risida ma'lumot
        print("\n----- 📊 RAUND YAKUNIDAGI VAZIYAT 📊 -----")
        for davlat, malumot in self.davlatlar.items():
            bayroq = malumot["bayroq"]
            
            if malumot["egallovchi"]:
                egallovchi_bayroq = self.davlatlar[malumot["egallovchi"]]["bayroq"]
                status = f"{egallovchi_bayroq} {malumot['egallovchi']} tomonidan EGALLANGAN"
            else:
                status = "🏳️ MUSTAQIL"
            
            if malumot["ittifoqlar"]:
                ittifoqlar_str = ", ".join([f"{self.davlatlar[ittifoq]['bayroq']} {ittifoq}" for ittifoq in malumot["ittifoqlar"]])
            else:
                ittifoqlar_str = "YO'Q"
            
            print(f"{bayroq} {davlat}: {status} | 💪 Kuch: {malumot['kuch']} | 🤝 Ittifoqlar: {ittifoqlar_str}")
        
        print("\n----- 🏅 JORIY BALLAR 🏅 -----")
        for oyinchi, ball in sorted(self.ballar.items(), key=lambda x: x[1], reverse=True):
            davlat = self.oyinchilar[oyinchi]
            bayroq = self.davlatlar[davlat]["bayroq"]
            print(f"{oyinchi} ({bayroq} {davlat}): {ball} ball")

    def o_yinni_boshlash(self):
        self.o_yinchilarni_royxatga_olish()
        
        print("\n🎮 O'yin boshlandi! Har bir o'yinchi navbat bilan harakatini tanlaydi.")
        
        while self.joriy_round < self.max_round:
            self.round_boshlash()
            
            # Keyingi raundga o'tishni so'rash
            input("\n⏭️ Keyingi raundga o'tish uchun ENTER tugmasini bosing...")
        
        # O'yin yakunida natijalarni e'lon qilish
        print("\n====== 🎯 O'YIN YAKUNLANDI 🎯 ======")
        print("🌎 YAKUNIY NATIJALAR:")
        
        for davlat, malumot in self.davlatlar.items():
            bayroq = malumot["bayroq"]
            
            if malumot["egallovchi"]:
                egallovchi_bayroq = self.davlatlar[malumot["egallovchi"]]["bayroq"]
                status = f"{egallovchi_bayroq} {malumot['egallovchi']} tomonidan EGALLANGAN"
            else:
                status = "🏳️ MUSTAQIL"
            
            if malumot["ittifoqlar"]:
                ittifoqlar_str = ", ".join([f"{self.davlatlar[ittifoq]['bayroq']} {ittifoq}" for ittifoq in malumot["ittifoqlar"]])
            else:
                ittifoqlar_str = "YO'Q"
            
            print(f"{bayroq} {davlat}: {status} | 💪 Kuch: {malumot['kuch']} | 🤝 Ittifoqlar: {ittifoqlar_str}")
        
        print("\n🏆 YAKUNIY BALLAR:")
        yakuniy_natijalar = sorted(self.ballar.items(), key=lambda x: x[1], reverse=True)
        
        for idx, (oyinchi, ball) in enumerate(yakuniy_natijalar, 1):
            davlat = self.oyinchilar[oyinchi]
            bayroq = self.davlatlar[davlat]["bayroq"]
            if idx == 1:
                print(f"🥇 {idx}. {oyinchi} ({bayroq} {davlat}): {ball} ball")
            elif idx == 2:
                print(f"🥈 {idx}. {oyinchi} ({bayroq} {davlat}): {ball} ball")
            elif idx == 3:
                print(f"🥉 {idx}. {oyinchi} ({bayroq} {davlat}): {ball} ball")
            else:
                print(f"{idx}. {oyinchi} ({bayroq} {davlat}): {ball} ball")
def yakuniy_natija(self):
    print("\n🏁 O'yin tugadi! Yakuniy ballar:")
    sorted_ballar = sorted(self.ballar.items(), key=lambda x: x[1], reverse=True)
    for ism, ball in sorted_ballar:
        davlat = self.oyinchilar[ism]
        bayroq = self.davlatlar[davlat]["bayroq"]
        print(f"{bayroq} {ism} ({davlat}): {ball} ball")
    
    g_olib = sorted_ballar[0]
    print(f"\n🏆 G‘olib: {g_olib[0]} ({self.oyinchilar[g_olib[0]]})! Tabriklaymiz! 🎊")        
      

# O'yinni ishga tushirish
if __name__ == "__main__":
    oyun = Strategiya()
    oyun.o_yinni_boshlash()