import pandas as pd
#Модули
from validators.responsible.responsible_main import responsible_main_concat 
from validators.triggers.triggers_main import triggers_main_concat

#Загрузка отчета!
def read_report():
	file_name = r"C:/DataIAS/Список спортмероприятий.xlsx"
	xls = pd.ExcelFile(file_name) 
	df = pd.read_excel(xls, 'Список спортмероприятий')
	df['IASControl'] = ''
	return df



def chek_file_save(df, name_file):
    file_name = fr"C:/DataIAS/Список спортмероприятий ({name_file}).xlsx"
    xls = pd.ExcelFile(file_name) 
    dfx = pd.read_excel(xls, 'Sheet1')
    if dfx.shape[0] == 0:
        df.iloc[:, [0, 1]].to_excel(file_name, index=False)
    elif dfx.shape[0] >= 1:
        df = pd.concat([dfx, df])
        df.iloc[:, [0, 1]].to_excel(file_name, index=False)
    else:
        pass
    print('Файл обновлен - ', file_name)


def chek_file_deviation(df):
	if df.shape[0] == 0:
		print('Замечаний для отклонения не обнаружено')
		return
	else:
		pass
	file_name = r"C:/DataIAS/Список спортмероприятий (отклонение).xlsx"
	xls = pd.ExcelFile(file_name)
	dfx = pd.read_excel(xls, 'Sheet1')
	if dfx.shape[0] == 0:
		df.iloc[:, [0, 1]].to_excel(file_name, index=False)
	elif dfx.shape[0] >= 1:
		df = pd.concat([dfx, df])
		df.iloc[:, [0, 1]].to_excel(file_name, index=False)
	else:
		pass
	print('Файл обновлен - ', file_name)
	return

def concat_all_report(df):
	dftmp1 = responsible_main_concat(df)
	dftmp2 = triggers_main_concat(df)
	df_concat = pd.concat([dftmp1, dftmp2])
	return df_concat


#Сохроняем файлы для обработки в ИАС Спорт
def save_file_DataIAS(name_file):
	#Загрузка файла
	df = read_report()
	#Мероприятия каоторые не прошли проверку
	dftmp = concat_all_report(df)
	#Убирамем мероприятия которые не прошли проверку из общего списка
	df_unique = df[~df.iloc[:, 0].isin(dftmp.iloc[:, 0])]
	#Заполняем список для отклонения
	chek_file_deviation(dftmp)
	#Заполняем файл файл для соглосования.
	chek_file_save(df_unique, name_file)
	return df_unique