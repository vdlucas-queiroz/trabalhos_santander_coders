'''
Projeto - Lógica de Programção II Python - Ada Tech / Santander Coders 2023
Alunos: Fernanda Beatriz Jordan Rojas Dallaqua / Vinícius D'Lucas Bezerra e Queiroz
Turma 1006 - Prof. Igor Garcia
'''

'''
   main_app.py
   
   Código que é executado pela API para calculadora compra vs aluguel imóvel.
   A API recebe requisições pelo método POST, executa diferentes funções de validação dos parâmetros de entrada, retornando ao usuário (lado cliente) mensagens de erro para o caso de parâmetros inválidos. Caso os parâmetros sejam válidos, são executadas funções que calculam os montantes obtidos mês a mês para cada opção de imóvel, retornando um dicionário ao usuário que informa qual a melhor opção, além dos valores finais. 
'''

from typing import Tuple, Union
from fastapi import Body, Request, FastAPI, HTTPException

app = FastAPI()

#####VARIÁVEIS GLOBAIS#############
TEMPO_ANALISE       = 20 #20 anos 
CHAVES_OBRIGATORIAS = ('aluguel', 'montante', 'valorizacao_imovel', 'juros_aluguel', 'juros_aplicacao')
CHAVES_POSITIVAS    = tuple()+CHAVES_OBRIGATORIAS 
CHAVES_DUAS_CASAS   = ('aluguel', 'montante')
TOKEN               = '830f111g-f26h-33f2-ab5e-c8fde68e204a'
###################################

def validar_chaves(entrada: dict) -> Tuple[int,dict]:
    '''
        Função para validar se todas as chaves necessárias pela API estão presentes na entrada. 
        
        Parâmetro:
            - entrada: dicionário com chaves e valores dados pelo usuário
            
        Saída:
            - valor inteiro 0 (chaves faltantes) ou 1 (chaves necessárias estão presentes na entrada)
            - dicionário com mensagem de erro (quais chaves estão faltando) ou com mensagem de sucesso     
    '''
    
    chaves_faltantes = [x for x in CHAVES_OBRIGATORIAS if x not in entrada.keys()]
    if len(chaves_faltantes) > 0:
        mensagem_erro = dict()
        mensagem_erro["Sem sucesso"] = "Falta(m) dado(s) de entrada(s)"
        for count, chave_faltante in enumerate(chaves_faltantes,1):
            mensagem_erro[count] = chave_faltante
        return 0, mensagem_erro
        
    return 1, {"Sucesso":"entrada possui todas as chaves necessarias"} 
    
def validar_tipos(entrada: dict) -> Tuple[int,dict]:
    '''
        Função para validar se os tipos dos valores de entrada estão de acordo com o que a API espera. A API espera receber valores ou do tipo int ou do tipo float.
        
        Parâmetro:
            - entrada: dicionário com chaves e valores dados pelo usuário
            
        Saída:
            - valor inteiro 0 (valores de tipos errados) ou 1 (todos os valores são int ou float)
            - dicionário com mensagem de erro (quais chaves possuem valores de tipos errados e quais são esses tipos) ou com mensagem de sucesso          
    '''
    
    erros_tipo_dado = []    
    for chave in CHAVES_OBRIGATORIAS:
        tipo_entrada = type(entrada[chave]) 
        if tipo_entrada != float and tipo_entrada != int:
            erros_tipo_dado.append((chave,str(tipo_entrada)))
    if len(erros_tipo_dado) > 0:
        mensagem_erro = dict()
        mensagem_erro["Sem sucesso"] = "Dado(s) de tipo errado. Devem ser float ou int"
        for chave_erro,tipo in erros_tipo_dado:
            mensagem_erro[chave_erro] = tipo.split('\'')[1]
        return 0, mensagem_erro
        
    return 1, {"Sucesso":"entrada possui todos os valores com tipos corretos"}
    
def validar_valores(entrada:dict) -> Tuple[int,dict]:
    '''
        Função para validar se certos campos possuem, como esperado, valores positivos.
        
        Parâmetro:
            - entrada: dicionário com chaves e valores dados pelo usuário
            
        Saída:
            - valor inteiro 0 (chaves com valores negativos) ou 1 (valores que devem ser positivos são positivos)
            - dicionário com mensagem de erro (quais chaves possuem valores negativos) ou com mensagem de sucesso          
    '''
    
    erros_valores = []
    for chave in CHAVES_POSITIVAS:
        if entrada[chave] < 0:
            erros_valores.append(chave)
    if len(erros_valores) > 0:
        mensagem_erro = dict()
        mensagem_erro["Sem sucesso"] = "Valor(es) negativo(s). Deve(m) ser positivo(s)"
        for count, chave_erro in enumerate(erros_valores,1):
            mensagem_erro[count] = chave_erro
        return 0, mensagem_erro
        
    return 1, {"Sucesso":"entrada possui valores válidos"}  
    
