import json
import requests

url = 'http://localhost:8000/appimovel'
headers = {
  'authorization': '830f111g-f26h-33f2-ab5e-c8fde68e204a'
}

def teste_token_errado():
    
    #token de autorização errado
    headers_errado = {
       'authorization': '831g111h-f26h-33f1-ab5e-c8fde68e204a'
    }

    payload = {
                "aluguel":            300,
                "montante":           500000,
                "valorizacao_imovel": 1.5,
                "juros_aluguel":      5,
                "juros_aplicacao":    0.5
              }
    response = requests.request("POST", url, headers=headers_errado, json=payload)
    print(response.json()) #{'detail': 'Usuario nao autorizado'}
    
    #sem token de autorização
    payload = {
                "aluguel":            300,
                "montante":           500000,
                "valorizacao_imovel": 1.5,
                "juros_aluguel":      5,
                "juros_aplicacao":    0.5
              }
    response = requests.request("POST", url, json=payload)
    print(response.json()) #{'detail': 'Usuario nao autorizado'}

def testes_input_tipo_errado():

    #input do tipo str
    payload = json.dumps({
                "aluguel":            300,
                "montante":           500000,
                "valorizacao_imovel": 1.5,
                "juros_aluguel":      5,
                "juros_aplicacao":    0.5
              })
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.json())  #{'Sem sucesso': 'Tipo inválido de entrada (str). Deve ser do tipo dict'}        
    
    #input do tipo list
    payload = [300, 500000, 1.5, 5, 0.5]
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.json()) #{'Sem sucesso': 'Tipo inválido de entrada (list). Deve ser do tipo dict'}
                        
    #input do tipo tuple
    payload = ( ("aluguel",300), ("montante",500000), ("valorizacao_imovel",1.5), ("juros_aluguel",5), ("juros_aplicacao",0.5) )
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.json()) #função da api transforma em lista de listas #{'Sem sucesso': 'Tipo inválido de entrada (list). Deve ser do tipo dict'} 
    
def testes_chaves_faltantes():

    payload = {
                "montante":           500000,
                "valorizacao_imovel": 1.5,
                "juros_aluguel":      5,
                "juros_aplicacao":    0.5
              }
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.json()) #{'Sem sucesso': 'Falta(m) dado(s) de entrada(s)', '1': 'aluguel'}                   
              
    payload = {
                "aluguel":            300,
                "valorizacao_imovel": 1.5,
                "juros_aluguel":      5,
                "juros_aplicacao":    0.5
              }
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.json()) #{'Sem sucesso': 'Falta(m) dado(s) de entrada(s)', '1': 'montante'}         
              
    payload = {
                "aluguel":            300,
                "montante":           500000,
                "juros_aluguel":      5,
                "juros_aplicacao":    0.5
              }
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.json())  #{'Sem sucesso': 'Falta(m) dado(s) de entrada(s)', '1': 'valorizacao_imovel'}        
              
    payload = {
                "aluguel":            300,
                "montante":           500000,
                "valorizacao_imovel": 1.5,
                "juros_aplicacao":    0.5
              }
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.json()) #{'Sem sucesso': 'Falta(m) dado(s) de entrada(s)', '1': 'juros_aluguel'}         
              
    payload = {
                "aluguel":            300,
                "montante":           500000,
                "valorizacao_imovel": 1.5,
                "juros_aluguel":      5
              }
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.json()) #{'Sem sucesso': 'Falta(m) dado(s) de entrada(s)', '1': 'juros_aplicacao'}         
              
    payload = {
                "ALUGUEL":            300,
                "montante":           500000,
                "juros_aplicacao":    0.5
              }
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.json()) #{'Sem sucesso': 'Falta(m) dado(s) de entrada(s)', '1': 'aluguel', '2': 'valorizacao_imovel', '3': 'juros_aluguel'}
    
