import os
import re
import json
import traceback
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.options import Options

class Bradesco:
  BASE_PATH = 'https://www.ne12.bradesconetempresa.b.br/ibpjlogin/login.jsf'
  cnpj = []

  with open('config.json', 'r') as json_file:
    dados = json.load(json_file)
    
  path = dados['path']
  path2 = dados['path2']
  iterator_lista_contas = 0


  def __init__(self):
    self.username = self.dados['bradesco_download_extrato_username']
    self.passwd = self.dados['bradesco_download_extrato_password']
    
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')

    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", self.path)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
    "text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml")
    fp.set_preference("pdfjs.disabled", True)
    self.driver = webdriver.Firefox(options=options, executable_path=r'./geckodriver', firefox_profile=fp)
    self.wait = WebDriverWait(self.driver, 60)

  def auth(self):
    self.driver.get(self.BASE_PATH)
    self.driver.find_element_by_id('identificationForm:txtUsuario').send_keys(self.username)
    self.driver.find_element_by_id('identificationForm:txtSenha').send_keys(self.passwd)
    self.driver.find_element_by_id('identificationForm:botaoAvancar').click()
    sleep(2)

    print("Login Efetuado")

    self._remove_home_modal()
    self.get_extratos()

  def _remove_home_modal(self):
    sleep(1)
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
    print("Download iniciado ......")    

    for row in rows:
      ## Abre a conta
      row.click()

      ## Abre o extrato
      extrato = self.wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="formSaldos:listagemContaCorrente:_id162:'+str(self.iterator_lista_contas)+':listaContasEmpresa:_id221:0:linhaContaSaldo"]/tr[1]'))
      )
      self.driver.execute_script("arguments[0].scrollIntoView(true);", extrato)
      
      soup = BeautifulSoup(extrato.text, 'html.parser')
      soupString = str(soup).split(' ')
      soupStringT = soupString[0]+ ' ' + soupString[1]+ ' ' + soupString[2]
      extrato = self.wait.until(
        EC.element_to_be_clickable((By.XPATH, '//td[.="'+ soupStringT +'"]'))
      )
      extrato.click()

      ## Clica no botão de salvar
      self.wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="formSaldos:listagemContaCorrente:_id162:'+str(self.iterator_lista_contas)+':listaContasEmpresa:_id221:0:linhaContaSaldo"]/tr[2]/td/div[3]/div/ul/li[2]/a'))
      ).click()

      ## Troca o frame
      self.driver.switch_to.default_content()
      self.wait.until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, 'modal_infra_estrutura'))
      )

      ## Clica no botão de salvar CSV
      self.wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="formSalvarComo:cvs"]'))
      ).click()

      sleep(1)
      self.rename() 

      ## Clica no botão de fechar o frame
      self.wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="_id29"]'))
      ).click()

      ## Troca o frame
      self.driver.switch_to.default_content()

      self.wait.until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, 'paginaCentral'))
      )

      ## Resolve o bug do Firefox
      extrato.click()
      row.click()

      # Itera linha da tabela
      self.iterator_lista_contas += 1

    print("Donwload Finalizado")
    sleep(3)
    self.driver.switch_to.default_content()
    sleep(3)
    self.driver.switch_to.default_content()
    sleep(3)
    self.wait.until(
      EC.element_to_be_clickable((By.XPATH, '//*[@id="botaoSair"]'))
    ).click()
    sleep(3)
    print('Bot Finalizado')
    self.driver.close()

  def rename(self):    
    for filename in os.listdir(self.path):      
      x = "".join(re.findall("\\d+", self.cnpj[self.iterator_lista_contas]))
      new_file_name = 'bradesco_saldo_investimento_'+x[1:]+'.csv' 
      try:
        os.rename(os.path.join(self.path, filename),
            os.path.join(self.path2, new_file_name))
      except Exception as e :
        traceback.format_exc(e)
      print(new_file_name)                    
      break

invest = Bradesco()
invest.auth()