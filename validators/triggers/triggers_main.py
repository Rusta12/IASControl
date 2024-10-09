import pandas as pd
#Модули
from validators.collectiv_def import input_report_text, search_open
from validators.collectiv_def import search_region, IASControl_comment
from validators.collectiv_def import search_status, search_festival
from validators.collectiv_def import search_outdoors, search_dep

#Поиск по открытым наименованияммероприятий
def filtred_open_events(df):
    name_event = '|'.join(search_open)
    name_region = '|'.join(search_region)
    df_filtered = df[
        df['Место проведения'].str.contains(name_region, case=False, na=False) &
        df['Наименование мероприятия'].str.contains(name_event, case=False, na=False)
    ]
    report_text = IASControl_comment['triggers'][0]
    df = input_report_text(df_filtered, report_text)
    return df

#Поиск по статусам и наименованиям не для Москвы
def filtred_status_events(df):
    name_status = '|'.join(search_status)
    name_region = '|'.join(search_region)
    df_filtered = df[
        df['Место проведения'].str.contains(name_region, case=False, na=False) &
        df['Статус мероприятия'].str.contains(name_status, case=False, na=False) 
    ]
    report_text = IASControl_comment['triggers'][1]
    df = input_report_text(df_filtered, report_text)
    return df

#Поиск по наименованиям студентческие мероприятия
def filtred_students_events(df):
    name_students = '|'.join(search_status)
    df_filtered = df[
        df['Наименование мероприятия'].str.contains(search_status, case=False, na=False)
    ]
    report_text = IASControl_comment['triggers'][2]
    df = input_report_text(df_filtered, report_text)
    return df

#Поиск по наименованию фестевальных мероприятий
def filtred_festival_events(df):
    name_festival = '|'.join(search_festival)
    name_region = '|'.join(search_region)
    df_filtered = df[
        df['Место проведения'].str.contains(name_region, case=False, na=False) &
        df['Наименование мероприятия'].str.contains(name_festival, case=False, na=False)
    ]
    report_text = IASControl_comment['triggers'][3]
    df = input_report_text(df_filtered, report_text)
    return df


#Поиск мероприятий на дворовой территории
def filtred_outdoors_events(df):
    name_outdoors = '|'.join(search_outdoors)
    df_filtered = df[
        df['Место проведения'].str.contains(name_outdoors, case=False, na=False) 
    ]
    report_text = IASControl_comment['triggers'][4]
    df = input_report_text(df_filtered, report_text)
    return df

#Поиск мероприятий на дворовой территории
def filtred_mks_events(df):
    name_outdoors = '|'.join(search_dep)
    df_filtered = df[
        df['Состав организаторов'].str.contains(name_outdoors, case=False, na=False) 
    ]
    report_text = IASControl_comment['triggers'][4]
    df = input_report_text(df_filtered, report_text)
    return df


#Общая проверка по отвественным.
def triggers_main_concat(df):
    df1 = filtred_open_events(df)
    df2 = filtred_status_events(df)
    df3 = filtred_students_events(df)
    df4 = filtred_festival_events(df)
    df5 = filtred_outdoors_events(df)
    df6 = filtred_mks_events(df)
    df_concat = pd.concat([df1, df2, df3, df4, df5, df6])
    return df_concat