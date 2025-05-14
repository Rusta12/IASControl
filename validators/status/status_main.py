import pandas as pd
import re
#Модули
from validators.collectiv_def import input_report_text, search_open
from validators.collectiv_def import search_region, IASControl_comment
from validators.collectiv_def import search_status_check, search_status_world, search_msk
from validators.collectiv_def import search_physics_culture, search_base, search_status_ytm
from validators.collectiv_def import search_rf
from validators.collectiv_def import load_dfiascontrol

def filtred_event_name_status(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    name_status = '|'.join(search_status_check)
    name_region = '|'.join(search_region)
    df_filtered = df[
        df['Наименование мероприятия'].str.contains('первенство', case=False, na=False) &
        df['Место проведения'].str.contains(name_region, case=False, na=False) &
        df['Статус мероприятия'].str.contains(name_status, case=False, na=False)
    ]
    report_text = IASControl_comment['verify_status'][0]
    input_report_text(df_filtered, excel_file_path, report_text)
    return

def filtred_event_world(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    name_status = '|'.join(search_status_world)
    name_region = '|'.join(search_region)
    df_filtered = df[
        df['Место проведения'].str.contains(name_region, case=False, na=False) &
        df['Статус мероприятия'].str.contains(name_status, case=False, na=False)
    ]
    report_text = IASControl_comment['verify_status'][1]
    input_report_text(df_filtered, excel_file_path, report_text)
    return


def filtred_event_msk_to_region(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    name_status = '|'.join(search_msk)
    name_region = '|'.join(search_region)
    df_filtered = df[
        df['Статус мероприятия'].str.contains(name_status, case=False, na=False) &
        ~(df['Место проведения'].str.contains(name_region, case=False, na=False)
    )]
    report_text = IASControl_comment['verify_status'][2]
    input_report_text(df_filtered, excel_file_path, report_text)
    return


def filtred_event_physics_culture(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    name_status = '|'.join(search_physics_culture)
    df_filtered = df[
        df['Статус мероприятия'].str.contains(name_status, case=False, na=False)
    ]
    report_text = IASControl_comment['verify_status'][3]
    input_report_text(df_filtered, excel_file_path, report_text)
    return

def filtred_event_kruglosutochnoye(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    name_status = '|'.join(search_status_ytm)
    name_base = '|'.join(search_base)
    df_filtered = df[
        df['Статус мероприятия'].str.contains(name_status, case=False, na=False) &
        df['Место проведения'].str.contains(name_base, case=False, na=False)
    ]
    report_text = IASControl_comment['verify_status'][4]
    input_report_text(df_filtered, excel_file_path, report_text)
    return

def filtred_event_minsport(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    name_status = '|'.join(search_rf)
    df_filtered = df[
        df['Статус мероприятия'].str.contains(name_status, case=False, na=False) &
        ~(df['Дополнительные календари/разделы'].str.contains('5.1. Календарный план Минспорта', case=False, na=False))
    ]
    report_text = IASControl_comment['verify_status'][5]
    input_report_text(df_filtered, excel_file_path, report_text)
    return


#Общая проверка по отвественным.
def status_main_concat(excel_file_path):
    filtred_event_name_status(excel_file_path)
    filtred_event_world(excel_file_path)
    filtred_event_msk_to_region(excel_file_path)
    filtred_event_physics_culture(excel_file_path)
    filtred_event_kruglosutochnoye(excel_file_path)
    filtred_event_minsport(excel_file_path)
    print('Общая проверка по Статусу успешно пройдена!')
    return