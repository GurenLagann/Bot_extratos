# -*- coding: utf-8 -*-
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import os
import re

class Bradesco:
  BASE_PATH = 'https://www.ne12.bradesconetempresa.b.br/ibpjlogin/login.jsf'
  cnpj = []
  path = '/home/wallace/Downloads'
  path2 = '/home/wallace/Extratos'
  iteratorListaContas = 0


  def __init__(self):
    self.username = 'LMI00542'
    self.passwd = '32458998'

    self.driver =  webdriver.Chrome(executable_path=r'./chromedriver')
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
      ## Abre a conta
      row.click()

      ## Abre o extrato
      self.wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="formSaldos:listagemContaCorrente:_id162:'+str(self.iteratorListaContas)+':listaContasEmpresa:_id221:0:linhaContaSaldo"]/tr[1]'))
      ).click()

      ## Clica no botão de salvar
      self.wait.until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="formSaldos:listagemContaCorrente:_id162:'+str(self.iteratorListaContas)+':listaContasEmpresa:_id221:0:linhaContaSaldo"]/tr[2]/td/div[3]/div/ul/li[2]/a'))
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

      # Troca o frame
      self.driver.switch_to.default_content()

      self.wait.until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, 'paginaCentral'))
      )  
      
      # Itera linha da tabela
      self.iteratorListaContas += 1

    self.driver.switch_to.default_content()
    self.driver.find_element_by_xpath('//*[@id="botaoSair"]').click()
    sleep(5)
    self.driver.close()

  def rename(self):    
    for filename in os.listdir(self.path):      
      x = self.cnpj[self.iteratorListaContas].split("/")
      new_file_name = 'saldo_investimento_'+x[0]+'.'+x[1]+'.csv'
      try:
        os.rename(os.path.join(self.path, filename),
            os.path.join(self.path2, new_file_name))
                
      except Exception:
        print(Exception)                    
      break

invest = Bradesco()
invest.auth()