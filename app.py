from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('home.html')

# endpoint - pesquisar endereço através do cep, retorna em formato json
@app.route('/pesquisacep', methods=['GET', 'POST'])
def pesquisacep():

    if  request.method == 'GET':
        return render_template("paginacep.html")
    
    elif request.method == 'POST':
        cep      = request.form['cep']
        url      = f"https://viacep.com.br/ws/{cep}/json/"
        resposta = requests.get(url).json()
        return render_template("paginacep.html", **resposta)

def get_tempo(cidade):

    key      = "c4380707dde242f4b78202712252204"
    url      = f"https://api.weatherapi.com/v1/current.json?key={key}&q={cidade}&lang=pt"
    result   = requests.get(url).json()

    return {"temperatura" : result["current"]["temp_c"],
            "umidade"     : result["current"]["humidity"],
            "velvento"    : result["current"]["vis_km"],
            "pressaoatim" : result["current"]["pressure_mb"],
            "cidade"      : result["location"]["name"],
            "regiao"      : result["location"]["region"],
            "localhora"   : result["location"]["localtime"],
            "pais"        : result["location"]["country"]}

#retorna a previsão do tempo
@app.route('/tempo', methods=['GET', 'POST'])
def tempo():

    if request.method == 'GET':
        result = get_tempo("São Paulo")
        return render_template("paginatempo.html", **result)

    elif request.method == 'POST':
        cidade = request.form['cidade']
        result = get_tempo(cidade)
        return render_template("paginatempo.html", **result)

if __name__ == '__main__':
    app.run(debug=True)
