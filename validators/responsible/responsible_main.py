import pandas as pd
#Модули
from validators.collectiv_def import input_report_text, search_msk, search_rf, search_region, IASControl_comment
from validators.collectiv_def import load_dfiascontrol

#Без отвественных за проведение где больше 300
def responsible_for_conducting(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    name_region = '|'.join(search_region)
    df = df[df['Место проведения'].str.contains(name_region, case=False, na=False)]
    df = df[(df['Кол. участ.'] >= 300)]
    df = df[~(df['Ответственные лица'].str.contains(
        'Ответ. за проведение', case=False, na=False
    ))]
    report_text = IASControl_comment['responsible'][0]
    input_report_text(df, excel_file_path, report_text)
    return


#Без отвественных за проведение ЧМ ПМ КМ
def responsible_for_rank(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    df = df[(df['Кол. участ.'] < 300)]
    search_list = search_msk
    df = df[df['Статус мероприятия'].str.contains("|".join(search_list))]
    df = df[~(df['Ответственные лица'].str.contains(
        'Ответ. за проведение', case=False, na=False
    ))]
    report_text = IASControl_comment['responsible'][1]
    input_report_text(df, excel_file_path, report_text)
    return

#Без отвественных за проведение по ВС в г. Москве
def responsible_for_rf(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    df = df[(df['Место проведения'].str.contains(
        'Москва', case=False, na=False
    ))] 
    df = df[(df['Кол. участ.'] < 300)]
    search_list = search_rf
    df = df[df['Статус мероприятия'].str.contains("|".join(search_list))]
    df = df[~(df['Ответственные лица'].str.contains(
        'Ответ. за проведение', case=False, na=False
    ))]
    report_text = IASControl_comment['responsible'][2]
    input_report_text(df, excel_file_path, report_text)
    return

 #Обновить номера телефонов (НЕ ИСПОЛЬЗУЕТСЯ)
def responsible_for_contact(excel_file_path):
    df = load_dfiascontrol(excel_file_path)
    df = df[(df['Ответственные лица'].str.contains(
        'Ответ. за проведение', case=True, na=False
    ))]
    pattern = r'\+7\d{10}'
    df = df[~(df['Ответственные лица'].str.contains(
        pattern, case=False, na=False
    ))]
    report_text = IASControl_comment['responsible'][3]
    input_report_text(df, excel_file_path, report_text)
    return


#Общая проверка по отвественным.
def responsible_main_concat(excel_file_path):
    responsible_for_conducting(excel_file_path)
    responsible_for_rank(excel_file_path)
    responsible_for_rf(excel_file_path)
    print('Общая проверка по отвественным успешно пройдена!')
    return