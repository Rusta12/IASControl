import time
from settings.config import *


url_report_fin = "https://ias.sport.mos.ru/Reports/ReportViewer.aspx?report_name=CompetitionCalendarSchoolSportFinans&report_param_backUrl=http://ias.sport.mos.ru"

def calendar_fin_report(name, pass_name):
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


def calendar_razdel(razdel='6. Учреждения Москомспорта (раздел для подведомственных организаций)'):
    while True:
        try:
            time.sleep(1)
            driver.implicitly_wait(5)
            # Кликаем на поле подраздела календаря
            select_element =  driver.find_element(By.XPATH,"//select[@id='rvMain_ctl04_ctl07_ddValue']")
            select_element.send_keys(Keys.ENTER)
            driver.implicitly_wait(3)
            select = Select(select_element)
            for option in select.options:
                if razdel in option.text:
                    select.select_by_visible_text(option.text)
                    print(f"Выбрана опция: {option.text}")
                    break

            time.sleep(1)
            break
        except:
            pass


def calendar_status(status=None):
    if status:
        driver.find_element(By.XPATH,"//input[@id='rvMain_ctl04_ctl09_txtValue']").click()
        driver.implicitly_wait(3)
        driver.find_element(By.XPATH,f"//label[contains(text(),'{status}')]").click()
    else:
        return
    
    
def calendar_typefin(typefin=None):
    if typefin:
        driver.find_element(By.XPATH,"//input[@id='rvMain_ctl04_ctl13_txtValue']").click()
        time.sleep(1)
        # Кликаем по чекбоксу через JavaScript
        checkbox = driver.find_element(By.ID, "rvMain_ctl04_ctl13_divDropDown_ctl00")
        driver.execute_script("arguments[0].click();", checkbox)
        driver.implicitly_wait(10)
        driver.find_element(By.XPATH,f"//label[contains(text(),'{typefin}')]").click()
    else:
        return


def calendar_reload():
    # Запуск просмотра отчета!
    time.sleep(1)
    button_up = driver.find_element(By.XPATH, "//input[@id='rvMain_ctl04_ctl00']")
    button_up.send_keys(Keys.ENTER)

    while True: #Цикл загрузки файла после ожидания отображения.
        try:
            time.sleep(5)
            driver.implicitly_wait(5)
            driver.find_element(By.XPATH, "//img[@id='rvMain_ctl06_ctl04_ctl00_ButtonImg']").click()
            time.sleep(1)
            driver.implicitly_wait(1)
            driver.find_element(By.XPATH, "//a[contains(text(),'CSV (с разделителями-запятыми)')]").click()
            break
        except:
            pass


def CalendarSchoolSportFinans(period, razdel, status=None, typefin=None):
    calendar_fin_report(login_b, pass_b)
    calendar_period(period)
    calendar_razdel(razdel)
    calendar_status(status)
    calendar_typefin(typefin)
    calendar_reload()
    driver.close()
    return
