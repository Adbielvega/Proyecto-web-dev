from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "Bienvenido a mi API"

@app.route("/saludo", methods=["GET"])
def saludo():
    data = request.json
    nombre = data.get("nombre", "usuario")
    return f"Hola, {nombre}!"

@app.route("/usuario", methods=["GET", "POST"])
def usuario():
    if request.method == "GET":
        return {"usuario": ["Alice", "Bob", "Charlie"]}

    if request.method == "POST":
        data = request.json
        nuevo_usuario = data.get("nombre")
        return {"mensaje": f"usuario {nuevo_usuario} creado exitosamente!"}, 201

if __name__ == "__main__":
    app.run(debug=True)

