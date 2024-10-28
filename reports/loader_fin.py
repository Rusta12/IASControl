import time
from settings.config import *


url_report_fin = "https://ias.sport.mos.ru/Reports/ReportViewer.aspx?report_name=CompetitionCalendarSchoolSportFinans&report_param_backUrl=http://ias.sport.mos.ru"

# Вход в отчет
def come_fin_report(name, pass_name):
   #Вход в ИАС
   driver.get(url_report_fin)
   driver.implicitly_wait(30)
   login = driver.find_element(By.XPATH, "//input[@id='UserName']")
   login.send_keys(name)
   pas = driver.find_element(By.XPATH, "//input[@id='Password']")
   pas.send_keys(pass_name, Keys.RETURN)
   time.sleep(4)
   return


def calendar_period(period):
    time.sleep(1)
    select_element = driver.find_element(By.XPATH,"//select[@id='rvMain_ctl04_ctl03_ddValue']")
    select_element.send_keys(Keys.ENTER)
    driver.implicitly_wait(3)
    select = Select(select_element)
    for option in select.options:
        if period in option.text:
            select.select_by_visible_text(option.text)
            print(f"Выбрана опция: {option.text}")
            break







def CalendarSchoolSportFinans(period, status):
    come_fin_report(login_b, pass_b)
    calendar_load(period, status)
