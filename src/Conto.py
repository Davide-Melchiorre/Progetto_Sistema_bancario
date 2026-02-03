import mysql.connector
from src.connessione_db import DB_CONNNESIONE 

class Conto:
    def __init__(self, numero_conto, id_cliente, tipo_conto):
        self.id_conto = None 
        self.numero_conto = numero_conto
        self.id_cliente = id_cliente
        self.tipo_conto = tipo_conto

    # metodo magico per gestire attributi opzionali
    def __getattr__(self, item):
        if item == "limite_scoperto":
            return 0.0
        elif item == "tasso_interesse":
            return 0.0

    # salva il conto nel database
    def salva(self):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary = True)
        try:
            sql = f"""
                INSERT INTO conti (numero_conto, id_cliente, tipo_conto, limite_scoperto, tasso_interesse)
                VALUES ('{self.numero_conto}', {self.id_cliente}, '{self.tipo_conto}', {self.limite_scoperto}, {self.tasso_interesse})
                """
            cursor.execute(sql)
            connection.commit()
            self.id_conto = cursor.lastrowid
            print(f"Conto '{self.id_conto}' creato!")
        except mysql.connector.Error as err:
            print(f"Errore : {err}")
        finally:
            cursor.close()
            connection.close()

    # mostra il saldo reale del conto
    def visualizza_saldo(self , id_conto : int) -> float:
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary=True)
        try:
            sql = f"SELECT SUM(importo) AS somma_importi FROM transazioni WHERE id_conto_sorgente = {id_conto}"
            cursor.execute(sql)
            risultato = cursor.fetchone()
            if risultato is None:
                return 0.0
            valore_saldo = risultato['somma_importi']
            if valore_saldo is None:
                return 0.0
            return float(valore_saldo)
        except mysql.connector.Error as err:
            print(f"Errore : {err}")
        finally:
            cursor.close()
            connection.close()

    # restituisce il saldo disponibile del conto
    def get_saldo_disponibile(self, id_conto):
        return self.visualizza_saldo(id_conto)
    
    # design pattern template method per verificare se una transazione può essere effettuata
    def verifica_transazione(self, id_conto: int, importo_da_spendere: float):
        # Passo 1
        disponibilita_totale = self.get_saldo_disponibile(id_conto)
        #Passo 2
        if disponibilita_totale >= importo_da_spendere :
            return True
        else :
            return False

    # mostra le transazioni associate al conto
    def visualizza_transazioni_conto(self ,id_conto : int):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary=True)
        try:
            sql = f""" SELECT * FROM transazioni WHERE id_conto_sorgente = {id_conto}"""
            cursor.execute(sql)
            lista_transazioni = cursor.fetchall()
            return lista_transazioni 
        except mysql.connector.Error as err:
            print(f"Errore : {err}")
        finally:
            cursor.close()
            connection.close()
