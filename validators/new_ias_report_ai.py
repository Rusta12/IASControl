import pandas as pd
import os
#Модули
from validators.responsible.responsible_main import responsible_main_concat 
from validators.triggers.triggers_main import triggers_main_concat
from validators.status.status_main import status_main_concat
from validators.sports.sports_main import sports_main_concat
from validators.collectiv_def import load_dfiascontrol

#Загрузка отчета!
def read_report():
	file_name = r"C:/DataIAS/Список спортмероприятий.xlsx"
	excel_file_path = r"C:/DataIAS/Список спортмероприятий IASControl.xlsx"
	xls = pd.ExcelFile(file_name) 
	df = pd.read_excel(xls, 'Список спортмероприятий')
	df = parse_dates(df)
	df['Ссылка'] = 'https://iasnew.sport.mos.ru/events-app/' + df['Id'].astype(str)
	df['IASControl'] = ''
	df.to_excel(excel_file_path, index=False)
	print(f'Файл обновлен - {excel_file_path}')
	return excel_file_path

#Расширяем даты проведения
def parse_dates(df):
    # Создаем новые столбцы
    df[['Дата начала', 'Дата конца']] = df['Сроки пров.'].str.split(' ', expand=True)
    # Если есть строки только с одной датой, заполняем 'Дата конца' значением из 'Дата начала'
    df['Дата конца'] = df['Дата конца'].fillna(df['Дата начала'])
    # Конвертируем строки в datetime (опционально)
    df['Дата начала'] = pd.to_datetime(df['Дата начала'], dayfirst=True)
    df['Дата конца'] = pd.to_datetime(df['Дата конца'], dayfirst=True)
    #Считаем дни
    df['Количество дней'] = (df['Дата конца'] - df['Дата начала']).dt.days + 1
    #Делаем квартал
    df['Квартал'] = pd.PeriodIndex(df['Дата конца'], freq='Q')
    #Делаем месяц
    df['Месяц'] = pd.PeriodIndex(df['Дата конца'], freq='M')
    return df

def chek_file_save(df, name_file):
	file_name = fr"C:/DataIAS/Список спортмероприятий ({name_file}).xlsx"
	xls = pd.ExcelFile(file_name) 
	dfx = pd.read_excel(xls, 'Sheet1')
	if dfx.shape[0] == 0:
		df.loc[:, ['Реестр №', 'IASControl']].to_excel(file_name, index=False)
	else:
		# Если есть данные, обновляем комментарии, где номера совпадают
		dfx = dfx.set_index('Реестр №')
		df = df.set_index('Реестр №')
		# Объединяем данные: заменяем существующие и добавляем новые
		dfx.update(df)
		df_final = pd.concat([dfx, df[~df.index.isin(dfx.index)]])
		# Сохраняем результат в Excel
		df_final.iloc[:, [0]].to_excel(file_name, index=False)
	print('Файл обновлен - ', file_name)
	return


#Сводная функция дял проверки
def concat_all_report(excel_file_path):
	responsible_main_concat(excel_file_path)
	triggers_main_concat(excel_file_path)
	status_main_concat(excel_file_path)
	sports_main_concat(excel_file_path)
	print('Все проверки пройдены')
	return


#Сохроняем файлы для обработки в ИАС Спорт
def save_file_DataIAS(name_file):
	#Загрузка файла и Сохраняем для анализа в Excel
	excel_file_path = read_report()
	#Проверка мероприятий
	concat_all_report(excel_file_path)
	dfiascontrol = load_dfiascontrol(excel_file_path)
	# Фильтрация строк, где поле 'Комментарий IASControl' не пустое
	df_unique = dfiascontrol[dfiascontrol['IASControl'].isna() | (dfiascontrol['IASControl'] == '')]
	#Заполняем файл файл для соглосования.
	chek_file_save(df_unique, name_file)
	os.startfile(excel_file_path)
	return 