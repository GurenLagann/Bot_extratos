from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import re

class Bradesco:
  BASE_PATH = 'https://www.ne12.bradesconetempresa.b.br/ibpjlogin/login.jsf'
  cnpj = []

  def __init__(self):
    self.username = 'LMI00542'
    self.passwd = '32458998'

    # options = webdriver.ChromeOptions()
    # options.add_argument('lang=pt-br')
    self.driver =  webdriver.Chrome(executable_path=r'./chromedriver')
    # self.driver = webdriver.Firefox(executable_path=r'./geckodriver')
    self.wait = WebDriverWait(self.driver, 60)

  def auth(self):
    self.driver.get(self.BASE_PATH)
    self.driver.find_element_by_id('identificationForm:txtUsuario').send_keys('LMI00542')
    self.driver.find_element_by_id('identificationForm:txtSenha').send_keys('32458998')
    self.driver.find_element_by_id('identificationForm:botaoAvancar').click()
    sleep(5)

    self._remove_home_modal()
    self.get_extratos()

  def _remove_home_modal(self):
    sleep(10)
    if len(self.driver.find_elements_by_css_selector('.jqmOverlay')) >= 1:
        self.driver.execute_script('document.querySelector(".jqmOverlay").remove()')

  def get_extratos(self):
    self.wait.until(
        EC.presence_of_element_located((By.XPATH, '//a[.="Saldos e Extratos"]'))
    ).click()
    self.wait.until(
          EC.frame_to_be_available_and_switch_to_it((By.ID, 'paginaCentral'))
    )
    self.wait.until(
      EC.presence_of_element_located((By.XPATH, '//a[.="Saldo"]'))
    ).click()
    table = self.wait.until(
      EC.presence_of_element_located((By.CSS_SELECTOR, '.ne-tabela-expansivel'))
    )
    rows = table.find_elements_by_css_selector('td:nth-child(3)')
    
    num = self.driver.find_elements_by_css_selector('td.nowrap.pl5')    
    for n in num:
      self.cnpj.append(n.text)    

    for row in rows:
      
      row.click()     
      # self.driver.find_element_by_css_selector('td.nowrap.alignRight').click()

      self.wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'td.nowrap.alignRight'))
      ).click()

      self.wait.until(
        EC.presence_of_element_located((By.XPATH, '//a[.="Salvar como arquivo"]'))
      ).click()
      self.driver.switch_to.default_content()
      self.wait.until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, 'modal_infra_estrutura'))
      )

      #Botão de Download
      sleep(5)      
      # self.driver.execute_script("clear_formSalvarComo();document.forms['formSalvarComo'].elements['autoScroll'].value=getScrolling();document.forms['formSalvarComo'].elements['formSalvarComo:_link_hidden_'].value='formSalvarComo:cvs';document.forms['formSalvarComo'].elements['formato'].value='CSV';if(document.forms['formSalvarComo'].onsubmit){if(document.forms['formSalvarComo'].onsubmit()) document.forms['formSalvarComo'].submit();}else{document.forms['formSalvarComo'].submit();}return false;")
      # self.driver.find_element_by_xpath('//a[@id="formSalvarComo:cvs"]').click()
      self.driver.get("https://www.ne12.bradesconetempresa.b.br/ibpjsei/salvarComoArquivoCompleto.jsf")
      sleep(5)
      
      #voltar para tabela
      self.driver.find_element_by_id('formSalvarComo:btnEnviarFechar_X').click()
      self.driver.switch_to.default_content()
      self.wait.until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, 'paginaCentral'))
      )
      
    print(self.cnpj)

invest = Bradesco()
invest.auth()