def validar_casas_decimais(entrada:dict) -> Tuple[int,dict]:
    '''
        Função para validar se campos monetários possuem até duas casas decimais.
        
        Parâmetro:
            - entrada: dicionário com chaves e valores dados pelo usuário
            
        Saída:
            - valor inteiro 0 (chaves monetárias com mais de duas casas decimais) ou 1 (chaves monetárias com até duas casas decimais)
            - dicionário com mensagem de erro (quais chaves possuem mais de duas casas decimais) ou com mensagem de sucesso          
    '''
    
    erros_casas = []
    for chave in CHAVES_DUAS_CASAS:
        aux = str(entrada[chave]).split('.')
        if len(aux) > 1:
            if len(aux[1]) > 2:
                erros_casas.append(chave)
    if len(erros_casas) > 0:
        mensagem_erro = dict()
        mensagem_erro["Sem sucesso"] = "Valor(es) em reais com mais de duas casas decimais"
        for count, chave_erro in enumerate(erros_casas,1):
            mensagem_erro[count] = chave_erro
        return 0, mensagem_erro
      
    return 1, {"Sucesso":"valores em reais possuem duas casas decimais"}                         

def validar_entrada(entrada: any) -> Tuple[int,dict]:
    '''
        Função que verifica se a entrada está de acordo com o esperado pela API.
        Primeiro é verificado se a entrada é um dicionário. Se não for retorna 0 e um dicionário informando que a entrada esperada deve ser do tipo dict.
        Depois são executadas as funções validar_chaves, validar_tipos, validar_valores e validar_casas_decimais. Se em algumas dessas funções houver retorno 0, validar_entrada retorna 0 e a mensagem de erro dada pela função. Se nenhuma dessas funções retornar 0, validar_entrada retorna 1 e mensagem de sucesso, indicando que a entrada está de acordo com o esperado pela API.
        Parâmetro:
            - entrada:    pode ser um dado de qualquer tipo (any)
            
        Saídas:
            - valor inteiro 0 para entrada inválida, 1 para entrada válida
            - dicionário com mensagem de erro ou mensagem de sucesso        
    '''
    tipo_entrada = type(entrada)
    if tipo_entrada != dict:
        tipo_entrada = str(tipo_entrada).split('\'')[1]
        return 0,{"Sem sucesso": f"Tipo inválido de entrada ({tipo_entrada}). Deve ser do tipo dict"}
    
    flag_chaves, mensagem_chaves = validar_chaves(entrada)
    if flag_chaves == 0:
        return flag_chaves, mensagem_chaves
    
    flag_tipos, mensagem_tipos = validar_tipos(entrada)
    if flag_tipos == 0:
        return flag_tipos, mensagem_tipos
        
    flag_valores, mensagem_valores = validar_valores(entrada)
    if flag_valores == 0:
        return flag_valores, mensagem_valores 
        
    flag_casas, mensagem_casas = validar_casas_decimais(entrada)
    if flag_casas == 0:
        return flag_casas, mensagem_casas               
                     
    return 1, {"Sucesso":"chaves e valores estão no padrão correto"}

#Cálculos opção aluguel
def calc_opcao_aluguel(aluguel: float, montante: float, jur_aluguel: float, jur_aplicacao_anual: float) -> Tuple[list,list,list]:
    '''
        Função que calcula os montantes com a opção aluguel mês a mês.
        No primeiro mês não há ganho de rendimentos da aplicação e nem cobrança de aluguel. Depois, a cada mês temos a cobrança do aluguel a partir do valor que o investimento rendeu em cima do montante atual. O que sobra é somado ao montante atual.
        
        Parâmetros:
            - aluguel:              valor do aluguel
            - montante:             valor do montante que o usuário possui atualmente
            - jur_aluguel:          taxa de juros do aluguel (valor do aluguel atualiza uma vez ao ano)
            - jur_aplicacao_anual:  taxa de juros da aplicação (a.a)
            
        Saídas:
            - montante_lista:       montante mês a mês
            - rendimento_lista:     quanto investimento rendeu mês a mês
            - aluguel_lista:        valor pago em aluguel mês a mês    
    '''
    
    montante_lista = [montante]
    rendimento_lista = [0]
    aluguel_lista = [0]
    
    jur_aplicacao = ((1+jur_aplicacao_anual)**(1/12)-1) # Transformando juros anuais em mensal (juros compostos)

    for mes in range(1,TEMPO_ANALISE*12):
        if mes%12 == 0:
            aluguel += aluguel * jur_aluguel
        aluguel_lista.append(aluguel)
        
        rendimento_mes = (montante * jur_aplicacao)
        rendimento_lista.append(rendimento_mes)
        
        ganho_opcao_aluguel = rendimento_mes - aluguel
        
        montante            = montante + ganho_opcao_aluguel
        montante_lista.append(montante)
        
    return montante_lista, rendimento_lista, aluguel_lista  
            
