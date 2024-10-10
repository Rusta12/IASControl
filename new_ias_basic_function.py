import time
import re
from datetime import datetime
#import pandas as pd
from settings.config import *


nan_application = []


# Вход в ИАС 
def come_application(name, pass_name):
   #name_period = int(name_period)
   #Вход в ИАС
   driver.get("https://iasnew.sport.mos.ru/")
   driver.implicitly_wait(30)
   login = driver.find_element(By.XPATH, "//input[@id='UserName']")
   login.send_keys(name)
   pas = driver.find_element(By.XPATH, "//input[@id='Password']")
   pas.send_keys(pass_name, Keys.RETURN)
   competition = driver.find_element(By.XPATH, "//a[contains(text(),'Реестр мероприятий')]")
   competition.send_keys(Keys.ENTER)
   time.sleep(1)
   return

#Вход в раздел заявок
def come_section_application():
   driver.implicitly_wait(30)
   driver.find_element(By.XPATH, "//span[contains(text(),'Заявки')]").click()
   return

#Нажатие на Фильтры
def filter_button(razdel='заявки'):
   driver.implicitly_wait(30)
   if razdel == 'заявки':
      driver.find_element(By.XPATH, "//app-events-app-section-header/form[1]/div[2]/div[2]/app-filters-button[1]/div[1]/button[1]").click()
      return
   elif razdel == 'мероприятия':
      #driver.find_element(By.XPATH, "//app-events-section-header/form[1]/div[2]/div[2]/app-filters-button[1]/div[1]/button[1]").click()
      driver.find_element(By.XPATH, '//button[@class="mat-menu-trigger filters-button"]').click()
      return

   #Очистка фильтров
def clear_filters(razdel='заявки'):
   filter_button(razdel)
   driver.implicitly_wait(10)
   time.sleep(1)
   clearFilter = driver.find_element(By.XPATH, "//button[contains(text(),'Сбросить всё')]")
   clearFilter.send_keys(Keys.ENTER)
   clearFilter_enter = driver.find_element(By.XPATH, "//button[contains(text(),'Применить')]")
   clearFilter_enter.send_keys(Keys.ENTER)
   time.sleep(1)
   return

   # Фильтр Календаря
def filter_application(name_period: int, razdel='заявки'):
   filter_button(razdel)
   time.sleep(1)
   driver.implicitly_wait(10)
   FilterBy = driver.find_element(By.XPATH, "//div[contains(text(),'Календари')]")
   FilterBy.click()
   driver.implicitly_wait(30)
   time.sleep(1)
   dataSort = driver.find_element(By.XPATH, 
      "//body/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/app-calendars[1]/div[1]/form[1]/div[2]/div[2]/ng-select[1]/div[1]/div[1]/div[2]/input[1]")
   dataSort.click()
   time.sleep(2)
   dataSort.send_keys(str(name_period))
   time.sleep(5)
   dataSort.send_keys(Keys.ARROW_DOWN)
   dataSort.send_keys(Keys.ENTER)
   time.sleep(1)
   driver.implicitly_wait(55)
   element = driver.find_element(By.XPATH, 
      "//body/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/app-calendars[1]/div[1]/form[1]/div[2]/div[3]/ng-select[1]/div[1]/div[1]/div[2]/input[1]")
   element.click()
   all_options = driver.find_element(By.XPATH, 
      "//span[contains(text(),'2.1. Подраздел «Спорт высших достижений и подготов')]")
   all_options.click()
   driver.implicitly_wait(30)
   clearFilter_enter = driver.find_element(By.XPATH, "//button[contains(text(),'Применить')]")
   clearFilter_enter.send_keys(Keys.ENTER)
   time.sleep(3)


   # Выбор статуса заявки
def filter_change(name_status):
   filter_button()
   driver.implicitly_wait(30)
   driver.find_element(By.XPATH, "//div[contains(text(),'Заявки')]").click()
   time.sleep(1)
   driver.implicitly_wait(35)
   driver.find_element(By.XPATH, "//div[contains(text(),'Статус заявки')]").click()
   time.sleep(1)
   driver.implicitly_wait(35)
   calendar = driver.find_element(By.XPATH, "//span[contains(text(),'проверено')]")
   calendar.click()
   time.sleep(1)
   if name_status != 'отклонено':
      driver.implicitly_wait(35)
      status = driver.find_element(By.XPATH, 
         "//body/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/app-event-application[1]/div[1]/form[1]/div[2]/div[2]/ng-select[1]/div[1]/div[1]/div[2]/input[1]")
      status.click()
      driver.implicitly_wait(30)
      time.sleep(1)
      status.send_keys(str(name_status))
      time.sleep(1)
      status.send_keys(Keys.ARROW_DOWN)
      status.send_keys(Keys.ENTER)
   else:
      pass
   clearFilter_enter = driver.find_element(By.XPATH, "//button[contains(text(),'Применить')]")
   clearFilter_enter.send_keys(Keys.ENTER)
   time.sleep(1)
   return

