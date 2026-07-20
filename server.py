from flask import Flask, request, jsonify
import requests
import database
import os

app = Flask(__name__)
app.json.sort_keys = False

# Devolver todos los usuarios
@app.route('/api/users', methods=['GET'])
def get_users_route():
    list_users = database.get_all_users()
    return jsonify(list_users), 200


# Devolver solo los usuarios consultados
@app.route('/api/users/<int:post_id>', methods=['GET'])
def get_specific_user_route(post_id):
    user = database.get_user_by_id(post_id)
    if user:
        return jsonify(user), 200
    return jsonify({"Error": "Usuario no encontrado"}), 404

# Crear un nuevo usuario
@app.route('/api/users/', methods=['POST'])
def create_user_route():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"Error": "Faltan datos por ingresar."}), 400

    result = database.insert_user(data["name"], data.get("age"), data.get("phone"))

    if result is None:
        return jsonify({"Error": "Algunos de los datos ingresados no es válido."}), 400

    return jsonify({"Response": f"Usuario creado con exito bajo el ID: {result}"}), 201

# Eliminar un usuario existente
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    rows = database.delete_user(user_id)

    if rows == 0:
        return jsonify({"Error": "Usuario no encontrado"}), 404
    return jsonify({"Response": "Usuario eliminado exitosamente"}), 204

# Eliminar todos los usuarios
@app.route('/api/users', methods=['DELETE'])
def delete_all_users_route():
    rows = database.delete_all_users()

    if rows != 0:
        return jsonify({"Response": "Usuarios eliminados exitosamente"}), 204

    return jsonify({"Error": "No se eliminaron los usuarios."}), 400

# Actualizar un usuario
@app.route('/api/users/<int:user_id>', methods=['PUT', 'PATCH'])
def update_user_route(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"Error": "Faltan datos por ingresar."}), 400

    if request.method == "PATCH":
        field = next(iter(data))
        value = data[field]
        rows = database.update_user_field(user_id, field, value)
    else:
        if "name" not in data:
            return jsonify({"Error": "Se requieren todos los campos."}), 400

        rows = database.update_user(user_id, data["name"], data.get("age"), data.get("phone"))

    if rows is None or rows == 0:
        return jsonify({"Error": "Usuario no encontrado o datos no válidos."}), 404

    return jsonify({"Response": f"Usuario {data['name']} actualizado correctamente"}), 200


name_database = "app_database.db"

if os.path.isfile(name_database):
    print(f" * La base de datos '{name_database}' ya se encuentra creada en el directorio actual")
else:
    print(f" * Creando la base de datos '{name_database}' en el directorio actual")
    database.create_user_table()
    database.create_sessions_table()

app.run(debug=True, port=5000)