def calc_opcao_compra(montante: float, val_imovel_anual: float) -> list:
    '''
        Função que calcula os montantes com a opção compra mês a mês.
        No primeiro mês não há valorização do imóvel. O montante atual será incrementado da valorização mensal do imóvel.
        
        Parâmetros:
            - montante:          valor do montante que o usuário possui atualmente (valor do imóvel)
            - val_imovel_anual:  valorização do imóvel (a.a)
            
        Saídas:
            - montante_lista:       montante mês a mês     
    '''
    
    montante_lista = [montante]

    val_imovel = ((1+val_imovel_anual)**(1/12)-1) # Transformando juros anuais em mensal (juros compostos)
    
    for mes in range(1,TEMPO_ANALISE*12):
        ganho_opcao_compra = montante * val_imovel
        
        montante           = montante + ganho_opcao_compra
        montante_lista.append(montante)

    return montante_lista 
    
def escolhe_opcao_vantajosa(montante_opcao_aluguel: list, montante_opcao_compra: list) -> list:
    '''
        Função que constrói uma lista com as opções que ganham a cada mês.
        
        Parâmetros:
            - montante_opcao_aluguel: lista com os montantes mensais da opção aluguel
            - montante_opcao_compra:  lista com os montantes mensais da opção compra
            
        Saída:
            - opcao_vantajosa:        lista com a opção mais vantajosa mês a mês    
    '''
    opcao_vantajosa = []

    for aluguel, compra in zip(montante_opcao_aluguel,montante_opcao_compra):
        if aluguel > compra:
            opcao_vantajosa.append("aluguel")
        elif compra > aluguel:
            opcao_vantajosa.append("compra")
        else:
            opcao_vantajosa.append("ambos")    

    return opcao_vantajosa 
    
def get_ponto_turnover(opcao_mes_a_mes: list) -> Union[str,int]:
    '''
        Função que encontra o ponto de turnover em uma lista. Percorre a lista, comparando o elemento atual com o elemento anterior, guardando o índice em uma lista quando esses elementos diferem. Se a lista resultante não tiver elementos, significa que todos os elementos são iguais. Se tiver elementos, retorna o mês do turnover mais recente.  
        
        Parâmetros:
            - opcao_mes_a_mes: lista com a opção mais vantajosa mês a mês
            
        Saída:
            - "Nao ha ponto de turnover" para o caso em que não foi encontrado ponto de turnover em opcao_mes_a_mes
            - mês em que ocorreu o turnover  
    '''
    
    turnover = []
    #começa pelo índice 2 pois opcao_mes_a_mes[0] será "ambos", uma vez que o primeiro mês não tem cobrança de aluguel, nem rendimento em aplicação e nem valorização do imóvel
    for i in range(2,len(opcao_mes_a_mes)):
        if opcao_mes_a_mes[i] != opcao_mes_a_mes[i-1]:
            turnover.append(i) 
        
    if len(turnover) == 0:
        return 'Nao ha ponto de turnover'
    
    return turnover[-1] + 1                                  
            
