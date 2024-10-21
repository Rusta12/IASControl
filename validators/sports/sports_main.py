import pandas as pd
import re
#Модули
from validators.collectiv_def import input_report_text 
from validators.collectiv_def import search_region, IASControl_comment
from validators.collectiv_def import search_status_sports


def filtred_complex_event(df, excel_file_path):
    name_status = '|'.join(search_status_sports)
    name_region = '|'.join(search_region)
    df_filtered = df[
        df['Место проведения'].str.contains(name_region, case=False, na=False) &
        df['Вид спорта'].str.contains(name_status, case=False, na=False)
    ]
    report_text = IASControl_comment['sports'][0]
    input_report_text(df_filtered, excel_file_path, report_text)
    return

#Общая проверка по отвественным.
def sports_main_concat(df, excel_file_path):
    filtred_complex_event(df, excel_file_path)
    print('Общая проверка по Виду спорта успешно пройдена!')
    return