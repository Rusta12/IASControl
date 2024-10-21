import pandas as pd
import re
#Модули
from validators.collectiv_def import input_report_text, search_open
from validators.collectiv_def import search_region, IASControl_comment
from validators.collectiv_def import search_status_check, search_status_world


def filtred_event_name_status(df, excel_file_path):
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

def filtred_event_world(df, excel_file_path):
    name_status = '|'.join(search_status_world)
    name_region = '|'.join(search_region)
    df_filtered = df[
        df['Место проведения'].str.contains(name_region, case=False, na=False) &
        df['Статус мероприятия'].str.contains(name_status, case=False, na=False)
    ]
    report_text = IASControl_comment['verify_status'][1]
    input_report_text(df_filtered, excel_file_path, report_text)
    return

#Общая проверка по отвественным.
def status_main_concat(df, excel_file_path):
    filtred_event_name_status(df, excel_file_path)
    filtred_event_world(df, excel_file_path)
    print('Общая проверка по Статусу успешно пройдена!')
    return