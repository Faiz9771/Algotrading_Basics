from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


ticker = "AAPL"

# Chrome options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

# Setup driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = f"https://finance.yahoo.com/quote/{ticker}/financials"
driver.get(url)
driver.implicitly_wait(2)

table = driver.find_element(By.XPATH,"//div[@class='table yf-yuwun0']").text


income_st_dir={}
table_heading = driver.find_elements(By.XPATH,"//*[contains(@class, 'column yf-1yyu1pc')]")
row = driver.find_elements(By.XPATH,"//*[@class = 'row lv-0 yf-t22klz']")
headings = []
for cell in table_heading:
    headings.append(cell.text)
    
for cell in row:
    parts = cell.text.split("\n")
    key = parts[0]
    income_st_dir[key] = parts[1:]


    
buttons = driver.find_elements(By.XPATH,"//article[@class='yf-eeqr8j']//button")
for button in buttons:
    print(button.accessible_name)
    if button.accessible_name in ["Annual", "Quarterly", "Expand All"]:
        pass
    else:
        WebDriverWait(driver,2).until(EC.element_to_be_clickable(button)).click()

income_st_dir={}
table_heading = driver.find_elements(By.XPATH,"//*[contains(@class, 'column yf-1yyu1pc')]")
row = driver.find_elements(By.XPATH,"//*[@class = 'row lv-0 yf-t22klz']")
headings = []
for cell in table_heading:
    headings.append(cell.text)
    
for cell in row:
    parts = cell.text.split("\n")
    key = parts[0]
    income_st_dir[key] = parts[1:]
    

