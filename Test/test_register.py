# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestLogin():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_login(self):
    self.driver.get("http://localhost:8082/")
    self.driver.set_window_size(1382, 744)
    self.driver.find_element(By.CSS_SELECTOR, ".profile-dropdown img").click()
    self.driver.find_element(By.LINK_TEXT, "Logout").click()
    self.driver.find_element(By.LINK_TEXT, "Sign up").click()
    self.driver.find_element(By.NAME, "username").click()
    self.driver.find_element(By.NAME, "username").send_keys("Ram")
    self.driver.find_element(By.NAME, "email").click()
    self.driver.find_element(By.NAME, "email").send_keys("ram@gmail.com")
    self.driver.find_element(By.ID, "password1").click()
    self.driver.find_element(By.ID, "password1").send_keys("ram123")
    self.driver.find_element(By.ID, "password2").click()
    self.driver.find_element(By.ID, "password2").send_keys("ram123")
    self.driver.find_element(By.CSS_SELECTOR, "button").click()
  
