import os
import shutil
import requests
from pprint import pprint as pp
from twocaptcha import TwoCaptcha
from datetime import datetime
from decouple import config

# Create a link for captcha image based on real
datetime_now = datetime.now()
datetime_now_timestamp = datetime.timestamp(datetime_now)
datetime_now_timestamp_str = str(datetime_now_timestamp)
datetime_now_timestamp_value = datetime_now_timestamp_str[:14].replace('.', '')

# Download captcha image
url = f'http://consultas.detrannet.sc.gov.br/Servicos/BitMap.asp?{datetime_now_timestamp_value}'
response = requests.get(url, stream=True)
with open('img.png', 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
del response

# Solve captcha
solver = TwoCaptcha(config('2_CAPCHA_API_KEY'))
result = solver.normal('img.png')
result_code = result['code']

# Delete photo downloaded above
if os.path.exists("img.png"):
  os.remove("img.png")
else:
  pp("The file does not exist")

# Post on page
payload = {'txtDocPrincipal': '04601616956', 'txtDocCNH': '03951668042', 'txtCodigo': f'{result_code}'}
r = requests.post('http://consultas.detrannet.sc.gov.br/servicos/ConsultaPontuacaoCondutor.asp', data=payload)

# if 'CONSULTA PONTUAÇÃO' not in r.text:
#     pp('Texto não encontrado')
# else:
#     pp('Texto encontrado! Ok!!')

if 'É necessário informar o código.' not in r.text:
    pp('Texto não encontrado')
else:
    pp('Texto encontrado! Ok!!')
