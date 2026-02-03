import mysql.connector
from src.connessione_db import DB_CONNNESIONE 

class Filiale:
    def __init__(self, codice_filiale, indirizzo):
        self.id_filiale = None
        self.codice_filiale = codice_filiale
        self.indirizzo = indirizzo

    # salva la filiale nel database 
    def salva(self):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor()
        try:
            sql = f""" INSERT INTO filiali (codice_filiale, indirizzo) VALUES ('{self.codice_filiale}', '{self.indirizzo}') """
            cursor.execute(sql)
            connection.commit()   
            self.id_filiale = cursor.lastrowid
            print(f"Filiale '{self.id_filiale}' creata!")
        except mysql.connector.Error as err:
            print(f"Errore creazione filiale: {err}")
        finally:
            cursor.close()
            connection.close()

    # mostra gli impiegati associati a una filiale
    def mostra_impiegati(self, id_filiale_da_trovare : int):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary=True)
        try:
            sql = f"SELECT * FROM impiegati WHERE id_filiale = {id_filiale_da_trovare}"
            cursor.execute(sql)
            risultati = cursor.fetchall() # Prende TUTTE le righe trovate
            if not risultati:
                print(f"Nessun impiegato trovato nella filiale {id_filiale_da_trovare}")
            return risultati
        except mysql.connector.Error as err:
            print(f"Errore: {err}")
            return []
        finally:
            cursor.close()
            connection.close()

    # mostra i clienti associati a una filiale
    def mostra_clienti_locali(self, id_filiale_da_trovare : int):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary=True)
        try:
            sql = f"SELECT * FROM clienti WHERE id_filiale = {id_filiale_da_trovare}"
            cursor.execute(sql)
            risultati = cursor.fetchall()
            if not risultati:
                print(f"Nessun cliente registrato nella filiale {id_filiale_da_trovare}")
            return risultati
        except mysql.connector.Error as err:
            print(f"Errore: {err}")
            return []
        finally:
            cursor.close()
            connection.close()