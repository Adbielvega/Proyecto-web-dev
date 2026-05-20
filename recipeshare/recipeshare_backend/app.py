from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection


app = Flask(__name__)
app.config["SECRET_KEY"] = "recipeshare_secret"

CORS(app)

def success(data=None, message="OK", status=200):
    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), status

def error(message="Error", status=400):
    return jsonify({
        "success": False,
        "message": message,
        "data": None
    }), status

def login_required(fn):

    from functools import wraps

    @wraps(fn)
    def wrapper(*args, **kwargs):

        if "user_id" not in session:

            return error(
                "Debe iniciar sesion.",
                401
            )

        return fn(*args, **kwargs)

    return wrapper

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/test-db")
def test_db():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT DATABASE();")

        db_name = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify({
            "success": True,
            "database": db_name[0]
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.post("/api/register")
def register():

    data = request.get_json() or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if len(name) < 3:
        return error("El nombre debe tener al menos 3 caracteres.")

    if "@" not in email:
        return error("Email invalido.")

    if len(password) < 6:
        return error("Password muy corto.")

    password_hash = generate_password_hash(password)

    conn = get_connection()
    cursor = conn.cursor()



    try:

        cursor.execute(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (%s, %s, %s)
            """,
            (name, email, password_hash)
        )

        conn.commit()

        user_id = cursor.lastrowid

        return success({
            "id": user_id,
            "name": name,
            "email": email
        }, "Usuario registrado.", 201)

    except Exception as e:

        conn.rollback()

        return error(str(e), 409)

    finally:

        cursor.close()
        conn.close()

@app.post("/api/login")
def login():

    data = request.get_json() or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE email = %s",
        (email,)
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return error("Usuario no encontrado.", 404)

    if not check_password_hash(user["password_hash"], password):
        return error("Password incorrecto.", 401)

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]

    return success({
        "id": user["id"],
        "name": user["name"],
        "email": user["email"]
    }, "Login correcto.")
    
@app.get("/api/recipes")
def get_recipes():

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            r.id,
            r.title,
            r.description,
            r.prep_minutes,
            r.created_at,

            u.name AS author_name,

            COUNT(l.id) AS likes_count

        FROM recipes r

        JOIN users u
        ON r.user_id = u.id

        LEFT JOIN recipe_likes l
        ON r.id = l.recipe_id

        GROUP BY
            r.id,
            r.title,
            r.description,
            r.prep_minutes,
            r.created_at,
            u.name

        ORDER BY r.created_at DESC
    """

    cursor.execute(query)

    recipes = cursor.fetchall()

    cursor.close()
    conn.close()

    return success(recipes)

@app.post("/api/recipes")
@login_required
def create_recipe():

    data = request.get_json() or {}

    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    ingredients = data.get("ingredients", "").strip()
    steps = data.get("steps", "").strip()

    prep_minutes = data.get("prep_minutes", 0)

    if len(title) < 3:
        return error("Titulo muy corto.")

    if len(description) < 10:
        return error("Descripcion muy corta.")

    if len(ingredients) < 5:
        return error("Ingredientes invalidos.")

    if len(steps) < 5:
        return error("Pasos invalidos.")

    try:
        prep_minutes = int(prep_minutes)

        if prep_minutes <= 0:
            return error("Tiempo invalido.")

    except:
        return error("prep_minutes debe ser entero.")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO recipes
        (
            user_id,
            title,
            description,
            ingredients,
            steps,
            prep_minutes
        )
        VALUES
        (%s, %s, %s, %s, %s, %s)
        """,
        (
            session["user_id"],
            title,
            description,
            ingredients,
            steps,
            prep_minutes
        )
    )

    conn.commit()

    recipe_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return success(
        {
            "recipe_id": recipe_id
        },
        "Receta creada.",
        201
    )

@app.put("/api/recipes/<int:recipe_id>")
@login_required
def update_recipe(recipe_id):

    data = request.get_json() or {}

    title = data.get("title", "").strip()
    description = data.get("description", "").strip()
    ingredients = data.get("ingredients", "").strip()
    steps = data.get("steps", "").strip()

    prep_minutes = data.get("prep_minutes", 0)

    if len(title) < 3:
        return error("Titulo muy corto.")

    try:
        prep_minutes = int(prep_minutes)

    except:
        return error("Tiempo invalido.")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE recipes
        SET
            title=%s,
            description=%s,
            ingredients=%s,
            steps=%s,
            prep_minutes=%s

        WHERE id=%s
        AND user_id=%s
        """,
        (
            title,
            description,
            ingredients,
            steps,
            prep_minutes,
            recipe_id,
            session["user_id"]
        )
    )

    conn.commit()

    affected = cursor.rowcount

    cursor.close()
    conn.close()

    if affected == 0:

        return error(
            "No existe la receta o no tienes permiso.",
            404
        )

    return success(
        message="Receta actualizada."
    )

@app.delete("/api/recipes/<int:recipe_id>")
@login_required
def delete_recipe(recipe_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM recipes
        WHERE id=%s
        AND user_id=%s
        """,
        (
            recipe_id,
            session["user_id"]
        )
    )

    conn.commit()

    affected = cursor.rowcount

    cursor.close()
    conn.close()

    if affected == 0:

        return error(
            "No existe la receta o no tienes permiso.",
            404
        )

    return success(
        message="Receta eliminada."
    )

@app.post("/api/recipes/<int:recipe_id>/like")
@login_required
def add_like(recipe_id):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO recipe_likes
            (user_id, recipe_id)
            VALUES (%s, %s)
            """,
            (
                session["user_id"],
                recipe_id
            )
        )

        conn.commit()

        return success(
            message="Like registrado.",
            status=201
        )

    except Exception:

        conn.rollback()

        return error(
            "Ya habias dado like o la receta no existe.",
            409
        )

    finally:

        cursor.close()
        conn.close()

@app.post("/api/recipes/<int:recipe_id>/favorite")
@login_required
def add_favorite(recipe_id):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO favorites
            (user_id, recipe_id)
            VALUES (%s, %s)
            """,
            (
                session["user_id"],
                recipe_id
            )
        )

        conn.commit()

        return success(
            message="Receta agregada a favoritos.",
            status=201
        )

    except Exception:

        conn.rollback()

        return error(
            "La receta ya estaba en favoritos o no existe.",
            409
        )

    finally:

        cursor.close()
        conn.close()

@app.post("/api/logout")
@login_required
def logout():

    session.clear()

    return success(
        message="Sesion cerrada."
    )

if __name__ == "__main__":
    app.run(debug=True)