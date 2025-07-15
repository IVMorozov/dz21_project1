from pprint import pprint
from mistralai import Mistral
from ..barbershop.settings import MISTRAL_MODERATIONS_GRADES, MISTRAL_API_KEY

import os
# from dotenv import load_dotenv


# load_dotenv()

# MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
# MISTRAL_API_KEY='lzhnfxZArJOTf4pOewWrsWWQoJYjmm6c'

# MISTRAL_MODERATIONS_GRADES = {
#     "hate_and_discrimination": 0.1,  # ненависть и дискриминация
#     "sexual": 0.1,  # сексуальный
#     "violence_and_threats": 0.1,  # насилие и угрозы
#     "dangerous_and_criminal_content": 0.1,  # опасный и криминальный контент
#     "selfharm": 0.1,  # самоповреждение
#     "health": 0.1,  # здоровье
#     "financial": 0.1,  # финансовый
#     "law": 0.1,  # закон
#     "pii": 0.1,  # личная информация
# }

def is_bad_review(review_text: str, api_key: str = MISTRAL_API_KEY, grades: dict = MISTRAL_MODERATIONS_GRADES,) -> bool:
    # Создаем клиента Mistral с переданным API ключом
    client = Mistral(api_key=api_key)

    # Формируем запрос
    response = client.classifiers.moderate_chat(
        model="mistral-moderation-latest",
        inputs=[{"role": "user", "content": review_text}],
    )
    # Вытаскиваем данные с оценкой
    result = response.results[0].category_scores

    # Округляем значения до двух знаков после запятой
    result = {key: round(value, 2) for key, value in result.items()}

    pprint(result)

    # Словарь под результаты проверки
    checked_result = {}

    for key, value in result.items():
        if key in grades:
            checked_result[key] = value >= grades[key]

    # Если одно из значений True, то отзыв не проходит модерацию
    return any(checked_result.values())

if __name__ == "__main__":
    print(
        is_bad_review(' Итого, стрижка у Тимура 1200, Очень дорого!! Работы по устранению последствий стрижки Тимура 1800... неплохо так сходил башку в порядок привел. В общем и целом прихожу к мнению, что барбершопы OldBoy, некогда очень хорошие барбершопы, в целях увеличения доходов стали принимать на работу низкооплачиваемых специалистов. В ущерб клиентам, разумеется. Они, конечно извинились, все такое... но осадочек остался. В эту "цирюльню" я уже точно никогда не пойду, в другую цирюльню под вывеской OldBoy если и пойду, то только от безисходности. СВОЛОЧИ!!!  Живу: Россия, Поселок Совхоза Раменское, ул. Ленина, д.1.')
    )