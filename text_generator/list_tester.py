phones_with_scores = [
    {
        "name": "Fairphone 5",
        "score": 4.1
    },
    {
        "name": "Galaxy S24 Ultra",
        "score": 2.2
    },
    {
        "name": "HUAWEI Pura 70 Ultra",
        "score": 2.0
    },
    {
        "name": "iPhone 16",
        "score": 4.0
    },
    {
        "name": "Redmi 14C",
        "score": 2.6
    }
]

sorted_scores = sorted(phones_with_scores, key=lambda x: x['score'])
best_phones = sorted_scores[-4:]
best_phones.reverse()
worst_phones = sorted_scores[:4]
print(sorted_scores)
print(best_phones)
print(worst_phones)