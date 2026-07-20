# Rest-API Project

Este es un pequeño proyecto práctico de desarrollo que hice siguiendo la metodología CRUD. Usé un servidor Flask para la API RESTful, SQLite para la persistencia de los datos, y desarrollé un cliente personalizado disponible en CLI/GUI (La GUI fue enteramente relizada pro Claude AI).

## Arquitectura

```
server.py       -> Rutas Flask (API REST)
database.py     -> Capa de acceso a SQLite
api_client.py   -> Cliente HTTP compartido (requests)
client.py       -> Interfaz de línea de comandos
client_gui.py   -> Interfaz gráfica (Tkinter)
```

`api_client.py` existe para que `client.py` y `client_gui.py` compartan la misma lógica (requests) y se evite duplicar el código entre ambas interfaces.

## Endpoints

| Método | Ruta                  | Descripción                          |
|--------|-----------------------|---------------------------------------|
| GET    | `/api/users`          | Lista todos los usuarios              |
| GET    | `/api/users/<id>`     | Consulta un usuario específico        |
| POST   | `/api/users/`         | Crea un nuevo usuario                 |
| PUT    | `/api/users/<id>`     | Actualiza todos los campos de un usuario |
| PATCH  | `/api/users/<id>`     | Actualiza un solo campo               |
| DELETE | `/api/users/<id>`     | Elimina un usuario específico         |
| DELETE | `/api/users`          | Elimina todos los usuarios            |

## Requisitos

```bash
pip install flask requests
```

## Uso

**1. Levantar el servidor:**

```bash
python3 server.py
```

**2. Cliente CLI:**

```bash
python3 client.py
```

> [!NOTE]
>
> Las queries dentro de la database.py usan parámetros (`?`), siguiendo las buenas prácticas de desarrollo y evitando las inyecciones SQL.
>
> El campo de actualizar datos vía `PATCH` se valida contra una lista blanca de columnas permitidas (`name`, `age`, `phone`) antes de construir la query.
>
> Mi próximo objetivo con este proyecto es el de probar autenticación/autorización real mediante el acceso a las funciones ya desarrolladas con un control de acceso basado en roles. Basicamente agregar (registro/login), campos de autenticación (password_hash) y de roles (role)

## Algunos archivos de útiles de demostración (no forman parte del proyecto)

* `insecure_database.py`
  Este programa fue escrito para probar la vulnerabilidad inyección SQL dentro del mismo código, cuando lo estaba escribiendo.

> [!IMPORTANT]
> Este código no deben tomarse como referencia de buenas prácticas. Solo lo incluyo, como evidencia de mi proceso de aprendizaje.

* `inserts.py`
  Este es un script para rellenar la tabla `users` de manera automatizada y rápida, facilitando el uso del proyecto con datos "reales"

## Cierre

Dicho todo eso, agradezco te hayas pasado por aquí. Ten un bonito recorrido en internet!

Happy Hacking! :D
