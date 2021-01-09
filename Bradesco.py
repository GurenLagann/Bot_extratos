from selenium import webdriver
from bs4 import BeautifulSoup
import time

class Bradesco:
  def __init__(self):
    self.driver = webdriver.Firefox(executable_path=r'./geckodriver')
    

  def Login(self):
    self.driver.get('https://www.ne12.bradesconetempresa.b.br/ibpjlogin/login.jsf')
    user = self.driver.find_element_by_id('identificationForm:txtUsuario')
    user.click()
    user.send_keys('LMI00542')
    pwd = self.driver.find_element_by_id('identificationForm:txtSenha')
    pwd.click()
    pwd.send_keys('32458998')
    nxt = self.driver.find_element_by_id('identificationForm:botaoAvancar')
    nxt.click()
    time.sleep(3)
    saldo = self.driver.find_element_by_id('_id73_0:_id75')
    saldo.click()
    time.sleep(5)
    for li_list in self.driver.find_elements_by_class_name('tabindex'):
      for ext in li_list.find_elements_by_xpath('//*[@title="Saldo"]'):
        print(ext)
    # print(li_list[2])
    # li_list[2].location_once_scrolled_into_view
    # li_list[2].click()
      
      #li_list[0].click()
    #ext[5].click()
    # extrato = self.driver.find_elements_by_xpath("//*[contains(text(), 'Saldo')]")
    # print(extrato)
    # extrato[0].click()
   


invest = Bradesco()
invest.Login()

    