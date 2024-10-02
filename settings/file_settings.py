import pandas as pd
import os


folder_path = r'C:\DataIAS'
expected_files = [
    'Список спортмероприятий (изменения).xlsx',
    'Список спортмероприятий (исключение).xlsx',
    'Список спортмероприятий (исправления).xlsx',
    'Список спортмероприятий (на комиссию).xlsx',
    'Список спортмероприятий (отклонение).xlsx'
]

def create_missing_files():
    """
    Проверяет наличие файлов в папке и создает их, если они отсутствуют.

    :param folder_path: Путь к папке, где должны находиться файлы.
    :param expected_files: Список ожидаемых файлов.
    """
    for file in expected_files:
        file_path = os.path.join(folder_path, file)
        if not os.path.exists(file_path):
            print(f"Файл {file} отсутствует, создаём...")
            # Создание пустого DataFrame с заголовками
            df = pd.DataFrame(columns=["Реестр №", "Комментарий IASControl"])
            # Сохранение в Excel-файл
            df.to_excel(file_path, index=False)
        else:
            print(f"Файл {file} уже существует.")
    # Открытие проводника в указанной папке
    os.startfile(folder_path)
    print("Открыт проводник с файлами.")