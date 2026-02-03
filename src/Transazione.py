import mysql.connector
from src.connessione_db import DB_CONNNESIONE 

class Transazione:
    def __init__(self, id_conto_sorgente, id_carta,importo, tipo, descrizione=""):
        self.id_transazione = None
        self.id_conto_sorgente = id_conto_sorgente
        self.id_carta = id_carta
        self.importo = importo
        self.tipo_transazione = tipo
        self.descrizione = descrizione

    # salva la transazione nel database 
    def salva(self):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor()
        if self.id_carta is not None :
            modifica_id_carta = self.id_carta 
        else :
            modifica_id_carta = "NULL"
        try:
            sql = f""" INSERT INTO transazioni (id_conto_sorgente,id_carta ,importo, tipo_transazione, descrizione) 
                    VALUES ({self.id_conto_sorgente},{modifica_id_carta}, {self.importo}, '{self.tipo_transazione}', '{self.descrizione}') """
            cursor.execute(sql)
            connection.commit()
            print(f"Transazione salvata!")
        except mysql.connector.Error as err:
            print(f"Errore nel salvataggio transazione: {err}")
        finally:
            cursor.close()
            connection.close()