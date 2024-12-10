from flask import Flask, render_template, request, redirect, url_for
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_spider', methods=['POST'])
def run_spider():
    # Run the Scrapy spider
    subprocess.run(['python', 'test.py'], cwd='/app/myproject/spiders')
    return redirect(url_for('index'))

@app.route('/show_results', methods=['POST'])
def show_results():
    # Read the contents of the text file
    file_path = '/app/myproject/spiders/bcbsla_webscraping_links.txt'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    else:
        content = "No results found."
    return render_template('results.html', content=content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
