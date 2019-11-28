from selenium import webdriver
options = webdriver.ChromeOptions()

options.add_argument("--start-maximized") #maximize_window
browser = webdriver.Chrome(chrome_options=options)
browser.get('https://www.irctc.co.in/nget/train-search')

logInBtn = browser.find_element_by_id("loginText").click()
