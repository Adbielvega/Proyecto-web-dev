from flask import Flask, render_template

app = Flask (__name__)

@app.route('/')
def index():
    data = {"title": "Bienvenidos", "message": "Hola, Flask con Jinja2"}
    return render_template('index.html', data=data)

@app.route('/capstone')
def capstone():
    data = {
    "title": "Proyecto Capstone",
    "description": "Lista de Tareas:",
    "items": ["Diseñar la base de datos", "Crear API REST",
    "Conectar Front-End"]
    }
    return render_template('capstone.html', **data)

if __name__ == '__main__':
    app.run(debug=True, port=8514)