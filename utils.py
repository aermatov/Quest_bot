import random


def random_choice_answer():
    result = random.choice(["Удача", "Не удача"])
    if result == "Удача":
        return result, "Вам улыбнулась удача! Проходите дальше"
    else:
        return result, "Упс"