def app_imovel(entrada: dict) -> dict:
    '''
        Função que calcula os valores finais das opções compra e aluguel, bem como o valor pago em aluguel, informando qual a melhor opção após um TEMPO_ANALISE de anos e se existe ponto de turnover.
        
        Parâmetros:
            - entrada:    dicionário com chaves e valores válidos dados pelo usuário
            
        Saída:
            - dict_saida: dicionário com os parâmetros de entrada fornecidos pelo usuário e a saída da API, que informa os valores finais das opções aluguel e compra, o valor total de aluguel pago em TEMPO_ANALISE anos, qual a melhor opção de investimento após esses anos e se ocorreu turnover    
    '''
    
    aluguel       = entrada["aluguel"] 
    montante      = entrada["montante"]
    val_imovel    = entrada["valorizacao_imovel"] / 100.0
    jur_aluguel   = entrada["juros_aluguel"] / 100.0
    jur_aplicacao = entrada["juros_aplicacao"] / 100.0
    
    montante_aluguel, rendimentos, alugueis = calc_opcao_aluguel(aluguel, montante, jur_aluguel, jur_aplicacao)
    montante_compra                         = calc_opcao_compra(montante, val_imovel)
    
    opcao_mes_a_mes  = escolhe_opcao_vantajosa(montante_aluguel, montante_compra)
    opcao_final      = opcao_mes_a_mes[-1]
    mes_turnover     = get_ponto_turnover(opcao_mes_a_mes)
    
    
    valor_final_opcao_aluguel = '{:.2f}'.format(montante_aluguel[-1])
    valor_final_opcao_aluguel = float(valor_final_opcao_aluguel) 
    valor_pago_aluguel        = '{:.2f}'.format(sum(alugueis))
    valor_pago_aluguel        = float(valor_pago_aluguel)
    valor_final_opcao_compra  = '{:.2f}'.format(montante_compra[-1])
    valor_final_opcao_compra  = float(valor_final_opcao_compra) 
    
    #APENAS PARA DEBUGGAR, NÃO É RETORNADO AO USUÁRIO
    print('ALUGUEIS')
    print(alugueis)
    print(sum(alugueis))
    #print('RENDIMENTOS')
    #print(rendimentos)
    #print(sum(rendimentos))
    print('IMOVEL')
    print(montante_compra)
    print('MONTANTE_INVESTIMENTO')
    print(montante_aluguel)
    print('OPCAO_MES_A_MES')
    print(opcao_mes_a_mes)
    ##################################################
    
    campo_melhor_opcao = f'Melhor Opcao apos {TEMPO_ANALISE} anos'
    
    dict_saida    = {
      "Dados de entrada":{
          "Aluguel":                                 aluguel,
          "Valor Inicial Imovel":                    montante,
          "Valorizacao do Imovel (a.a)":             entrada["valorizacao_imovel"],
          "Juros aluguel (a.a)":                     entrada["juros_aluguel"],
          "Juros aplicacao (a.a)":                   entrada["juros_aplicacao"]
                                            
      },
      "Saida API":{
          "Valor Final Opcao Aluguel":               valor_final_opcao_aluguel,
          "Valor Final Opcao Compra":                valor_final_opcao_compra,
          "Valor Final Pago (Aluguel)":              valor_pago_aluguel,
          campo_melhor_opcao:                        opcao_final,
          "Mes de turnover":                         mes_turnover
      }
    } 
    
    return dict_saida
    
def validar_token(token_requisicao: str) -> bool:
    '''
        Função para validar se token da requisição do usuário é válido. 
        
        Parâmetro:
            - entrada: string com token da requisição
            
        Saída:
            - True se o token da requisição for válido
            - Erro de exceção 401 do HTTP se o token da requisição não for válido. Será retornado ao usuário o dicionário {'detail': 'Usuario nao autorizado'}. 
    '''
        
    if token_requisicao == TOKEN:
        return True
    raise HTTPException(
        status_code = 401,
        detail="Usuario nao autorizado"
    )
    return False
    
@app.post("/appimovel")
async def get_body(request: Request) -> dict:
    '''
        Função da API que recebe uma requisição do usuário (lado cliente), executa procedimentos de validação dessa requisição e se validada, executa a função de calculadora compra vs aluguel imóvel (app_imovel).
        
        Parâmetros:
            - request:          requisição do usuário, que contém o token de acesso e os parâmetros de entrada para a calculadora
            
        Saída:
            - mensagem_entrada: dicionário com mensagem de erro retornada quando algum(ns) parâmetro(s) do usuário é(são) inválido(s)
            - saida_app_imovel: dicionário com a saída da função de calculadora compra vs aluguel imóvel (app_imovel)   
    '''
    
    entrada    = await request.json()
    token      = request.headers.get('authorization')
    flag_token = validar_token(token)
          
    flag_entrada, mensagem_entrada = validar_entrada(entrada)
    if flag_entrada == 0:
        return mensagem_entrada
    
    saida_app_imovel = app_imovel(entrada)    
    
    return saida_app_imovel
