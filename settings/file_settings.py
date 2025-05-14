import pandas as pd
import os


expected_files = [
    'Список спортмероприятий (внесение изменений).xlsx',
    'Список спортмероприятий (исключение).xlsx',
    'Список спортмероприятий (исправления).xlsx',
    'Список спортмероприятий (на комиссию).xlsx',
    'Список спортмероприятий (отклонение).xlsx',
    'Список спортмероприятий (утверждение).xlsx',
    'Список спортмероприятий (участие).xlsx',
]

expected_folders = [
    'CalendarSchoolSportFinans',
    'CalendarRankSport',
]


def create_missing_files(folder_path='.'):
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
            df = pd.DataFrame(columns=["Реестр №", "IASControl"])
            # Сохранение в Excel-файл
            df.to_excel(file_path, index=False)
        else:
            print(f"Файл {file} уже существует.")
    # Открытие проводника в указанной папке
    os.startfile(folder_path)
    print("Открыт проводник с файлами.")

def create_folders_from_lists(base_path='.'):
    """
    Создаёт папки, если они отсутствуют.
    
    :param expected_folders: один или несколько списков с названиями папок
    :param base_path: путь, относительно которого будут созданы папки (по умолчанию текущая директория)
    """
    for folder_list in expected_folders:
        for folder_name in folder_list:
            folder_path = os.path.join(base_path, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Папка создана: {folder_path}")
            else:
                print(f"Папка уже существует: {folder_path}")