def testes_valores_tipo_errado():

    payload = {
                "aluguel":            "300",
                "montante":           500000,
                "valorizacao_imovel": {"valor": 1.5},
                "juros_aluguel":      [5],
                "juros_aplicacao":    0.5
              } 
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.json())  #{'Sem sucesso': 'Dado(s) de tipo errado. Devem ser float ou int', 'aluguel': 'str', 'valorizacao_imovel': 'dict', 'juros_aluguel': 'list'}                                                                      

def testes_valores_range_errado():

    payload = {
                "aluguel":            -300,
                "montante":           500000,
                "valorizacao_imovel": -1.5,
                "juros_aluguel":      5,
                "juros_aplicacao":    0.5
              } 
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.json()) #{'Sem sucesso': 'Valor(es) negativos. Devem ser positivos', '1': 'aluguel', '2': 'valorizacao_imovel'}
    
    payload = {
                "aluguel":            300,
                "montante":           -500000,
                "valorizacao_imovel": 1.5,
                "juros_aluguel":      -5,
                "juros_aplicacao":    0.5
              } 
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.json()) #{'Sem sucesso': 'Valor(es) negativos. Devem ser positivos', '1': 'montante', '2': 'juros_aluguel'}
    
def testes_casas_decimais_errado():

    payload = {
                "aluguel":            300.078,
                "montante":           500000,
                "valorizacao_imovel": 1.5,
                "juros_aluguel":      5,
                "juros_aplicacao":    0.5
              } 
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.json()) #{'Sem sucesso': 'Valor(es) em reais com mais de duas casas decimais', '1': 'aluguel'}
    
    payload = {
                "aluguel":            300,
                "montante":           500000.0759,
                "valorizacao_imovel": 1.5,
                "juros_aluguel":      5,
                "juros_aplicacao":    0.5
              } 
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.json()) #{'Sem sucesso': 'Valor(es) em reais com mais de duas casas decimais', '1': 'montante'}  
    
def testes_validacao_input(): 
    '''
        Função que executa funções que testam a validação dos parâmetros de entrada.
    '''  
    teste_token_errado()
    testes_input_tipo_errado()
    testes_chaves_faltantes()
    testes_valores_tipo_errado()
    testes_valores_range_errado()
    testes_casas_decimais_errado()

def testes_app_imovel(aluguel: float,montante: float, valorizacao_imovel: float, juros_aluguel: float, juros_aplicacao:float) -> None:
    '''
        Função para auxiliar testes da calculadora de compra vs aluguel imóvel. Recebe os parâmetros que deverão ser enviados à API, as insere em um dicionário, que é enviado como parâmetro à uma requisição do tipo POST de uma dada url e que possui headers com token de autorização.
        O dicionário retornado pela API é printado na tela em um formato pretty json.
        
        Parâmetros:
            - aluguel:            valor do aluguel mensal
            - montante:           valor do imóvel
            - valorizacao_imovel: valorização do imóvel ao ano
            - juros_aluguel:      taxa de juros do aluguel ao ano
            - juros_aplicacao:    taxa de juros da aplicação ao ano   
    '''

    payload = {
                "aluguel":            aluguel,
                "montante":           montante,
                "valorizacao_imovel": valorizacao_imovel,
                "juros_aluguel":      juros_aluguel,
                "juros_aplicacao":    juros_aplicacao
              }
    URL = 'http://localhost:8000/appimovel'
    HEADERS = {
                "authorization": "830f111g-f26h-33f2-ab5e-c8fde68e204a"
              }           
    response = requests.request("POST", URL, headers=HEADERS, json=payload)
    print(json.dumps(response.json(),indent=2))
    
if __name__ == "__main__":
    #testes_validacao_input()
    #testes_app_imovel(1500.00,300000.00,5,7.5,12.68)
    #testes_app_imovel(1500,300000,5,10,10)
    #testes_app_imovel(1500,300000,5,10,12.68)
    #testes_app_imovel(1500.00,3000000.00,5,7.5,12.68)
    testes_app_imovel(10000.00,3000000.00,5,7.5,12.68)






