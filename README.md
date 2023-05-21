# mercadolivre-webcrawler

Este é um código em Python que coleta dados de anúncios do site Mercado Livre e os salva em um arquivo JSON. O programa utiliza a biblioteca Selenium para automatizar a navegação e extração de informações do site.

## Pré-requisitos
* Python 3.x instalado</br>
* Chromedriver
* Bibliotecas Python:
* * selenium
* * json

## Instalação
1. Faça o download ou clone este repositório em seu ambiente de trabalho.
2. Instale as bibliotecas necessárias usando o comando:
```
pip install selenium json
```
3. Certifique-se de ter o Chrome instalado em sua máquina.
4. Baixe o ChromeDriver compatível com a versão do Chrome instalada em sua máquina. O ChromeDriver pode ser baixado <a href="https://sites.google.com/chromium.org/driver/downloads">aqui</a>.
5. Extraia o arquivo ChromeDriver baixado e coloque-o no mesmo diretório do código fonte, ou nas variáveis do sistema.

## Uso
1. Abra o arquivo main.py em um editor de texto ou ambiente de desenvolvimento Python.
2. Execute o código Python.
3. Aguarde enquanto o programa coleta os dados dos anúncios. O programa irá navegar pelas páginas de ofertas do Mercado Livre e extrair informações como nome, vendedor, preço atual, preço anterior, desconto e link da imagem do anúncio.
4. O arquivo anuncios.json será gerado no mesmo diretório do código fonte, contendo os dados coletados no formato JSON, e o tempo de execução do programa será exibido no console.

## Observações
* O programa utiliza threads para coletar os dados dos anúncios de forma paralela e acelerar o processo. Neste caso, foram utilizadas duas threads para dividir a lista de anúncios e coletar os dados em paralelo. Após testes, verificou-se que o uso de quatro threads não apresentou um impacto relevante na velocidade do programa, por isso optou-se por usar apenas duas threads.
* O programa faz uso do navegador Chrome em modo headless para executar as operações de automação sem abrir uma janela do navegador visível. Se preferir ver a execução em tempo real, você pode remover a opção --headless nas configurações do Chrome.