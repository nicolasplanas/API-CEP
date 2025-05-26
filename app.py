from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

# endpoint - página principal do projeto
@app.route('/')
def hello():
    return render_template('home.html')

# endpoint - pesquisa de endereço através do cep
@app.route('/cep', methods=['GET', 'POST'])
def pesquisacep():

    if   request.method == 'GET':
        return render_template("paginacep.html")
    
    elif request.method == 'POST':
        cep      = request.form['cep']
        url      = f"https://viacep.com.br/ws/{cep}/json/"
        resposta = requests.get(url).json()
        if "erro" in resposta:
            return render_template("paginacep.html", erro=True)
        
        return render_template("paginacep.html", **resposta)

# endpoint - pesquisa de previsão do tempo
@app.route('/tempo', methods=['GET', 'POST'])
def tempo():

    if   request.method == 'GET':
        return render_template("paginatempo.html")
 
    elif request.method == 'POST':
        cidade = request.form.get('cidade')

        if not cidade or cidade == "Nenhum":
            return render_template("paginatempo.html", erro=True)
        
        result = get_tempo(cidade)
        return render_template("paginatempo.html", **result)
    
# função - retorna a previsão do tempo para o endpoint
def get_tempo(cidade):

    key    = "c4380707dde242f4b78202712252204"
    url    = f"https://api.weatherapi.com/v1/current.json?key={key}&q={cidade}&lang=pt"
    result = requests.get(url).json()

    return {"temperatura" : result["current"]["temp_c"],
            "umidade"     : result["current"]["humidity"],
            "velvento"    : result["current"]["vis_km"],
            "pressaoatim" : result["current"]["pressure_mb"],
            "cidade"      : result["location"]["name"],
            "regiao"      : result["location"]["region"],
            "localhora"   : result["location"]["localtime"],
            "pais"        : result["location"]["country"]}

# inicia o app
if __name__ == '__main__':
    app.run(debug=True)
