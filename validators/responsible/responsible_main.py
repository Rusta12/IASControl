import pandas as pd
#Модули
from validators.collectiv_def import input_report_text, search_msk, search_rf, search_region, IASControl_comment


#Без отвественных за проведение где больше 300
def responsible_for_conducting(df):
    name_region = '|'.join(search_region)
    df = df[df['Место проведения'].str.contains(name_region, case=False, na=False)]
    df = df[(df['Кол. участ.'] >= 300)]
    df = df[~(df['Ответственные лица'].str.contains(
        'Ответ. за проведение', case=False, na=False
    ))]
    report_text = IASControl_comment['responsible'][0]
    df = input_report_text(df, report_text)
    return df


#Без отвественных за проведение ЧМ ПМ КМ
def responsible_for_rank(df):
    df = df[(df['Кол. участ.'] < 300)]
    search_list = search_msk
    df = df[df['Статус мероприятия'].str.contains("|".join(search_list))]
    df = df[~(df['Ответственные лица'].str.contains(
        'Ответ. за проведение', case=False, na=False
    ))]
    report_text = IASControl_comment['responsible'][1]
    df = input_report_text(df, report_text)
    return df

#Без отвественных за проведение по ВС в г. Москве
def responsible_for_rf(df):
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
    df = input_report_text(df, report_text)
    return df

 #Обновить номера телефонов
def responsible_for_contact(df):
    df = df[(df['Ответственные лица'].str.contains(
        'Ответ. за проведение', case=True, na=False
    ))]
    pattern = r'\+7\d{10}'
    df = df[~(df['Ответственные лица'].str.contains(
        pattern, case=False, na=False
    ))]
    report_text = IASControl_comment['responsible'][3]
    df = input_report_text(df, report_text)
    return df


#Общая проверка по отвественным.
def responsible_main_concat(df):
    df1 = responsible_for_conducting(df)
    df2 = responsible_for_rank(df)
    df3 = responsible_for_rf(df)
    #df4 = responsible_for_contact(df) временно отключено
    df_concat = pd.concat([df1, df2, df3])
    return df_concat