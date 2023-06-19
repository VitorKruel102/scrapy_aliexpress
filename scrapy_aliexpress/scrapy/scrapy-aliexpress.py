import scrapy
from bs4 import BeautifulSoup
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class ProdutosAliExpressSpider(scrapy.Spider):
    """."""
    name = 'ProdutosAliExpress'
    start_urls  = [
        f'https://pt.aliexpress.com/category/201001900/women-clothing.html?CatId=201001900&category_redirect=1&g=y&isCategoryBrowse=true&isrefine=y&page={pagina}&sortType=total_tranpro_desc&spm=a2g0o.home.101.1.2e581c91ueQTKU&trafficChannel=ppc'
        for pagina in range(1, 2)
    ]

    def parse(self, response):
        PRODUTO_XPATH = response.xpath('//*[@id="card-list"]/a')
        for produto in PRODUTO_XPATH:
            URL_PRODUTO_XPAH = produto.css('a::attr(href)').get()

            yield self.parse_produto(URL_PRODUTO_XPAH)


    def parse_produto(self, response):
        """."""
        chrome = self.acessa_chrome(response)
        chrome.implicitly_wait(10) # gives an implicit wait for 20 seconds
        html_do_produto = self.retornar_html_do_produto(chrome)
        sleep(20)
        while True:
            try: 
                DESCRIACAO_DO_PRODUTO = html_do_produto.find('div', class_='product-title').get_text()
                print(DESCRIACAO_DO_PRODUTO)
                print()
            except Exception as e: 
                print('Erro')
                try:
                    DESCRIACAO_DO_PRODUTO = html_do_produto.find('h3', class_='titleBanner--title--1BJltZV').get_text()
                    print(DESCRIACAO_DO_PRODUTO)
                    print()
                except:
                    try:
                        print('erro 2')
                        DESCRIACAO_DO_PRODUTO = html_do_produto.find('div', class_='title--wrap--Ms9Zv4A').get_text()
                        print(DESCRIACAO_DO_PRODUTO)
                        print()
                    except:
                        print('erro 3')
                        sleep(1110000000)
                break
            break

        chrome.close()
        sleep(5)


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
        return BeautifulSoup(html_content, 'html.parser') 






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