#Выбрать статус мероприятия в ЕКП
def status_sport():
   filter_button('мероприятия')
   driver.implicitly_wait(30)
   time.sleep(1)
   driver.find_element(By.XPATH, "//div[contains(text(),'Статус мероприятия')]").click()
   time.sleep(2)
   driver.implicitly_wait(35)
   status = driver.find_element(By.XPATH, 
      "//body/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/app-event-status[1]/div[1]/form[1]/div[2]/div[1]/ng-select[1]/div[1]/div[1]/div[1]")
   status.click()
   time.sleep(1)
   driver.implicitly_wait(30)
   status = driver.find_element(By.XPATH, "//span[contains(text(),'в ЕКП')]")
   status.click()
   time.sleep(1)
   clearFilter_enter = driver.find_element(By.XPATH, "//button[contains(text(),'Применить')]")
   clearFilter_enter.send_keys(Keys.ENTER)
   time.sleep(1)
   return
#Фильтр соглосование участия
def status_paty():
   filter_button('мероприятия')
   driver.implicitly_wait(30)
   time.sleep(1)
   driver.find_element(By.XPATH, "//div[contains(text(),'Статус участия')]").click()
   time.sleep(1)
   driver.implicitly_wait(35)
   status = driver.find_element(By.XPATH, 
      "//body/div[3]/div[2]/div[1]/div[1]/div[1]/div[2]/app-event-participation-status[1]/div[1]/form[1]/div[2]/div[1]/ng-select[1]/div[1]/span[1]")
   status.click()
   driver.implicitly_wait(30)
   time.sleep(2)
   status = driver.find_element(By.XPATH, "//span[contains(text(),'на согласование')]")
   status.click()
   time.sleep(1)
   clearFilter_enter = driver.find_element(By.XPATH, "//button[contains(text(),'Применить')]")
   clearFilter_enter.send_keys(Keys.ENTER)
   time.sleep(3)


#поиск по номеру
def search_number(x:int, razdel='заявки'):
   driver.implicitly_wait(30)
   if razdel == 'заявки':
      find = driver.find_element(By.XPATH,
         "//app-events-app-section-header/form[1]/div[2]/div[2]/app-search-input[1]/div[1]/input[1]")
   elif razdel == 'мероприятия':
      find = driver.find_element(By.XPATH,  
         "//app-events-section-header/form[1]/div[2]/div[2]/app-search-input[1]/div[1]/input[1]")
   find.clear()
   time.sleep(1)
   find.send_keys(x, Keys.RETURN)
   find.clear()
   time.sleep(1)
   find.send_keys(x, Keys.RETURN)
   time.sleep(3)
   driver.implicitly_wait(30)
   return

#развернуть окно мероприятия
def expand_event():
   driver.implicitly_wait(30)
   driver.find_element(By.XPATH, "//datatable-body-cell/div[1]/div[1]/img[1]").click()
   driver.implicitly_wait(30)
   driver.find_element(By.XPATH, "//div[contains(text(),'Развернуть')]").click()
   time.sleep(1)
   return

#Выбрать статус заявки
def agree_event(name_agree, comment=''):
   driver.implicitly_wait(30)           
   driver.find_element(By.XPATH, 
      "//body/app-root[1]/app-sections[1]/app-events-section-card[1]/div[1]/app-card[1]/div[1]/div[1]/div[1]/a[2]/span[1]").click()
   driver.implicitly_wait(30)
   coordination = driver.find_element(By.XPATH, 
      "//body/div[3]/div[2]/div[1]/mat-dialog-container[1]/app-events-section-modal-edit-app-status[1]/app-modal-container[1]/div[1]/div[2]/form[1]/div[1]/ng-select[1]/div[1]/div[1]/div[2]/input[1]")
   coordination.click()
   driver.implicitly_wait(10)
   coordination.find_element(By.XPATH, f"//span[contains(text(),'{name_agree}')]").click()
   driver.implicitly_wait(10)
   element = driver.find_element(By.XPATH, "//body/div[3]/div[2]/div[1]/mat-dialog-container[1]/app-events-section-modal-edit-app-status[1]/app-modal-container[1]/div[1]/div[2]/form[1]/div[2]/textarea[1]")
   element.click()
   element.send_keys(comment)
   """
   if driver.find_element(By.XPATH, '//*[@formcontrolname="archiveDate"]'):
      element = driver.find_element(By.XPATH, '//*[@formcontrolname="archiveDate"]')
      current_date = datetime.now().strftime("%d.%m.%Y")
      element.click()
      element.send_keys(current_date)
      #element.send_keys(Keys.ENTER)
      driver.implicitly_wait(30)
      time.sleep(2)
      element = driver.find_element(By.XPATH, '//body/div[3]/div[2]/div[1]/mat-dialog-container[1]/app-events-section-modal-edit-app-status[1]/app-modal-container[1]/div[1]/div[2]/form[1]/div[7]/ng-select[1]/div[1]/div[1]/div[2]/input[1]')
      element.click()
      element.send_keys(comment)
      element.send_keys(Keys.ENTER)
   else:
      pass
   """
   end_coordination = driver.find_element(By.XPATH, "//button[contains(text(),'Сохранить')]")
   end_coordination.send_keys(Keys.ENTER)
   time.sleep(1)
   return


