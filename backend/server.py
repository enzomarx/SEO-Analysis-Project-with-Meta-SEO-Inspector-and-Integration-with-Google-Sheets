from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/seo', methods=['GET'])
def get_seo_data():
    url = request.args.get('url')
    # Aqui você deve implementar a lógica para obter os dados SEO da URL fornecida
    # Exemplo de dados fictícios para teste:
    seo_data = {
        'url': url,
        'title': 'Título da Página',
        'description': 'Descrição da Página',
        'links': {
            'total': 10,
            'internal': 7,
            'external': 3
        }
    }
    return jsonify(seo_data)

if __name__ == '__main__':
    app.run(debug=True)
