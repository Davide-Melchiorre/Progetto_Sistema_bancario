import mysql.connector
from src.connessione_db import DB_CONNNESIONE
from src.Conto import Conto

class Conto_corrente(Conto):
    def __init__(self, numero_conto, id_cliente,limite_scoperto = 0.0):
        super().__init__(numero_conto, id_cliente,"Conto corrente")
        self.limite_scoperto = limite_scoperto

    # mostra il saldo spendibile del conto corrente (incluso il fido)
    def visualizza_saldo_spendibile(self , id_conto : int) -> float:
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary=True)
        try :
            sql = f"""SELECT limite_scoperto FROM conti WHERE id_conto = {id_conto}"""
            cursor.execute(sql)
            risultato = cursor.fetchone()
            if risultato is None:
                return 0.0
            saldo_fido = float(risultato["limite_scoperto"])
            saldo_reale = self.visualizza_saldo(id_conto)
            return saldo_reale + saldo_fido
        except mysql.connector.Error as err:
            print(f"Errore : {err}")
        finally:
            cursor.close()
            connection.close()

    # restituisce il saldo disponibile del conto corrente
    def get_saldo_disponibile(self, id_conto):
        return self.visualizza_saldo_spendibile(id_conto)