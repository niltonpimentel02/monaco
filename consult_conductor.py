import os
from selenium import webdriver
from time import sleep, time
from selenium.webdriver.common.keys import Keys
from pprint import pprint as pp
from twocaptcha import TwoCaptcha
from decouple import config
from collections import OrderedDict

try:
    browser = webdriver.Firefox(executable_path='C:\Webdrivers\geckodriver.exe')

    browser.maximize_window()

    sleep(1)

    url = 'http://consultas.detrannet.sc.gov.br/servicos/ConsultaPontuacaoCondutor.asp'
    browser.get(url=url)

    sleep(1)

    """
    Download captcha image
    """
    captcha_photo = browser.find_element_by_xpath('//img[@id="imgDesafio"]')

    sleep(2)

    captcha_photo.screenshot('img.png')

    """
    Solve captcha
    """
    solver = TwoCaptcha(config('2_CAPCHA_API_KEY'))
    result = solver.normal('img.png')
    result_code = result['code']

    """
    Delete photo downloaded above
    """
    if os.path.exists('img.png'):
        os.remove('img.png')
        print('The file was deleted successfully')
    else:
        print('The file does not exist')

    sleep(1)

    cpf = config('CPF')
    registro = config('REGISTRO')
    codigo = result_code

    sleep(1)

    cpf_field = browser.find_element_by_name('txtDocPrincipal').send_keys(cpf)
    registro_field = browser.find_element_by_name('txtDocCNH').send_keys(registro)
    codigo_field = browser.find_element_by_name('txtCodigo').send_keys(codigo)
    browser.find_element_by_xpath('//input[@name="btnConsultar"]').click()

    sleep(1)

    data = browser.find_elements_by_xpath('//tr[@width="100%"]')

    content = OrderedDict(
        data_time=data[0].text,
        data_conductor=data[1].text,
        data_conductor_name=data[2].text,
    )

    pp('========================================================================')
    pp(content)
    pp('========================================================================')
    pp(type(content))
    pp('========================================================================')

    """
    WIP - Work In Progress
    """
    data_detail = browser.find_elements_by_xpath('//*[@id="divDadosPontuacao"]/table[2]/tbody/tr')
    for elements in data_detail:
        print(elements.text)

    browser.save_screenshot(str(round(time() * 1000)) + ".png")

    browser.quit()

except:
    print('========================================================================')
    print('There was a problem with the server! Try again in a few moments, please!')
    print('========================================================================')
