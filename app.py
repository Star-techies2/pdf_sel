import logging
from flask import Flask, render_template, request, redirect, url_for
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from playwright.sync_api import sync_playwright

app = Flask(__name__)
PDF_LINKS_FILE = 'pdf_links.txt'
DOWNLOAD_FOLDER = '/app/downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Path to the ChromeDriver executable
CHROMEDRIVER_PATH = 'chromedriver.exe'

CHROME_BINARY_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Function to extract PDF links using Selenium in headless mode with specified ChromeDriver path
def extract_pdf_links():
    options = Options()
    options.headless = True  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--headless')  # Ensure headless mode is enabled
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--single-process')
    options.add_argument('--disable-application-cache')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-logging')
    options.add_argument('--log-level=3')
    options.add_argument('--output=/dev/null')
    service = ChromeService(executable_path=CHROMEDRIVER_PATH)
    try:
        logging.debug("Starting ChromeDriver service")
        driver = webdriver.Chrome(service=service, options=options)
        logging.debug("Navigating to the target URL")
        driver.get('https://providers.bcbsla.com/resources/professional-provider-office-manual-24')  # Replace with the URL you want to scrape
        pdf_links = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
        with open(PDF_LINKS_FILE, 'w') as file:
            for link in pdf_links:
                file.write(link.get_attribute('href') + '\n')
        driver.quit()
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise

# Function to extract PDF links using Selenium with ChromeDriverManager
def extract_pdf_links_with_manager():
    options = Options()
    options.headless = True  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--headless')  # Ensure headless mode is enabled
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--single-process')
    options.add_argument('--disable-application-cache')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-logging')
    options.add_argument('--log-level=3')
    options.add_argument('--output=/dev/null')
    try:
        logging.debug("Starting ChromeDriver with ChromeDriverManager")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        logging.debug("Navigating to the target URL")
        driver.get('https://providers.bcbsla.com/resources/professional-provider-office-manual-24')  # Replace with the URL you want to scrape
        pdf_links = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")
        with open(PDF_LINKS_FILE, 'w') as file:
            for link in pdf_links:
                file.write(link.get_attribute('href') + '\n')
        driver.quit()
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise

# Function to extract PDF links using Playwright
def extract_pdf_links_with_playwright():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, executable_path=CHROME_BINARY_PATH)
            page = browser.new_page()
            logging.debug("Navigating to the target URL with Playwright")
            page.goto('https://providers.bcbsla.com/resources/professional-provider-office-manual-24')  # Replace with the URL you want to scrape
            pdf_links = page.locator("//a[contains(@href, '.pdf')]").all()
            with open(PDF_LINKS_FILE, 'w') as file:
                for link in pdf_links:
                    file.write(link.get_attribute('href') + '\n')
            browser.close()
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        raise

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

@app.route('/extract_pdfs_with_manager', methods=['POST'])
def extract_pdfs_with_manager():
    extract_pdf_links_with_manager()
    return redirect(url_for('index'))

@app.route('/extract_pdfs_with_playwright', methods=['POST'])
def extract_pdfs_with_playwright():
    extract_pdf_links_with_playwright()
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
