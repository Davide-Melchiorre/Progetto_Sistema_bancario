import mysql.connector
from src.connessione_db import DB_CONNNESIONE
from src.Conto_corrente import Conto_corrente
from src.Conto_risparmio import Conto_risparmio
from src.Conto import Conto

# design pattern Factory Method per creare istanze di conti
class ContoFactory :
    # metodo statico per ottenere un oggetto conto in base al tipo
    @staticmethod
    def get_conto(tipo , numero_conto , id_cliente , valore):
        if tipo == "Conto corrente":
            return Conto_corrente(numero_conto,id_cliente,limite_scoperto = valore)
        elif tipo == "Conto Risparmio":
            return Conto_risparmio(numero_conto,id_cliente,tasso_interesse = valore)
    
    # metodo statico per ottenere un oggetto conto da un id_conto
    @staticmethod
    def get_conto_da_id(id_conto):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary=True)
        try:
            sql = f"SELECT * FROM conti WHERE id_conto = {id_conto}"
            cursor.execute(sql)
            dati = cursor.fetchone()
            if not dati:
                return None    
            tipo = dati['tipo_conto']
            if tipo == "Conto corrente":
                return Conto_corrente(dati['numero_conto'], dati['id_cliente'], limite_scoperto=float(dati['limite_scoperto']))
            elif tipo == "Conto Risparmio":
                return Conto_risparmio(dati['numero_conto'], dati['id_cliente'], tasso_interesse=float(dati['tasso_interesse']))
            else:
                return Conto(dati['numero_conto'], dati['id_cliente'], tipo)
        except mysql.connector.Error as err:
            print(f"Errore: {err}")
            return None
        finally:
            cursor.close()
            connection.close()