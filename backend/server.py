import requests
from flask import Flask, request, jsonify, render_template
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

def get_page_load_time(url):
    try:
        response = requests.get(url)
        return response.elapsed.total_seconds()
    except Exception as e:
        print(f"Erro ao obter tempo de carregamento: {e}")
        return None

def get_main_keywords(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        text = soup.get_text()
        words = re.findall(r'\b\w+\b', text.lower())
        word_count = {}
        for word in words:
            if len(word) > 3:  # considerando apenas palavras com mais de 3 caracteres
                word_count[word] = word_count.get(word, 0) + 1
        sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        return sorted_words[:5]  # retornar as 5 palavras mais frequentes
    except Exception as e:
        print(f"Erro ao obter palavras-chave principais: {e}")
        return None

def check_mobile_compatibility(html_content):
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        meta_viewport = soup.find('meta', attrs={'name': 'viewport'})
        if meta_viewport and 'width=device-width' in meta_viewport.get('content', ''):
            return True
        return False
    except Exception as e:
        print(f"Erro ao verificar compatibilidade móvel: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/seo', methods=['GET'])
def get_seo_data():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL não fornecida'})

    try:
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({'error': f'Erro ao acessar URL: Código de status {response.status_code}'})

        page_load_time = get_page_load_time(url)
        main_keywords = get_main_keywords(response.content)
        mobile_compatible = check_mobile_compatibility(response.content)

        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else 'N/A'
        description = soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else 'N/A'
        links = soup.find_all('a')
        total_links = len(links)
        internal_links = sum(1 for link in links if url in link.get('href', ''))
        external_links = total_links - internal_links

        seo_data = {
            'url': url,
            'title': title,
            'description': description,
            'links': {
                'total': total_links,
                'internal': internal_links,
                'external': external_links
            },
            'page_load_time': page_load_time,
            'main_keywords': main_keywords,
            'mobile_compatible': mobile_compatible,
        }

        return jsonify(seo_data)

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
