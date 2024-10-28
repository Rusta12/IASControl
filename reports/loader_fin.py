import time
from settings.config import *


# Вход в отчет
def come_fin_report(name, pass_name):
   #Вход в ИАС
   driver.get("https://ias.sport.mos.ru/Reports/ReportViewer.aspx?report_name=CompetitionCalendarSchoolSportFinans&report_param_backUrl=http://ias.sport.mos.ru")
   driver.implicitly_wait(30)
   login = driver.find_element(By.XPATH, "//input[@id='UserName']")
   login.send_keys(name)
   pas = driver.find_element(By.XPATH, "//input[@id='Password']")
   pas.send_keys(pass_name, Keys.RETURN)
   time.sleep(4)
   return


def calendar_load(period, status):
    time.sleep(1)
    kalendar = driver.find_element(By.XPATH,"//select[@id='rvMain_ctl04_ctl03_ddValue']")
    kalendar.send_keys(Keys.ENTER)
    driver.implicitly_wait(3)



def CalendarSchoolSportFinans(period, status):
    come_fin_report(login_b, pass_b)
    calendar_load(period, status)
