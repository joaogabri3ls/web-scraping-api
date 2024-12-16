from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_espn_news(url: str):
    service = Service("D:\\chromedriver-win64\\chromedriver.exe")
    options = Options()
    options.add_argument("--headless")  # Executa o navegador em modo headless
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=service, options=options)

    try:
        print("Acessando a URL...")
        driver.get(url)

        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "contentItem"))
            )
        except TimeoutException:
            print("Tempo de espera excedido. O conteúdo não foi carregado.")
            return pd.DataFrame()

        time.sleep(5)
        print("Extraindo conteúdo da página...")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        news = []

        for item in soup.select('.contentItem'):
            title = item.select_one('.contentItem__title')
            summary = item.select_one('.contentItem__subhead')
            date = item.select_one('.contentMeta__timestamp')
            link = item.select_one('a')

            news.append({
                "title": title.text.strip() if title else None,
                "summary": summary.text.strip() if summary else None,
                "date": date.text.strip() if date else None,
                "link": f"https://www.espn.com.br{link['href']}" if link and link.get('href') else None
            })

        print(f"Coletadas {len(news)} notícias.")
    finally:
        driver.quit()

    df = pd.DataFrame(news)
    print("Dados organizados com sucesso.")
    return df

if __name__ == "__main__":
    url = "https://www.espn.com.br/futebol/"
    df = scrape_espn_news(url)

    if not df.empty:
        print(df.head())  # Exibe as primeiras linhas para validação
        df.to_csv("espn_news.csv", index=False)  # Salva os dados em CSV
        print("Dados salvos em 'espn_news.csv'.")
    else:
        print("Nenhum dado foi extraído.")
