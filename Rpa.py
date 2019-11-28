# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class Rpa(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_rpa(self):
        driver = self.driver
        driver.get("https://159.65.157.226/lazy/submit-online/terafast")
        driver.find_element_by_xpath("//input[@type='text']").click()
        driver.find_element_by_xpath("//input[@type='text']").clear()
        driver.find_element_by_xpath("//input[@type='text']").send_keys("David")
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='*'])[2]/following::span[3]").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='ui-btn'])[1]/following::select[2]").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='ui-btn'])[1]/following::select[1]").click()
        driver.find_element_by_link_text("12").click()
        driver.find_element_by_xpath("//div[@id='ui-panel-0-content']/div/div/div[3]/div[2]/p-dropdown/div/div[2]/span").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Male'])[1]/following::li[1]").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='*'])[4]/following::label[1]").click()
        driver.find_element_by_xpath("(.//*[normalize-space(text()) and normalize-space(.)='Choose Marital Status'])[1]/following::li[1]").click()
        driver.find_element_by_xpath("(//input[@type='text'])[6]").click()
        driver.find_element_by_xpath("(//input[@type='text'])[6]").clear()
        driver.find_element_by_xpath("(//input[@type='text'])[6]").send_keys("fg")
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
