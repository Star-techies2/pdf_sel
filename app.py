from flask import Flask, render_template, request, redirect, url_for
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

app = Flask(__name__)
PDF_LINKS_FILE = 'pdf_links.txt'
DOWNLOAD_FOLDER = './downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Path to the ChromeDriver executable
CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'  # Update this path

# Function to extract PDF links using Selenium in headless mode
def extract_pdf_links():
    service = Service(executable_path=CHROMEDRIVER_PATH)
    options = Options()
    options.add_argument('--headless')
    options.headless = True
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://providers.bcbsla.com/resources/professional-provider-office-manual-24')  # Replace with the URL you want to scrape
    pdf_links = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
    with open(PDF_LINKS_FILE, 'w') as file:
        for link in pdf_links:
            file.write(link.get_attribute('href') + '\n')
    driver.quit()

# Function to read PDF links
def read_pdf_links():
    if os.path.exists(PDF_LINKS_FILE):
        with open(PDF_LINKS_FILE, 'r') as file:
            pdf_urls = file.readlines()
        return [link.strip() for link in pdf_urls]
    return []

# Function to delete PDF links
def delete_pdf_links():
    if os.path.exists(PDF_LINKS_FILE):
        os.remove(PDF_LINKS_FILE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract_pdfs', methods=['POST'])
def extract_pdfs():
    extract_pdf_links()
    return redirect(url_for('index'))

@app.route('/show_pdfs', methods=['POST'])
def show_pdfs():
    pdf_links = read_pdf_links()
    return render_template('show_pdfs.html', pdf_links=pdf_links)

@app.route('/delete_pdfs', methods=['POST'])
def delete_pdfs():
    delete_pdf_links()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)