from similarity import find_similar
from heroes_vectors import heroes

target = "juggernaut"

result = find_similar(target, heroes)

print("Heroes similar to", target)

for hero,score in result:
    print(hero, round(score,2))