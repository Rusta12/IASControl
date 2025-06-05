import new_ias_basic_function as ias
from settings.config import login_b, login_a, pass_b, pass_a


#================== обновленные ===========================================
#Функция соглосования изменений мероприятий (согласовано ответственным)
def change_approve(name_period: int, df, razdel_ekp):
   #========= Вход
   ias.come_application(login_b, pass_b)
   #======== Вход в раздел заявок
   ias.come_section_application()
   #======= Фильтр чистка
   ias.clear_filters('заявки')
   #======= Фильтр календаря
   ias.filter_application(name_period, razdel_ekp, 'заявки')
   #======= Фильтр проверено - изменение
   ias.filter_change('внесение')
   #======= Цикл перебора мероприятий
   ias.list_application(df, 'agree_event', 'заявки', 'согласовано ответственным')
   return ias.nan_application 

#Функция отправки мероприятий на комиссию
def commission_application(name_period: int, df, razdel_ekp):
   #========= Вход
   ias.come_application(login_b, pass_b)
   #======== Вход в раздел заявок
   ias.come_section_application()
   #======= Фильтр чистка
   ias.clear_filters('заявки')
   #======= Фильтр календаря
   ias.filter_application(name_period, razdel_ekp, 'заявки')
   #======= Фильтр проверено - включение
   ias.filter_change('включение')
   #======= Цикл перебора мероприятий
   ias.list_application(df, 'agree_event', 'заявки', 'на комиссию')
   return ias.nan_application

#Функция утверждения мероприятий
def commission_approve(name_period: int, df):
	#========= Вход
   ias.come_application(login_b, pass_b)
   #======== Вход в раздел заявок
   ias.come_section_application()
   #======= Фильтр чистка
   ias.clear_filters('заявки')
   #======= Фильтр календаря
   ias.filter_application(name_period, 'заявки')
   #======= Фильтр проверено - включение
   ias.filter_approve('на комиссию')
   #======= Цикл перебора мероприятий
   ias.list_application(df, 'agree_event', 'заявки', 'согласовано комиссией')
   return ias.nan_application


#Функция отклонений по причине ... 
def deviation(name_period: int, df):
   #========= Вход
   ias.come_application(login_b, pass_b)
   #======== Вход в раздел заявок
   ias.come_section_application()
   #======= Фильтр чистка
   ias.clear_filters('заявки')
   #======= Фильтр календаря
   ias.filter_application(name_period, 'заявки')
   #======= Фильтр проверено - включение или отклонено
   ias.filter_change('отклонено')
   #======= Цикл перебора мероприятий
   ias.list_application(df, 'agree_event', 'заявки', 'отклонено')
   return ias.nan_application

#Функция соглосования участников ... 
def paty_approve(name_period: int, df):
   #========= Вход
   ias.come_application(login_b, pass_b)
   #======== Чистка фильтров
   ias.clear_filters('мероприятия')
   #======== Фильтр календаря
   ias.filter_application(name_period, razdel='мероприятия')
   #======== Фильтр статуса
   ias.status_sport()
   #======== Фильтр участия на соглосование
   ias.status_paty()
   #======= Цикл перебора мероприятий
   ias.list_application(df, 'agree_paty', 'мероприятия')
   return ias.nan_application


#Функция изменения раздела ... 
def fix_approve(name_period: int, df, name_agree:str):
   #========= Вход
   ias.come_application(login_a, pass_a)
   #======== Чистка фильтров
   ias.clear_filters('мероприятия')
   #======== Фильтр календаря
   ias.filter_application(name_period, 'мероприятия')
   #======== Фильтр статуса
   ias.status_sport()
   #======== Цикл перебора мероприятий
   ias.list_application(df, 'fix_razdel', 'мероприятия', name_agree)
   return ias.nan_application

#Функция рассмотрения заявок на исключение
def except_approve(name_period: int, df, razdel_ekp):
   #========= Вход
   ias.come_application(login_b, pass_b)
   #======== Вход в раздел заявок
   ias.come_section_application()
   #======= Фильтр чистка
   ias.clear_filters('заявки')
   #======= Фильтр календаря
   ias.filter_application(name_period, razdel_ekp, 'заявки')
   #======= Фильтр проверено - изменение
   ias.filter_change('исключение')
   #======= Цикл перебора мероприятий
   ias.list_application(df, 'agree_event', 'заявки', 'согласовано ответственным')
   return ias.nan_application 


