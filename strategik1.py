# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 06:38:23 2025

@author: U S E R
"""

import random

class StrategikOyin:
    def __init__(self):
        self.davlatlar = {
            "AQSH": {"kuch": 100},
            "Rossiya": {"kuch": 95},
            "Xitoy": {"kuch": 90},
            "Yevropa Ittifoqi": {"kuch": 85},
            "Hindiston": {"kuch": 80}
        }

        self.ballar = {
            "O'yinchi 1": 0,
            "O'yinchi 2": 0,
            "O'yinchi 3": 0,
            "O'yinchi 4": 0,
            "O'yinchi 5": 0
        }

        self.davlatlar_royxati = list(self.davlatlar.keys())
        self.harakatlar = {
            "urush": "⚔️",
            "ittifoq": "🤝",
            "yordam": "🎁",
            "savdo": "💰",
            "neutralitet": "🕊️"
        }

        self.natija_stikerlar = {
            "urush_yutdi": "🏆",
            "urush_yutqazdi": "💥",
            "ittifoq_muvaffaqiyatli": "✅",
            "ittifoq_qarshi": "❌",
            "yordam_olindi": "🙏",
            "yordam_rad": "⛔️",
            "savdo_muvaffaqiyatli": "📈"
        }

    def strategiya_boshlash(self):
        for raund in range(5):
            print(f"\n🎯 {raund + 1}-RAUND BOSHLANDI 🎯\n")
            for i, davlat in enumerate(self.davlatlar_royxati):
                oyinchi = f"O'yinchi {i + 1}"
                print(f"\n{oyinchi} ({davlat}) navbati:")
                print("Harakatlar: urush, ittifoq, yordam, savdo, neutralitet")

                tanlangan_harakat = input("Harakat tanlang: ").lower()
                bayroq = self.harakatlar.get(tanlangan_harakat, "❓")

                if tanlangan_harakat == "urush":
                    nishon = self._tasodifiy_davlat(davlat)
                    if self.davlatlar[davlat]["kuch"] > self.davlatlar[nishon]["kuch"]:
                        self.davlatlar[davlat]["kuch"] += 10
                        self.davlatlar[nishon]["kuch"] -= 10
                        print(f"{self.natija_stikerlar['urush_yutdi']} {bayroq} {davlat} {nishon} ustidan g‘alaba qozondi!")
                        self.ballar[oyinchi] += 2
                    else:
                        self.davlatlar[davlat]["kuch"] -= 5
                        print(f"{self.natija_stikerlar['urush_yutqazdi']} {bayroq} {davlat} {nishon}ga qarshi urushda yutqazdi.")
                        self.ballar[oyinchi] -= 1

                elif tanlangan_harakat == "ittifoq":
                    sherik = self._tasodifiy_davlat(davlat)
                    if random.random() > 0.3:
                        bonus = 5
                        self.davlatlar[davlat]["kuch"] += bonus
                        self.davlatlar[sherik]["kuch"] += bonus
                        print(f"{self.natija_stikerlar['ittifoq_muvaffaqiyatli']} {bayroq} {davlat} va {sherik} ittifoq tuzdi!")
                        self.ballar[oyinchi] += 1.5
                    else:
                        print(f"{self.natija_stikerlar['ittifoq_qarshi']} {sherik} ittifoqqa rozi bo‘lmadi.")

                elif tanlangan_harakat == "yordam":
                    yordam_oluvchi = self._tasodifiy_davlat(davlat)
                    self.davlatlar[yordam_oluvchi]["kuch"] += 7
                    print(f"{self.natija_stikerlar['yordam_olindi']} {bayroq} {davlat} {yordam_oluvchi}ga yordam berdi.")
                    self.ballar[oyinchi] += 1

                elif tanlangan_harakat == "savdo":
                    daromad = random.randint(5, 15)
                    oldin = self.davlatlar[davlat]["kuch"]
                    self.davlatlar[davlat]["kuch"] += daromad
                    print(f"{self.natija_stikerlar['savdo_muvaffaqiyatli']} {bayroq} {davlat} savdodan foyda ko‘rdi! Kuch: {oldin} → {self.davlatlar[davlat]['kuch']}")
                    self.ballar[oyinchi] += 1

                elif tanlangan_harakat == "neutralitet":
                    print(f"{bayroq} {davlat} bu raundda neytral qoldi. Hech qanday harbiy harakat qilmadi.")
                    self.ballar[oyinchi] += 0.5

                else:
                    print("Noto‘g‘ri harakat tanlandi. Raund o‘tkazib yuborildi.")

        self._yakuniy_natijalar()

    def _tasodifiy_davlat(self, hozirgi_davlat):
        tanlov = [d for d in self.davlatlar_royxati if d != hozirgi_davlat]
        return random.choice(tanlov)

    def _yakuniy_natijalar(self):
        print("\n🏁 O‘YIN YAKUNLANDI! Natijalar:")
        for oyinchi, ball in self.ballar.items():
            print(f"{oyinchi}: {ball} ball")

        golib = max(self.ballar, key=self.ballar.get)
        print(f"\n🥇 G‘olib: {golib} tabriklaymiz!")

# O'yinni ishga tushurish
if __name__ == "__main__":
    oyin = StrategikOyin()
    oyin.strategiya_boshlash()
