import time
from settings.config import *
import pandas as pd
import numpy as np
import datetime
import os
import re
import time

url_report = "https://ias.sport.mos.ru/Reports/ReportViewer.aspx?report_name=Отчет+по+разрядам+и+званиям+спортсменов+города+Москвы"

file_name = r'C:\DataIAS\Отчет по разрядам и званиям спортсменов города Москвы.csv'

base_filename ='RankSport'

directory = 'C:/DataIAS/CalendarRankSport'



def calendar_rank_report(name, pass_name):
    #Вход в ИАС
    driver.get(url_report)
    driver.implicitly_wait(30)
    login = driver.find_element(By.XPATH, "//input[@id='UserName']")
    login.send_keys(name)
    pas = driver.find_element(By.XPATH, "//input[@id='Password']")
    pas.send_keys(pass_name, Keys.RETURN)
    time.sleep(4)
    return

def click_view_report_button():
    while True:
        try:
            # Ожидаем появления и кликабельности кнопки
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "rvMain_ctl04_ctl00"))
            )
            button.click()
            print("Кнопка 'Просмотр отчета' была нажата!")
            break  # Выход из цикла после успешного нажатия

        except Exception as e:
            print(f"Кнопка недоступна: {e}. Повторная попытка через 5 секунд...")
            time.sleep(5)  # Пауза перед следующей попыткой

def input_date_if_provided(
    day:int = None,
    month:int = None,
    year:int = None,
    hour:int = 0,
    minute:int = 0,
):
    try:
        element = driver.find_element(By.ID, "rvMain_ctl04_ctl03_txtValue")
        # Проверяем, заданы ли месяц и год
        if month is not None and year is not None and day is not None:
            # Форматируем дату с ведущими нулями
            formatted_date = f"{day:02d}.{month:02d}.{year} 0:00:00"
            element.clear()
            element.send_keys(formatted_date)
            print(f'Выставленна дата: {formatted_date}')
            click_view_report_button()
            time.sleep(60)
        elif month is not None and year is not None:
            formatted_date = f"01.{month:02d}.{year} {hour:02d}:{minute:02d}:00"
            element.clear()
            element.send_keys(formatted_date)
            print(f'Выставленна дата: {formatted_date}')
            click_view_report_button()
            time.sleep(60)
        elif month is not None:
            current_year = datetime.datetime.now().year
            formatted_date = f"01.{month:02d}.{current_year} {hour:02d}:{minute:02d}:00"
            element.clear()
            element.send_keys(formatted_date)
            print(f'Выставленна дата: {formatted_date}')
            click_view_report_button()
            time.sleep(60)
        elif year is not None:
            formatted_date = f"31.12.{year} {hour:02d}:{minute:02d}:00"
            element.clear()
            element.send_keys(formatted_date)
            print(f'Выставленна дата: {formatted_date}')
            click_view_report_button()
            time.sleep(60)
        else:
            print("Месяц и год не заданы - данные не вводятся")
            
    except Exception as e:
        print(f"Произошла ошибка в функции даты {e}")

def input_in_department(department:str = None, timeout=30, max_attempts=5):
    for attempt in range(1, max_attempts + 1):
        try:
            element = driver.find_element(By.ID, "rvMain_ctl04_ctl09_txtValue")
            if department == 'Москомспорт':
                element.click()
                time.sleep(1)
                checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "rvMain_ctl04_ctl09_divDropDown_ctl00"))
                )
                checkbox.click()
                checkdep = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "rvMain_ctl04_ctl09_divDropDown_ctl01"))
                )
                checkdep.click()
                print(f'Выставлено ведомство: {department}')
                click_view_report_button()
                break
            else:
                break
        except Exception as e:
            print(f"Произошла ошибка в функции ведомтсво {e}")
            print(f"Попытка {attempt}/{max_attempts} не удалась: {str(e)}")
            if attempt == max_attempts:
                raise
            time.sleep(10)  # Пауза перед повторной попыткой

def calendar_reload(timeout=30, max_attempts=5):
    """
    Загружает отчёт в формате CSV и закрывает браузер.
    Параметры:
        driver: WebDriver (например, Chrome или Firefox)
        timeout (int): Максимальное время ожидания элемента (сек)
        max_attempts (int): Количество попыток загрузки
    """
    try:
        print("Запуск загрузки отчёта...")
        for attempt in range(1, max_attempts + 1):
            try:
                # 1. Нажимаем кнопку экспорта
                export_btn = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, "//img[@id='rvMain_ctl06_ctl04_ctl00_ButtonImg']"))
                )
                export_btn.click()
                time.sleep(2)
                # 2. Выбираем CSV-формат
                csv_link = WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'CSV (с разделителями-запятыми)')]"))
                )
                csv_link.click()
                print("Начата загрузка CSV-файла...")
                # 3. Даём время на загрузку файла (можно настроить)
                time.sleep(90)
                # Ожидание скачивания
                break
                
            except Exception as e:
                print(f"Попытка {attempt}/{max_attempts} не удалась: {str(e)}")
                if attempt == max_attempts:
                    raise
                time.sleep(5)  # Пауза перед повторной попыткой
    finally:
        # Всегда закрываем браузер, даже если возникла ошибка
        print("Завершение работы браузера...")
        driver.quit()
        print("Готово!")        

def save_df_to_csv(df, directory='.', base_filename='RankSport', month=None, year=None):
    """
    Сохраняет DataFrame в CSV с именем файла по шаблону:
    :param df: DataFrame для сохранения
    :param directory: папка для сохранения файла
    :param base_filename: базовое имя файла
    :param month: месяц (int или str)
    :param year: год (int или str)
    """
    n = df['SportsmenId'].count()
    n = f'{n:,.0f}'.replace(",", " ").replace(".", ",")
    if month and year:
        filename = f"{base_filename}_{n}_{month:02d}-{year}.csv"
    elif month is not None:
        current_year = datetime.datetime.now().year
        filename = f"{base_filename}_{n}_{month:02d}-{current_year}.csv"
    elif year is not None:
        filename = f"{base_filename}_{n}_31_12-{year}.csv"
    else:
        current_year = datetime.datetime.now().year
        current_month = datetime.datetime.now().month
        filename = f"{base_filename}_{n}_{current_month:02d}-{current_year}.csv"

    filepath = f"{directory}/{filename}"
    df.to_csv(filepath, index=False, sep='\t')
    print(f"Файл сохранён: {filepath}")

def CalendarRankSport(day, month, year, department:str = None):
    calendar_rank_report(login_b, pass_b)
    input_date_if_provided(day, month, year)
    input_in_department(department)
    calendar_reload()
    df = pd.read_csv(file_name, on_bad_lines='warn')
    save_df_to_csv(df, directory, base_filename, month, year)
    os.remove(file_name)
    return