#Возврат в меню поиска
def back_list_main():
   back_event = driver.find_element(By.XPATH, "//body/div[@id='main-container']/a[1]")
   back_event.send_keys(Keys.ENTER)



#Соглосование участия
def agree_paty():
   driver.find_element(By.XPATH, "//mat-tab-header/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]").click()
   time.sleep(5)
   driver.implicitly_wait(50)
   elements_button = driver.find_elements(By.CLASS_NAME, "mat-menu-trigger")
   #elements_button = driver.find_elements(By.CSS_SELECTOR, "span.icon-hamburger_outline")
   elements_text = driver.find_elements(By.XPATH, "//tbody[@class='ng-star-inserted']")
   print(len(elements_button))
   text =''
   for i in elements_text:
      text += i.text +"\n"
   pattern = re.compile(r'\(утверждена\)|\(на согласование\)|\(проект\)|\(архив\)')
   #values_in_brackets = re.findall(r'\((.*?)\)', text)
   values_in_brackets =re.findall(pattern, text)
   result_list = []
   for idx, value in enumerate(values_in_brackets, 0):
      print(idx, value)
      if value == '(на согласование)':
         result_list.append(idx)
      else:
         pass
   print(result_list, ' Это список согла!')
   time.sleep(2)
   #Дальше сделать отдельной функццией!
   for el_status in result_list:
      driver.execute_script("window.scrollTo(0, 5000)")
      time.sleep(1)
      driver.implicitly_wait(50)
      print(el_status)
      elements_button[el_status].click()
      #el_status.click()
      button = driver.find_element(By.LINK_TEXT,'Редактировать статус участия')
      button.click()
      driver.implicitly_wait(30)
      input_status = driver.find_element(By.XPATH, '//input[@aria-autocomplete="list"]')
      print('Элемент найден!')
      driver.implicitly_wait(55)
      time.sleep(2)
      try:
         input_status.click()
         time.sleep(1)
         try:
            accept = driver.find_element(By.XPATH, "//span[contains(text(),'утверждена')]")
            accept.click()
            time.sleep(1)
            driver.implicitly_wait(15)
            accept = driver.find_element(By.XPATH, "//button[contains(text(),'Сохранить')]")
            accept.click()
            print('Участие соглосованно')
         except:
            cancel = driver.find_element(By.XPATH, "//button[contains(text(),'Отменить')]")
            cancel.click()
            pass
      except:
         print(el_status, ' Ошибка соглосования элемента!')
         pass
   return


#Изменения основного раздела
def fix_razdel(name_razdel:str):
   element = driver.find_element(By.XPATH, '/html[1]/body[1]/app-root[1]/app-sections[1]/app-events-section-card[1]/div[1]/app-card[1]/div[1]/mat-tab-group[1]/div[1]/mat-tab-body[1]/div[1]/div[1]/app-events-section-card-info[1]/div[1]/h5[1]/span[1]')
   element.click()
   driver.implicitly_wait(30)
   time.sleep(2)
   razdel = driver.find_element(By.XPATH, '//body/div[3]/div[2]/div[1]/mat-dialog-container[1]/app-events-section-modal-edit-calendar[1]/app-modal-container[1]/div[1]/div[2]/form[1]/div[2]/ng-select[1]/div[1]/div[1]/div[3]/input[1]')
   razdel.click()
   razdel.send_keys(name_razdel)
   razdel.send_keys(Keys.ENTER)
   time.sleep(2)
   end_coordination = driver.find_element(By.XPATH, "//button[contains(text(),'Сохранить')]")
   end_coordination.send_keys(Keys.ENTER)
   return



#Список проход по каждому мероприятию для соглосования или отклонения!
def list_application(df, fun_name:str, razdel, name_agree=None):
   for index, row in df.iterrows():
      i = int(row['Реестр №'])
      comment = str(row['IASControl'])
      print(f'{index} из {df.iloc[-1].name}')
      print('===', i, '===')
      hrefList = []
      search_number(i, razdel)
      try:
         expand_event()
         handles = driver.window_handles
         driver.switch_to.window(handles[1])
         time.sleep(5)
         try:
            if fun_name == 'agree_event':
               agree_event(name_agree, comment)
            elif fun_name == 'fix_razdel':
               fix_razdel(name_agree)
            elif fun_name == 'agree_paty':
               agree_paty()
            else:
               print('Не верно указано имя функции')
            time.sleep(3)
            driver.close()
            driver.switch_to.window(handles[0])
         except:
            nan_application.append(i)
            print(i, 'Ошибка функции')
            time.sleep(1)
            driver.implicitly_wait(30)
            driver.close()
            driver.switch_to.window(handles[0])
      except:
         nan_application.append(i)
         print(i, 'Мероприятие не найдено')
         pass
   driver.close()
