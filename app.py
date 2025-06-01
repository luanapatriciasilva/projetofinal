from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Importando o módulo de utilidades do dicionário
# Certifique-se de que dicionario_utils.py está no mesmo nível que app.py
from dicionarios_utils import carregar_termos, salvar_termos

# --- INICIALIZAÇÃO DO FLASK (APENAS UMA VEZ!) ---
app = Flask(__name__)

# --- CONFIGURAÇÃO DO GEMINI ---
load_dotenv()
gemini_api_key = os.getenv('GOOGLE_API_KEY')

if not gemini_api_key:
    raise ValueError("A variável de ambiente 'GOOGLE_API_KEY' não está definida. "
                     "Por favor, crie um arquivo .env com sua chave.")

genai.configure(api_key=gemini_api_key)

# Inicializar o modelo Gemini
try:
    model = genai.GenerativeModel("gemini-1.5-pro")
except Exception as e:
    print(f"Erro ao inicializar o modelo Gemini: {e}")
    model = None # Define model como None se houver erro na inicialização

# --- DEFINIÇÃO DA EQUIPE (Variável Global) ---
# É melhor definir isso fora das funções de rota se for usado em múltiplos lugares
equipe_data = [
    {
        "nome": "Luana Patrícia Gomes da Silva",
        "github": "https://github.com/luanapatriciasilva",
        "foto": "static/images/luana.jpg",
        "descricao": "Sistemas para Internet, Uniesp -PB. Apaixonada por tecnologia e programação."
    }
]

# --- ROTAS DA APLICAÇÃO ---

# Rota para a Página Inicial
@app.route('/')
def pagina_inicial():
    """
    Rota para a página inicial.
    Renderiza o template 'index.html'.
    """
    return render_template('index.html', titulo_pagina="Página Inicial")

# Rota do Gemini (IA)
@app.route('/ia', methods=['GET', 'POST'])
def ia():
    ai_response = None
    error = None
    user_input = ""

    if request.method == 'POST':
        user_input = request.form.get('user_input', '')
        if not model:
            error = "O modelo Gemini não foi inicializado. Verifique sua chave da API e conexão."
        elif not user_input.strip():
            error = "Por favor, digite sua pergunta."
        else:
            try:
                response = model.generate_content(user_input)
                ai_response = response.text
            except Exception as e:
                error = f"Erro ao obter resposta do Gemini: {e}"

    return render_template('ia.html',
                            ai_response=ai_response,
                            user_input=user_input,
                            error=error)

# Rota para a Página da Equipe
@app.route('/equipe')
def pagina_equipe():
    """
    Rota para a página da equipe.
    Renderiza o template 'equipe.html' passando os dados da equipe.
    """
    # Usamos equipe_data que foi definido globalmente
    return render_template('equipe.html', titulo_pagina="Nossa Equipe", equipe=equipe_data)

# Rotas de Fundamentos
@app.route('/fundamentos')
def fundamentos():
    """
    Rota para a página de Fundamentos.
    Renderiza o template 'fundamentos.html'.
    """
    return render_template('fundamentos.html', titulo_pagina="Fundamentos da Programação")

@app.route('/selecao')
def fundamentos_selecao():
    return render_template('selecao.html', titulo_pagina="Estruturas de Seleção")

@app.route('/repeticao')
def fundamentos_repeticao():
    return render_template('repeticao.html', titulo_pagina="Estruturas de Repetição")

@app.route('/vetores-matrizes')
def fundamentos_vetores_matrizes():
    return render_template('vetores_matrizes.html', titulo_pagina="Vetores e Matrizes")

@app.route('/funcoes')
def fundamentos_funcoes():
    return render_template('funcoes.html', titulo_pagina="Funções e Procedimentos")

@app.route('/excecoes')
def fundamentos_excecoes():
    return render_template('excecoes.html', titulo_pagina="Tratamento de Exceções")

# Rotas do Dicionário de Termos
@app.route('/dicionario')
def dicionario():
    termos = carregar_termos()
    return render_template('dicionario.html', termos=termos, titulo_pagina="Dicionário de Termos")

@app.route('/adicionar', methods=['POST'])
def adicionar():
    termo = request.form.get('termo', '').strip() # Adicionado .get para segurança
    definicao = request.form.get('definicao', '').strip() # Adicionado .get para segurança

    if termo and definicao:
        termos = carregar_termos()
        termos[termo] = definicao
        salvar_termos(termos)

    return redirect(url_for('dicionario')) # CORRIGIDO: Nome da função da rota, não o nome do template

@app.route('/alterar', methods=['POST'])
def alterar():
    termo = request.form.get('termo', '')
    nova_definicao = request.form.get('definicao', '').strip()
    termos = carregar_termos()
    if termo in termos and nova_definicao:
        termos[termo] = nova_definicao
        salvar_termos(termos)
    return redirect(url_for('dicionario')) # CORRIGIDO: Nome da função da rota

@app.route('/deletar', methods=['POST'])
def deletar():
    termo = request.form.get('termo', '')
    termos = carregar_termos()
    if termo in termos:
        del termos[termo]
        salvar_termos(termos)
    return redirect(url_for('dicionario')) # CORRIGIDO: Nome da função da rota

if __name__ == '__main__':
    app.run(debug=True)

    pergunte_ia = input("Você gostaria de fazer uma pergunta à IA? (s/n): ")
    if pergunte_ia.lower() == 's':
        pergunta = input("Digite sua pergunta: ")
        if model:
            try:
                resposta = model.generate_content(pergunta)
                print(f"Resposta da IA: {resposta.text}")
            except Exception as e:
                print(f"Erro ao obter resposta da IA: {e}")
        else:
            print("O modelo Gemini não está disponível.")
# O código acima define uma aplicação Flask que integra o modelo Gemini da Google para responder perguntas,
# além de fornecer funcionalidades para um dicionário de termos e uma página sobre a equipe.