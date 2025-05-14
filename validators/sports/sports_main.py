import pandas as pd
import re
#Модули
from validators.collectiv_def import input_report_text 
from validators.collectiv_def import search_region, IASControl_comment
from validators.collectiv_def import search_status_sports, search_status_ytm, search_years_athletes
from validators.collectiv_def import search_sports_inva, search_team__sports
from validators.collectiv_def import load_dfiascontrol

def filtred_complex_event(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    name_status = '|'.join(search_status_sports)
    name_region = '|'.join(search_region)
    df_filtered = df[
        df['Место проведения'].str.contains(name_region, case=False, na=False) &
        df['Вид спорта'].str.contains(name_status, case=False, na=False)
    ]
    report_text = IASControl_comment['sports'][0]
    input_report_text(df_filtered, excel_file_path, report_text)
    return

def filtred_lvl_ytm_event(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    name_status = '|'.join(search_status_ytm)
    name_age = '|'.join(search_years_athletes)
    df = df[~(df['Статус мероприятия'].str.contains('Учебно-тренировочное мероприятие в каникулярный период', case=False, na=False))]
    df_filtered = df[
        df['Статус мероприятия'].str.contains(name_status, case=False, na=False) &
        df['Пол/Возраст'].str.contains(name_age, case=False, na=False)
    ]
    report_text = IASControl_comment['sports'][1]
    input_report_text(df_filtered, excel_file_path, report_text)
    return

def filtred_sports_inva_event(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    name_sports = '|'.join(search_sports_inva)
    df_filtered = df[
        df['Вид спорта'].str.contains(name_sports, case=False, na=False) 
    ]
    report_text = IASControl_comment['sports'][2]
    input_report_text(df_filtered, excel_file_path, report_text)
    return

def filtred_paty_event(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    name_sports = '|'.join(search_team__sports)
    df = df[~(df['Вид спорта'].str.contains(name_sports, case=False, na=False))]
    df_filtered = df[
        df['Дополнительные календари/разделы'].str.contains(r'Другие мероприятия \(не на территории города Москвы\)', case=False, na=False) 
    ]
    report_text = IASControl_comment['sports'][3]
    input_report_text(df_filtered, excel_file_path, report_text)
    return

#Общая проверка
def sports_main_concat(excel_file_path):
    filtred_complex_event(excel_file_path)
    filtred_lvl_ytm_event(excel_file_path)
    filtred_sports_inva_event(excel_file_path)
    filtred_paty_event(excel_file_path)
    print('Общая проверка по Виду спорта успешно пройдена!')
    return