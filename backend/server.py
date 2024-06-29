from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Rota para obter dados da API do Meta SEO Inspector
@app.route('/api/seo')
def get_seo_data():
    url = request.args.get('url')
    api_url = f'https://www.metaseoapi.com/api/meta?url={url}'
    response = requests.get(api_url)
    data = response.json()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
