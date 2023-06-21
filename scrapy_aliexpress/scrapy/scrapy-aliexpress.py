import scrapy
import logging
from pprint import pprint

from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


# Desativa o log do Scrapy
logging.getLogger('scrapy').setLevel(logging.WARNING)

# Contador de produtos:
quantidade_de_produtos_processados = 0

def decorador_produtos(metodo):
    """."""
    def anuncio_produtos(self, html):
        """."""
        print('=' * 50)
        print(' ' * 20, 'A-Z Express', ' ' * 19)
        print('=' * 50)
        print()
        metodo(self, html)
    return anuncio_produtos


CATEGORIA = [
    'https://pt.aliexpress.com/category/201001892/men-clothing.html?CatId=201001892&category_redirect=1&g=y&isCategoryBrowse=true&isFavorite=y&isrefine=y&sortType=total_tranpro_desc&spm=a2g0o.home.102.1.75ee1c91dMBDON&trafficChannel=ppc&page=',
    'https://pt.aliexpress.com/category/201001900/women-clothing.html?CatId=201001900&category_redirect=1&g=y&isCategoryBrowse=true&isFavorite=y&isrefine=y&sortType=total_tranpro_desc&spm=a2g0o.home.101.1.229a1c91Vjcfys&trafficChannel=ppc&page=',
    'https://pt.aliexpress.com/category/201000020/consumer-electronics.html?CatId=201000020&category_redirect=1&g=y&isCategoryBrowse=true&isFavorite=y&isrefine=y&sortType=total_tranpro_desc&spm=a2g0o.home.105.1.16ea1c91ePYWUn&trafficChannel=ppc&page='
]


class ProdutosAliExpressSpider(scrapy.Spider):
    """."""
    name = 'ProdutosAliExpress'
    start_urls  = [
        f'{url}{pagina}'
        for pagina in range(1, 2)
        for url in CATEGORIA
    ]


    def parse(self, response):
        PRODUTO_XPATH = response.xpath('//*[@id="card-list"]/a')
        for produto in PRODUTO_XPATH:
            print()
            print(response)
            print()
            print()
            URL_PRODUTO_XPAH = produto.css('a::attr(href)').get()

            yield self.parse_produto(URL_PRODUTO_XPAH)

    
    def parse_produto(self, response):
        """."""
        chrome = self.acessa_chrome(response)
        html_do_produto = self.retornar_html_do_produto(chrome)
        
        while True:
            DESCRICAO_PRODUTO = self.retorna_descricao_do_produto(html_do_produto)
            QUANTIDADE_VENDIDA = self.retorna_quantidade_de_produtos_vendidos(html_do_produto)
            PRECO_ANTIGO = self.retorna_preco_antigo_do_produto(html_do_produto)
            print()
            break

        chrome.close()
        sleep(2)


    def acessa_chrome(self, url):
        """."""
        driver = webdriver.Chrome()
        driver.get(f'http:{url}')
        return driver


    def retornar_html_do_produto(self, chrome):
        """."""
        try: 
            div_main = chrome.find_element(By.ID, 'root')
        except: 
            div_main = chrome.find_element(By.CLASS_NAME, 'product-main')

        html_content = div_main.get_attribute('outerHTML')
        html_parser = BeautifulSoup(html_content, 'html.parser')
        return html_parser


    @decorador_produtos
    def retorna_descricao_do_produto(self, html_do_produto):
        """."""
        global quantidade_de_produtos_processados
        quantidade_de_produtos_processados += 1
        print('Quantidade de Itens processados:', quantidade_de_produtos_processados, sep=' ', end='\n')

        try: 
            DESCRIACAO_DO_PRODUTO = html_do_produto.find('div', class_='product-title').get_text()
            print(f'{DESCRIACAO_DO_PRODUTO=}')
            return DESCRIACAO_DO_PRODUTO
        except Exception as e: 
            try:
                DESCRIACAO_DO_PRODUTO = html_do_produto.find('h3', class_='titleBanner--title--1BJltZV').get_text()
                print(f'{DESCRIACAO_DO_PRODUTO=}')
                return DESCRIACAO_DO_PRODUTO
            except Exception as e:
                DESCRIACAO_DO_PRODUTO = html_do_produto.find('div', class_='title--wrap--Ms9Zv4A').get_text()
                print(f'{DESCRIACAO_DO_PRODUTO=}')
                return DESCRIACAO_DO_PRODUTO

            

    def retorna_quantidade_de_produtos_vendidos(self, html_do_produto):
        """."""
        try: 
            QUANTIDADE_VENDIDA = html_do_produto.find('span', class_='product-reviewer-sold').get_text()
            print(f'{QUANTIDADE_VENDIDA=}')
            return QUANTIDADE_VENDIDA
        except Exception as e:
            QUANTIDADE_VENDIDA = 0
            print(f'{QUANTIDADE_VENDIDA=}')
            return QUANTIDADE_VENDIDA


    def retorna_preco_antigo_do_produto(self, html_do_produto):
        """."""
        try: 
            PRECO_ANTIGO = html_do_produto.find('div', class_='product-price-del').get_text()
            print(f'{PRECO_ANTIGO=}')
            return PRECO_ANTIGO
        except Exception as e:
            try:
                PRECO_ANTIGO = html_do_produto.find('span', class_='uniform-banner-box-discounts').get_text(strip=True)
                PRECO_ANTIGO = f'{PRECO_ANTIGO.split(",")[0]},{PRECO_ANTIGO.split(",")[1][:2]}'
                print(f'{PRECO_ANTIGO=}') 
                return PRECO_ANTIGO  
            except Exception as e:  
                PRECO_ANTIGO = html_do_produto.find('span', class_='price--originalText--Zsc6sMv pdp-comp-price-original').get_text()
                print(f'{PRECO_ANTIGO=}')
                return PRECO_ANTIGO

