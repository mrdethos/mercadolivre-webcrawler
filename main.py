import json
import threading
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Anuncio:
    def __init__(self, nome, vendedor, preco_atual, preco_anterior, desconto, link_imagem):
        self.nome = nome
        self.vendedor = vendedor
        self.preco_atual = preco_atual
        self.preco_anterior = preco_anterior
        self.desconto = desconto
        self.link_imagem = link_imagem


def get_anuncio_data(anuncio):
    '''
    Extrai os dados dos anúncios, localizando-os pelo css_selector
    Alguns dados podem não estar presentes nos anúncios, podendo ser substituídos por "N/A"
    '''
    # Obtém o preço atual do anúncio
    try:
        preco_atual = anuncio.find_element_by_css_selector(
            '.andes-money-amount-combo__main-container .andes-money-amount__fraction').text
    except:
        preco_atual = "N/A"

    # Obtém o preço anterior do anúncio
    try:
        preco_anterior = anuncio.find_element_by_css_selector(
            '.andes-money-amount-combo__previous-value .andes-money-amount__fraction').text
    except:
        preco_anterior = "N/A"

    # Obtém o nome do anúncio
    nome = anuncio.find_element_by_css_selector('.promotion-item__title').text

    # Obtém o desconto do anúncio
    try:
        desconto = anuncio.find_element_by_css_selector(
            '.andes-money-amount__discount').text
    except:
        desconto = "N/A"

    # Obtém o vendedor do anúncio
    vendedor_elementos = anuncio.find_elements_by_css_selector(
        '.promotion-item__seller')
    if len(vendedor_elementos) > 0:
        vendedor = fix_vendedor(vendedor_elementos[0].text)
    else:
        vendedor = "N/A"

    return nome, vendedor, preco_atual, preco_anterior, desconto


def fix_vendedor(vendedor):
    '''
    Retira o trecho "por" da string de vendedor
    '''
    return vendedor.replace("por ", "")


def scroll_anuncio(driver, element):
    '''
    Rola apenas para o próximo anúncio visível
    '''
    driver.execute_script("arguments[0].scrollIntoView();", element)


def collect_anuncios(anuncios, anuncios_lista, driver):
    '''
    Coleta os dados dos anúncios e os adiciona à lista de anúncios
    Utiliza um bloqueio para evitar condições de corrida durante a atualização da lista de anúncios
    '''
    for i, anuncio in enumerate(anuncios):
        # Obtém os dados do anúncio
        nome, vendedor, preco_atual, preco_anterior, desconto = get_anuncio_data(
            anuncio)

        # Para evitar adicionar o link da imagem codificada como base64, é necessário rolar a página até o trecho do anúncio, fazendo com que a url inteira da imagem carregue
        if i < len(anuncios) - 1:
            proximo_anuncio = anuncios[i+1]
            scroll_anuncio(driver, proximo_anuncio)

        # Obtém o link da imagem do anúncio
        link_imagem = WebDriverWait(anuncio, 5).until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '.promotion-item__img'))).get_attribute("src")

        # Cria um objeto Anuncio com os dados coletados
        anuncio_obj = Anuncio(nome, vendedor, preco_atual,
                              preco_anterior, desconto, link_imagem)

        # Adquire um bloqueio para evitar condições de corrida durante a atualização da lista de anúncios
        lock.acquire()
        anuncios_lista.append(anuncio_obj)
        lock.release()


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get('https://www.mercadolivre.com.br/ofertas')

anuncios_lista = []
lock = threading.Lock()

start_time = time.time()

while True:
    # Seleção de todos os anúncios da página atual
    anuncios_container = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.items_container')))
    anuncios = anuncios_container.find_elements_by_css_selector(
        '.promotion-item')

    # Divide a lista de anúncios em duas partes
    mid = len(anuncios) // 2
    anuncios1 = anuncios[:mid]
    anuncios2 = anuncios[mid:]

    # Cria as threads para coletar os dados dos anúncios (cada thread ficará com metade da lista de anúncios)
    thread1 = threading.Thread(target=collect_anuncios, args=(
        anuncios1, anuncios_lista, driver))
    thread2 = threading.Thread(target=collect_anuncios, args=(
        anuncios2, anuncios_lista, driver))

    # Inicia as threads
    thread1.start()
    thread2.start()

    # Aguarda a conclusão das threads
    thread1.join()
    thread2.join()

    # Lida com a paginação
    botao_proxima = driver.find_element_by_css_selector(
        '.andes-pagination__button--next')

    # Caso o botão de próxima página esteja desabilitado, o programa sai do while
    if 'andes-pagination__button--disabled' in botao_proxima.get_attribute('class'):
        break
    else:
        link_proxima_pagina = botao_proxima.find_element_by_tag_name(
            'a').get_attribute('href')
        driver.get(link_proxima_pagina)

end_time = time.time()
execution_time = end_time - start_time

driver.quit()

# Exportação dos dados para um arquivo .JSON
with open('anuncios.json', 'w') as file:
    json.dump([anuncio.__dict__ for anuncio in anuncios_lista], file)

print("Programa finalizado. Tempo de execução:",
      round(execution_time, 2), "segundos")
