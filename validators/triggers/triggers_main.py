import pandas as pd
from datetime import datetime, timedelta
import re
#Модули
from validators.collectiv_def import input_report_text, search_open
from validators.collectiv_def import search_region, IASControl_comment
from validators.collectiv_def import search_status, search_festival
from validators.collectiv_def import search_outdoors, search_students
from validators.collectiv_def import load_dfiascontrol
from validators.collectiv_def import search_razdel_rf, search_debtor_organizer

#Поиск по открытым наименованияммероприятий
def filtred_open_events(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    name_event = '|'.join(search_open)
    name_region = '|'.join(search_region)
    df_filtered = df[
        df['Место проведения'].str.contains(name_region, case=False, na=False) &
        df['Наименование мероприятия'].str.contains(name_event, case=False, na=False)
    ]
    report_text = IASControl_comment['triggers'][0]
    input_report_text(df_filtered, excel_file_path, report_text)
    return

#Поиск по статусам и наименованиям не для Москвы
def filtred_status_events(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    name_status = '|'.join(search_status)
    name_region = '|'.join(search_region)
    df_filtered = df[
        df['Место проведения'].str.contains(name_region, case=False, na=False) &
        df['Статус мероприятия'].str.contains(name_status, case=False, na=False) 
    ]
    report_text = IASControl_comment['triggers'][1]
    input_report_text(df_filtered, excel_file_path, report_text)
    return

#Поиск по наименованиям студентческие мероприятия
def filtred_students_events(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    name_students = '|'.join(search_students)
    df_filtered = df[
        df['Наименование мероприятия'].str.contains(name_students, case=False, na=False)
    ]
    report_text = IASControl_comment['triggers'][2]
    input_report_text(df_filtered, excel_file_path, report_text)
    return

#Поиск по наименованию фестевальных мероприятий
def filtred_festival_events(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    name_festival = '|'.join(search_festival)
    name_region = '|'.join(search_region)
    df_filtered = df[
        df['Место проведения'].str.contains(name_region, case=False, na=False) &
        df['Наименование мероприятия'].str.contains(name_festival, case=False, na=False)
    ]
    report_text = IASControl_comment['triggers'][3]
    input_report_text(df_filtered, excel_file_path, report_text)
    return


#Поиск мероприятий на дворовой территории
def filtred_outdoors_events(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    name_pattern = '|'.join(search_outdoors)
    df_filtered = df[
        df['Место проведения'].str.contains(name_pattern, case=False, na=False) 
    ]
    # Если фильтрация не вернула данных
    if df_filtered.empty:
        return
    report_text = IASControl_comment['triggers'][4]
    input_report_text(df_filtered, excel_file_path, report_text)
    return

#Поиск мероприятий где организатор Москомспорт
def filtred_mks_events(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    name_pattern = 'Москомспорт.'
    df_filtered = df[
        df['Состав организаторов'].str.contains(name_pattern, case=False, na=False) &
        df['Состав организаторов'].str.contains('\.', case=False, na=False) &
        ~df['Состав организаторов'].str.contains('Москомспорта', case=False, na=False)
    ]
    report_text = IASControl_comment['triggers'][5]
    input_report_text(df_filtered, excel_file_path, report_text)
    return

def filtred__upcoming_events(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    today = datetime.now().date()
    name_pattern = '|'.join(search_razdel_rf)
    df_filtered = df[
        (today - df['Дата начала'].dt.date >= timedelta(days=14)) & # Исключаем календарь минспорта
        (~df['Дополнительные календари/разделы'].str.contains(name_pattern, case=False, na=False))  
    ]
    report_text = IASControl_comment['triggers'][6]
    input_report_text(df_filtered, excel_file_path, report_text)
    return df_filtered

def filtred__upcoming_debtor(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    name_pattern = '|'.join(search_debtor_organizer)
    df_filtered = df[
        df['Состав организаторов'].str.contains(name_pattern, case=False, na=False) 
    ]
    report_text = IASControl_comment['triggers'][7]
    input_report_text(df_filtered, excel_file_path, report_text)
    return df_filtered


#Общая проверка
def triggers_main_concat_insert(excel_file_path):
    filtred_open_events(excel_file_path)
    filtred_status_events(excel_file_path)
    filtred_students_events(excel_file_path)
    filtred_festival_events(excel_file_path)
    filtred_outdoors_events(excel_file_path)
    filtred_mks_events(excel_file_path)
    filtred__upcoming_events(excel_file_path)
    filtred__upcoming_debtor(excel_file_path)
    print('Общая проверка по триггерам успешно пройдена!')
    return

def triggers_main_concat_change(excel_file_path):
    filtred_open_events(excel_file_path)
    filtred_status_events(excel_file_path)
    filtred_students_events(excel_file_path)
    filtred_festival_events(excel_file_path)
    filtred_outdoors_events(excel_file_path)
    filtred_mks_events(excel_file_path)
    print('Общая проверка по триггерам успешно пройдена!')
    return