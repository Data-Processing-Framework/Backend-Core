from flask import jsonify
import mysql.connector
import os


def create(request, name):

    try:
        # Get the request json data and create a singleton instance of the controller
        request_json = request.get_json()
        conexion = mysql.connector.connect(
            host=os.getenv("LOGGING_DB_HOST"),
            user=os.getenv("LOGGING_DB_USER"),
            password=os.getenv("LOGGING_DB_PASSWORD"),
            database=os.getenv("LOGGING_DB_NAME"),
        )

        cursor = conexion.cursor()

        return_items = request_json["number"]

        if len(request_json["fromDate"]) != 0 and len(request_json["toDate"] != 0):
            fromDate = request_json["fromDate"]
            toDate = request_json["toDate"]

        if len(fromDate) and len(toDate) != 0:

            cursor.execute(
                "SELECT * FROM Workers WHERE name = %s AND created_at BETWEEN %s AND %s LIMIT %s",
                [name, fromDate, toDate, return_items],
            )
            resultados = cursor.fetchall()

            for fila in resultados:
                print(fila)

        else:
            cursor.execute(
                "SELECT * FROM Workers WHERE name = %s LIMIT %s", [name, return_items]
            )
            resultados = cursor.fetchall()

            for fila in resultados:
                print(fila)

        cursor.close()
        conexion.close()

    except:
        pass
    return jsonify({"status": 200})  # Exemple de resposta
