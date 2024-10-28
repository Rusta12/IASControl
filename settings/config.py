from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
import dotenv

dotenv.load_dotenv(".env")

login_b = os.getenv('LOGIN_B')
pass_b = os.getenv('PASS_B')
login_a = os.getenv('LOGIN_A')
pass_a = os.getenv('PASS_A')


options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
   "download.default_directory": r"C:\DataIAS",
   "download.prompt_for_download": False,
   "download.directory_upgrade": True,
   "safebrowsing.enabled": True
})

service = Service(executable_path='C:\DataIAS\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

