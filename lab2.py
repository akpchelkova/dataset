import pandas as pd
import random
import re

def read_data(file_path):
    """Читать данные из XML файла."""
    return pd.read_xml(file_path)


def anonymize_dataset(df, quasi_identifiers):
    """Обезличить набор данных, заменяя квази-идентификаторы."""
    for col in quasi_identifiers:
        if col in df.columns:
            if col == 'ФИО':
                # Обезличиваем ФИО, оставляя только пол
                df[col] = df[col].apply(lambda x: random.choice(['Ж', 'М']) if isinstance(x, str) else x)
            elif col == 'ПаспортныеДанные':
                # Оставляем только последние 2 цифры паспортных данных
                df[col] = df[col].apply(lambda x: str(x)[-2:] if isinstance(x, str) and len(x) >= 2 else x)
            elif col == 'СНИЛС':
                # Оставляем только последние 2 цифры СНИЛСа
                df[col] = df[col].apply(lambda x: str(x)[-2:] if isinstance(x, str) and len(x) >= 2 else x)
            elif col == 'ДатаПосещенияВрача':

                df[col] = df[col].apply(lambda x: str(x)[-2:] if isinstance(x, str) and len(x) >= 2 else x)
            elif col == 'ДатаПолученияАнализов':

                df[col] = df[col].apply(lambda x: str(x)[-2:] if isinstance(x, str) and len(x) >= 2 else x)
            elif col == 'СтоимостьАнализов':
                df[col] = df[col].apply(lambda x: 'меньше 2000' if (int(re.search(r'\d+', x).group()) < 2000) else 'больше 2000' if re.search(r'\d+', x) else 'NO!')
            elif col == 'КартаОплаты':
                df[col] = df[col].apply(lambda card_info: ''.join(filter(str.isalpha, card_info)))
            elif col == 'Анализы':
                df[col] = df[col].apply(lambda x: x[0] if isinstance(x, str) and x else x)
            elif col == 'Симптомы':
                df[col] = df[col].apply(lambda x: x[0] if isinstance(x, str) and x else x)
            elif col == 'ВыборВрача':
                df[col] = df[col].apply(lambda x: x[0] if isinstance(x, str) and x else x)
            else:
                # Если ошиблись
                print("Ошибочка вышла:(, таких квази нет")
        else:
            # Удаляем квази-идентификаторы, которые отсутствуют в df
            print(f"Квази-идентификатор '{col}' не найден в наборе данных. Он будет пропущен.")

    return df

def calculate_k_anonymity(df, quasi_identifiers):
    """Вывести значение K-анонимности."""
    return df.groupby(quasi_identifiers).size().min()


def report_bad_k_values(df, quasi_identifiers):
    """Вывести 'плохие' значения K-анонимности и проценты."""
    k_values = df.groupby(quasi_identifiers).size()
    bad_k_values = k_values[k_values < 7].sort_values()  # Устанавливаем порог K=7
    total_records = len(df)
    return bad_k_values, total_records


def report_unique_rows(df, k):
    """Вывод уникальных строк при K=1."""
    if k == 1:
        unique_rows = df.drop_duplicates()
        return unique_rows
    else:
        return None


def acceptable_k_value(df):
    """Оценить приемлемое значение K-анонимности для набора данных."""
    record_count = len(df)
    if record_count <= 51000:
        return 10
    elif record_count <= 105000:
        return 7
    elif record_count <= 260000:
        return 5
    return None


def main():
    file_path = 'medical_dataset.xml'
    df = read_data(file_path)

    # Ввод квази-идентификаторов
    quasi_identifiers = input("Введите квази-идентификаторы через запятую: ").strip().split(',')
    quasi_identifiers = [q.strip() for q in quasi_identifiers]

    print(f"\nЧисло записей в исходном наборе: {len(df)}")

    # Обезличивание
    anonymized_df = anonymize_dataset(df.copy(), quasi_identifiers)

    # Расчет K-анонимности
    k = calculate_k_anonymity(anonymized_df, quasi_identifiers)
    bad_k_values, total_records = report_bad_k_values(anonymized_df, quasi_identifiers)

    # Уникальные строки при K=1
    report_unique = report_unique_rows(anonymized_df, k)

    # Приемлемое значение K
    min_k = acceptable_k_value(df)

    # Отчет в терминале
    print(f"\nK-анонимность обезличенного набора: {k}")
    print("\nПлохие значения K-анонимности:")
    if not bad_k_values.empty:
        bad_k_summary = bad_k_values.value_counts().head(5)  # Отображаем только 5 наименьших
        for k_val, count in bad_k_summary.items():
            print(f"K = {k_val:.0f}, процент = {count / total_records * 100:.2f}% (повторяется {count} раз)")
    else:
        print("Нет 'плохих' значений K-анонимности.")

    if report_unique is not None and not report_unique.empty:
        print("\nУникальные строки при K=1:")
        print(report_unique)

    print(f"\nПриемлемое значение K-анонимности для набора данных: K >= {min_k}")

    # Сохранение обезличенных данных
    output_file_path = 'anonymized_dataset.xml'
    anonymized_df.to_xml(output_file_path, index=False)
    print(f"\nОбезличенный датасет сохранен в {output_file_path}.")


if __name__ == "__main__":
    main()