"""



driver = webdriver.Chrome()
driver.get("https://pt.aliexpress.com/item/1005004127052611.html?spm=a2g0o.productlist.main.31.4f1a1f4d0JeS7Y&algo_pvid=c6fc52ed-5e49-4643-a004-24bd1853e2a3&algo_exp_id=c6fc52ed-5e49-4643-a004-24bd1853e2a3-15&pdp_npi=3%40dis%21BRL%21264.01%21132.01%21%21%21%21%21%40211be72e16868659117174600d079b%2112000028124436360%21sea%21BR%210&curPageLogUid=zKmCqxBUJiJ6")
sleep(5)

div_main = driver.find_element(By.CLASS_NAME, 'product-main')
html_content = div_main.get_attribute('outerHTML')
SOUP = BeautifulSoup(html_content, 'html.parser') 
sleep(5)


TITULO = SOUP.find('div', class_='product-title').get_text()
try:
    VENDIDOS = SOUP.find('span', class_='product-reviewer-sold').get_text()
except AttributeError:
    VENDIDOS = '0 Vendidos'

PRECO_ANTIGO = SOUP.find('span', class_='product-price-value').get_text()
DESCONTO = SOUP.find('span', class_='product-price-mark').get_text()
PARCELAS = SOUP.find('div', class_='product-installment-wrap').get_text()
CORES_HTML = list(SOUP.find_all('div', class_='sku-property-image'))

CORES = ''
for cor in CORES_HTML:
   CORES += str(cor).split('title="')[1].split('"')[0] + ','

TAMANHOS_HTML = list(SOUP.find_all('div', class_='sku-property-text'))

TAMANHOS = ''
for tamanho in TAMANHOS_HTML:
   TAMANHOS += str(tamanho).split('<span>')[1].split('</span>')[0] + ','

ITENS_DISPONIVEIS = SOUP.find('div', class_='product-quantity-tip').get_text()
ENVIO = SOUP.find('span', class_='product-delivery-to').get_text()
FRETE = SOUP.find('div', class_='dynamic-shipping-line dynamic-shipping-titleLayout').get_text()
QUEM_ENTREGA = ...
ENTREGA_E_FORNECEDOR = list(SOUP.find_all('div', class_='dynamic-shipping-line dynamic-shipping-contentLayout'))
for tamanho in ENTREGA_E_FORNECEDOR:
    
    if str(tamanho).split(';">')[1].split('</span>')[0].strip() == 'Estimativa de Entrega:':
        ENTREGA = str(tamanho).split(';">')[2].split('</span>')[0]
    else:
        FORNECEDOR = str(tamanho).split(';">')[2].split('</span>')[0]


print(f'{TITULO=}')
print(f'{VENDIDOS=}')
print(f'{PRECO_ANTIGO=}')
print(f'{DESCONTO=}')
print(f'{PARCELAS.strip()=}')
print(f'{CORES=}')
print(f'{TAMANHOS=}')
print(f'{ITENS_DISPONIVEIS=}')
print(f'{ENVIO=}')
print(f'{FRETE=}')
print(f'{ENTREGA=}')
print(f'{FORNECEDOR=}')

div_main = driver.find_element(By.XPATH, '//*[@id="store-info-wrap"]')
html_content = div_main.get_attribute('outerHTML')
SOUPS = BeautifulSoup(html_content, 'html.parser') 

AVALIACAO_DA_LOJA = str(SOUPS.find('div', class_='store-container')).split('<i>')[1].split('</i>')[0]
SEGUIDORES = SOUPS.find('p', class_='num-followers').get_text()


print(f'{AVALIACAO_DA_LOJA=}')
print(f'{SEGUIDORES=}')"""