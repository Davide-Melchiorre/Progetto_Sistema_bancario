import mysql.connector
from src.connessione_db import DB_CONNNESIONE 

class Notifica:
    def __init__(self, id_cliente, messaggio):
        self.id_notifica = None 
        self.id_cliente = id_cliente
        self.messaggio = messaggio

    # salva la notifica nel database
    def salva(self):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor()
        try:
            sql = f""" INSERT INTO notifiche (id_cliente, messaggio) VALUES ({self.id_cliente}, '{self.messaggio}') """
            cursor.execute(sql)
            connection.commit()
            print(f"Notifica salvata")
        except mysql.connector.Error as err:
            print(f"Errore : {err}")
        finally:
            connection.close()
            cursor.close()
            