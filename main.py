from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
# # from selenium.webdriver.common.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

# Replace these with your camera's details
camera_url = "http://192.168.1.143/"
username = "admin"
password = "ObstructionDetection123"
name_format = "%y%M%d%h%m%s_%14_%09"

options = Options()
options.add_experimental_option("detach", True)
# options.add_argument("window-size=1200x600")
options.add_argument("start-maximized");
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
# Set preferences for automatic multiple downloads
prefs = {
    "download.default_directory": "C:\\Users\\HomePC\\Desktop\\obstruction\\server\\observer\\plate_numbers",
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    'profile.default_content_setting_values.automatic_downloads': 1
}
options.add_experimental_option("prefs", prefs)

service = Service(executable_path="chromedriver.exe")
# Start the browser (you need to have the WebDriver executable in your PATH)
driver = webdriver.Chrome(service=service, options=options)

# Open the camera login page
driver.get(f"{camera_url}")
# driver.get('https://www.google.com/')

wait = WebDriverWait(driver, 5)

def wait_keys(by, selector, keys, clear = False):
    wait.until(EC.presence_of_all_elements_located((by, selector)))
    if clear:
        driver.find_element(by, selector).send_keys(Keys.CONTROL,"a");
        driver.find_element(by, selector).send_keys(Keys.DELETE);
    
    driver.find_element(by, selector).send_keys(keys)

def wait_click(by, selector):
    wait.until(EC.element_to_be_clickable((by, selector)))
    driver.find_element(by, selector).click()

def wait_click_xpath(attr):
    wait_click(By.XPATH, f'//*[@{attr}]')

def sure_click(full_xpath: str):
    wait.until(EC.presence_of_all_elements_located((By.XPATH, full_xpath)))
    driver.execute_script(f"""
        var xpath = "{full_xpath}";
        var element = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        if (element) element.click();
    """)

#! LOGIN
wait_keys(By.ID, "login_user", username)
wait_keys(By.ID, "login_psw", password)
wait_keys(By.ID, "login_psw", Keys.RETURN)

#! UPDATE SETTINGS
wait_click_xpath('data-for="set"')
wait_click_xpath('category="storage"')
wait_click_xpath('t="sto.Storage"')
wait_click_xpath('data-for="storepath"')
wait_keys(By.ID, "store_inp_snapname", name_format, clear=True)
sure_click("/html/body/div[2]/div[2]/div[5]/div[1]/div[2]/div/div[2]/div/div[5]/div[1]/div[4]/a[3]")
sleep(1)
wait_click_xpath('data-for="preview"')
sleep(10)
while True:
    wait_click(By.ID, 'b_manusnap')
    sleep(30)







# You may need to add a delay here to wait for the login to complete
# For example: driver.implicitly_wait(10)  # 10 seconds

# After login, you can perform additional actions as needed

# Close the browser when done
# driver.quit()
# while True:
#     pass