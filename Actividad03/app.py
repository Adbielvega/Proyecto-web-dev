from flask import Flask, jsonify, request

app = Flask(__name__)

usuarios =[]

@app.route ("/saludo", methods= ["POST"])
def saludo ():
    data =request.json
    nombre = data.get("nombre", "usuario")
    correo = data.get("correo")
    return jsonify({"mensaje": f"Hola, {nombre}! tu correo es {correo}"})

@app.route("/usuario", methods = ["POST"])
def usuario ():
    data = request.json
    if not data or "nombre" not in data:
        return jsonify ({"error": "Datos incompletos"}), 400
    
    return jsonify ({"mensaje": "usuario creado exitosamente"}) 

@app.route("/producto", methods = ["GET"])
def producto ():
    data = {
        "productos": "Laptop",
        "precio": 1200.00,
        "disponible" : True
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
 
