from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify(message="Ola, mundo!"), 200

@app.route('/senai', methods=['GET'])
def senai():
    return jsonify(message="Ola, senai!"), 200

# endpoint - pesquisar endereço através do cep, retorna em formato json
@app.route('/pesquisacep/<cep>', methods=['GET'])
def pesquisacep(cep):

    url = f"https://viacep.com.br/ws/{cep}/json/"
    resposta = requests.get(url)
    return resposta.json()

@app.route('/search-city/<city>', methods=['GET'])
def searchcity(city):

    key = "c4380707dde242f4b78202712252204&q"
    url = f"https://api.weatherapi.com/v1/current.json?key={key}={city}&lang=pt"
    resposta = requests.get(url)
    result   = resposta.json()

    temperatura = result['current']['temp_c']
    umidade     = result['current']['humidity']

    return render_template("paginatempo.html",
    temp=temperatura, umid=umidade, city=city)

if __name__ == '__main__':
    app.run(debug=True)
