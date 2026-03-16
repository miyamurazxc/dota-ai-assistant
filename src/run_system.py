from pipeline import recommendation

text = input("Опишите, какого героя вы хотите: ")

hero, rec = recommendation(text)

print("Рекомендуемый герой:", hero)

print("Похожие герои:")

for h,s in rec[:3]:
    print(h, round(s,2))