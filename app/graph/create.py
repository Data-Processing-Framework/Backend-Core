from flask import jsonify
from app.helpers.controller import controller
import mysql.connector
from datetime import datetime

conexion = mysql.connector.connect(
                host="log-db",
                user="logger",
                port=3306,
                password="Password12345",
                database="logs"
)

def create(request, name):

    try:
        # Get the request json data and create a singleton instance of the controller
        request_json = request.get_json()
        singleton = controller()

        name = "Worker 5"

        cursor = conexion.cursor()
        
        return_items = request_json["number"]

        if len(request_json['fromDate'])!=0 and len(request_json['toDate'] !=0):
            fromDate = request_json['fromDate']
            toDate = request_json['toDate']

        if len(fromDate) and len(toDate) != 0:

            cursor.execute("SELECT * FROM Workers WHERE name = %s AND created_at BETWEEN %s AND %s LIMIT %s", [name, fromDate, toDate, return_items])
            resultados = cursor.fetchall()

            for fila in resultados:
                print(fila)

        else:
            cursor.execute("SELECT * FROM Workers WHERE name = %s LIMIT %s", [name, return_items])
            resultados = cursor.fetchall()

            for fila in resultados:
                print(fila)

        cursor.close()
        conexion.close()



    except:
        pass
    return jsonify({"status": 200})  # Exemple de resposta
