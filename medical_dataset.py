import pandas as pd
import random
from faker import Faker
from datetime import timedelta

# Инициализация Faker
fake = Faker('ru_RU')

# Задаем параметры
num_rows = 50000  # количество строк

# Настройки банка и типов карт
banks_with_probabilities = {
    "Сбербанк": {"Visa": 0.6, "MasterCard": 0.4},
    "Тинькофф": {"Visa": 0.5, "MasterCard": 0.5},
    "Альфа-Банк": {"Visa": 0.3, "MasterCard": 0.7},
}

# Список медицинских симптомов
possible_symptoms = [
                        "Боль в грудной клетке", "Одышка", "Кашель", "Головная боль", "Температура",
                        "Тошнота", "Рвота", "Боль в животе", "Сыпь", "Слабость", "Гипертония",
                        "Гипотония", "Отечность", "Общее недомогание", "Боль в спине", "Нарушение сна",
                        "Тревожность", "Депрессия", "Потеря аппетита", "Нарушение пищеварения",
                        "Снижение веса", "Увеличение веса", "Зуд", "Сухой кашель", "Насморк",
                    ] * 200  # Дублируем для увеличения списка
possible_symptoms = list(set(possible_symptoms))[:5000]

# Уникальные специальные врачи
possible_doctors = [
                       "Терапевт", "Хирург", "Кардиолог", "Невролог", "Педиатр", "Офтальмолог",
                       "Лор", "Дерматолог", "Гастроэнтеролог", "Онколог", "Аллерголог",
                       "Иммунолог", "Эндокринолог", "Стоматолог", "Психиатр", "Ревматолог",
                       "Нарколог", "Красный Кросс", "Гинеколог", "Уролог", "Травматолог",
                       "Судебно-медицинский эксперт", "Косметолог", "Логопед",
                       "Физиотерапевт", "Фармацевт", "Ортопед", "Химиотерапевт",
                       "Мануальный терапевт", "Массажист", "Специалист по ЛФК", "Реабилитолог", "Ангиохирург", "Сосудистый хирург",
                       "Нейрохирург", "Детский невролог", "Анестезиолог", "Микрохирург",
                       "Психотерапевт", "Травматолог-ортопед", "Репродуктолог", "Челюстно-лицевой хирург",
                   ] * 2  # Дублируем для увеличения списка
possible_doctors = list(set(possible_doctors))[:50]

# Список медицинских анализов
possible_analyses = [
                        "Общий анализ крови", "Анализ крови на сахар", "Биохимический анализ крови",
                        "Анализ мочи", "ЭКГ", "УЗИ органов брюшной полости", "Рентгенографическое исследование",
                        "КТ", "МРТ", "Анализ на ПЦР", "Иммунограмма", "Аллергопробы", "Группа крови",
                        "Коагулограмма", "Гормоны", "Цитология", "Микробиологическое исследование",
                        "Тест на коронавирус", "Вторичный анализ крови", "Серологическое исследование",
                    ] * 10  # Дублируем для увеличения списка
possible_analyses = list(set(possible_analyses))[:250]

# Генерация данных
data = []
# Хранение карт для возможных повторных оплат
credit_cards = {}

for i in range(num_rows):
    name = fake.name()
    passport_data = f"{random.randint(1000, 9999)} {random.randint(100000, 999999)}"
    snil_data = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(100, 999)} {random.randint(10, 99)}"
    symptoms = random.sample(possible_symptoms, random.randint(1, 10))
    doctor = random.choice(possible_doctors)
    visit_date = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
    analysis = random.sample(possible_analyses, random.randint(1, 5))
    analysis_receive_date = visit_date + timedelta(days=random.randint(1, 3))
    analysis_cost = random.randint(500, 5000)

    # Выбор банка и вида карты на основе вероятностей
    bank = random.choices(
        list(banks_with_probabilities.keys()),
        weights=[1 / len(banks_with_probabilities)] * len(banks_with_probabilities)
    )[0]

    card_type = random.choices(
        list(banks_with_probabilities[bank].keys()),
        weights=list(banks_with_probabilities[bank].values())
    )[0]

    # Создание или выбор существующей карты
    if (bank, card_type) in credit_cards:
        payment_card = credit_cards[(bank, card_type)]
    else:
        payment_card = f"{card_type} {fake.credit_card_number()}"
        credit_cards[(bank, card_type)] = payment_card

    # Приведение дат к требуемому формату
    visit_date_str = visit_date.strftime("%d-%m-%Y/%H:%M")
    analysis_receive_date_str = analysis_receive_date.strftime("%d-%m-%Y/%H:%M")

    data.append({
        "ФИО": name,
        "ПаспортныеДанные": passport_data,
        "СНИЛС": snil_data,
        "Симптомы": ", ".join(symptoms),
        "ВыборВрача": doctor,
        "ДатаПосещенияВрача": visit_date_str,
        "Анализы": ", ".join(analysis),
        "ДатаПолученияАнализов": analysis_receive_date_str,
        "СтоимостьАнализов": f"{analysis_cost} руб.",
        "КартаОплаты": payment_card
    })

# Создание DataFrame и сохранение в XML
df = pd.DataFrame(data)
df.to_xml('medical_dataset.xml', index=False, root_name='MedicalRecords', row_name='Record')
print("Датасет успешно сгенерирован и сохранен в 'medical_dataset.xml'.")
