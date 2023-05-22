from flask import jsonify
import mysql.connector
import os


def logs(request, name):

    try:
        request_json = request.get_json()
        conexion = mysql.connector.connect(
            host=os.getenv("LOGGING_DB_HOST"),
            user=os.getenv("LOGGING_DB_USER"),
            password=os.getenv("LOGGING_DB_PASSWORD"),
            database=os.getenv("LOGGING_DB_NAME"),
        )

        cursor = conexion.cursor()

        return_items = request_json["number"]

        fromDate = request_json["fromDate"]
        toDate = request_json["toDate"]

        if len(fromDate) and len(toDate) != 0:

            cursor.execute(
                "SELECT created_at, log_levelname, type, name, created_by, log  FROM Workers WHERE name = %s AND created_at BETWEEN %s AND %s LIMIT %s",
                [name, fromDate, toDate, return_items],
            )
            resultados = cursor.fetchall()

            for fila in resultados:
                print(fila)

        else:
            cursor.execute(
                "SELECT created_at, log_levelname, type, name, created_by, log FROM Workers WHERE name = %s LIMIT %s",
                [name, return_items],
            )
            resultados = cursor.fetchall()
            r = "[created_at, log_levelname, type, name, created_by, log]\n"

            for fila in resultados:
                fila = list(fila)
                fila[0] = str(fila[0])
                r += str(fila) + "\n"

        cursor.close()
        conexion.close()

        return r

    except Exception as e:
        return (
            jsonify(
                {
                    "errors": [
                        {
                            "error": "Core error",
                            "message": str(e),
                            "detail": "Error getting history, try restarting the system.",
                        }
                    ],
                    "code": 400,
                }
            ),
            400,
        )
