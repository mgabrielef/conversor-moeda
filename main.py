from flask import Flask, render_template, request
import requests
from dicionario import *


app = Flask(__name__, template_folder='templates', static_folder='static')

#moeda = 0

@app.route('/')
def index():
    return render_template('index.html', len=len(lista), lista=lista)

@app.route('/converter', methods=['GET','POST'])
def converter():
    suaMoeda = request.form.get("select")
    moedaConvert = request.form.get("select2")

    moedaEscolhida = options_dict[suaMoeda]
    moedaConversao = options_dict[moedaConvert]


    requisicao = requests.get(f'https://economia.awesomeapi.com.br/all/{moedaEscolhida}-{moedaConversao}')
    
    cotacao = requisicao.json()
    try:
        moeda = float(cotacao[moedaEscolhida]['bid'])
        moeda = round(moeda, 2)
        nomeMoeda = cotacao[moedaEscolhida]['name']
        nomeMoeda = nomeMoeda.replace('/',' para ')
        data = cotacao[moedaEscolhida]['create_date']
            
        valor = float(request.form.get("valor"))
            
        resultado = moeda * valor
        resultado = round(resultado, 2)
        return render_template("converter.html", nomeMoeda=nomeMoeda, data=data,resultado=resultado,moeda=moeda, len=len(lista), lista=lista)
    except:
        return render_template("converter.html", len=len(lista), lista=lista)
  

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)