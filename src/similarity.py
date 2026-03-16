from math import sqrt

def cosine_similarity(v1, v2):
    
    dot = sum(a*b for a,b in zip(v1,v2))
    
    norm1 = sqrt(sum(a*a for a in v1))
    norm2 = sqrt(sum(b*b for b in v2))
    
    if norm1 == 0 or norm2 == 0:
        return 0
    
    return dot/(norm1*norm2)


def find_similar(target, data):

    target_vector = data[target]

    scores = {}

    for hero, vector in data.items():
        if hero == target:
            continue

        score = cosine_similarity(target_vector, vector)
        scores[hero] = score

    return sorted(scores.items(), key=lambda x: x[1], reverse=True)