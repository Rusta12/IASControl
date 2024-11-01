from reports.mappings_report_fin import replace_razdel
import pandas as pd
import numpy as np
import time
from datetime import datetime
import os
import re



def replace_cost(df):
    #План
    df['PlannedCost'] = df['PlannedCost'].replace(r'\s+', '', regex=True)
    df['PlannedCost'] = df['PlannedCost'].replace('-', '0.0')
    df['PlannedCost'] = df['PlannedCost'].str.replace(',', '.')
    df['PlannedCost'] = df['PlannedCost'].astype('float')
    # Факт
    df['ActualCost'] = df['ActualCost'].replace(r'\s+', '', regex=True)
    df['ActualCost'] = df['ActualCost'].replace('-', '0.0')
    df['ActualCost'] = df['ActualCost'].str.replace(',', '.')
    df['ActualCost'] = df['ActualCost'].astype('float')
    # Столбцы
    df = df[[
        'CalendarSectionName1', 'Textbox1', 'NameSummary',
        'SportName', 'Summary', 'Appointment', 'Textbox117',
        'Count', 'Textbox9', 'FirmName', 'ExpenseTypeShortName',
        'PlannedCost', 'ActualCost'
    ]]
    return df


def parse_dates(date_str, period):
    # Определяем текущий и следующий годы для обработки
    current_year = period
    next_year = period + 1

    # Шаблоны для поиска одной или двух дат
    pattern_two_dates = r'(\d{2}\.\d{2}) (\d{2}\.\d{2})'
    pattern_one_date = r'(\d{2}\.\d{2})$'

    # Проверяем, соответствуют ли данные одному из шаблонов
    match_two = re.match(pattern_two_dates, date_str)
    match_one = re.match(pattern_one_date, date_str)

    if match_two:
        # Парсим две даты
        date_start_str, date_end_str = match_two.groups()
        date_start = datetime.strptime(date_start_str + f'.{current_year}', '%d.%m.%Y')
        date_end = datetime.strptime(date_end_str + f'.{current_year}', '%d.%m.%Y')
        
        # Если дата окончания меньше даты начала, то это переход на следующий год
        if date_end < date_start:
            date_end = datetime.strptime(date_end_str + f'.{next_year}', '%d.%m.%Y')
        
        return date_start, date_end

    elif match_one:
        # Если только одна дата, парсим и возвращаем её для обеих колонок
        date_start = datetime.strptime(match_one.group(1) + f'.{current_year}', '%d.%m.%Y')
        return date_start, date_start

    return None, None

def cor_dates(df, period):
    period = int(period)
    df[['Date_at', 'Date_of']] = df['Textbox117'].apply(lambda x: pd.Series(parse_dates(x, period)))
    #Считаем дни
    df['Count_day'] = (df['Date_of'] - df['Date_at']).dt.days + 1
    #Делаем квартал
    df['Quarter'] = pd.PeriodIndex(df['Date_of'], freq='Q')
    #Делаем месяц
    df['Month_m'] = pd.PeriodIndex(df['Date_of'], freq='M')
    return df

def transform_record(record):
    # Используем регулярное выражение, чтобы оставить только нужную часть
    return re.sub(r'^\S+\s*', '', record)  # Убираем все, что перед первым пробелом



def replace_df(df, name_colum):
    df[name_colum] = df[name_colum].replace(replace_razdel)
    return df

def colum_action(df):
    # Оставляем только нужные поля
    df = df[['CalendarSectionName1', 'RazdelShool', 'Textbox1',
                        'NameSummary', 'SportName', 'Summary', 'Appointment',
                        'Date_at', 'Date_of', 'Count_day', 'Quarter', 'Month_m',
                        'Textbox9', 'Count', 'FirmName', 'ExpenseTypeShortName',
                        'PlannedCost', 'ActualCost',
                        ]]
    return df



def rename_columns(df):
    # Переименовываем столбцы на рус
    new_df = ['Раздел календаря', 'Раздел учреждения', 'Реестр №',
               'Наименование мер', 'Вид спорта', 'Дисциплины и возрастная группа',
               'Место проведения', 'Дата начала', 'Дата завершения', 'Кол-во дней',
               'Квартал', 'Месяц', 'Пров\Участие', 'Кол-во. уч.', 'Организаторы', 'Тип расходов',
               'План расходов', 'Факт расходов',
               ]
    df.set_axis(new_df, axis='columns', inplace=True)
    return df


def to_xlsx(df, period, name):
    name = str(name)
    name_0 = fr"C:\DataIAS\CalendarSchoolSportFinans\{period}\Calendar"
    df = rename_columns(df)
    creation = datetime.today().strftime("%d_%m_%Y")
    tmp_df = f"{name_0}{period}_{name}_{creation}.xlsx"
    df.to_excel(tmp_df, index=False)
    print("Файл успешно сохранился")
    print(tmp_df)
    os.startfile(tmp_df)



def mean_analysis(file_name, period:str, name):
    df = pd.read_csv(file_name, error_bad_lines=False)
    df = replace_cost(df)
    df = cor_dates(df, period)
    df['RazdelShool'] = df['CalendarSectionName1'].apply(transform_record)
    df = replace_df(df, 'RazdelShool')
    df = colum_action(df)
    to_xlsx(df, period, name)
    os.remove(file_name)