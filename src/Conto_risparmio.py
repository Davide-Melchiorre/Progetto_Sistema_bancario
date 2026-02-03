import mysql.connector
from src.connessione_db import DB_CONNNESIONE
from src.Conto import Conto

class Conto_risparmio(Conto):
    def __init__(self, numero_conto, id_cliente, tasso_interesse = 0.0):
        super().__init__(numero_conto, id_cliente,"Conto Risparmio")
        self.tasso_interesse = tasso_interesse
    
    # calcola gli interessi totali sul conto di risparmio
    def calcola_interessi(self,id_conto : int) -> float:
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary=True)
        try :
            sql = f"SELECT tasso_interesse FROM conti WHERE id_conto = {id_conto}"
            cursor.execute(sql)
            risultato = cursor.fetchone()
            if risultato is None:
                return 0.0
            tasso_effettivo = risultato["tasso_interesse"]
            saldo_reale = self.visualizza_saldo(id_conto)
            saldo_interessi = saldo_reale * (tasso_effettivo / 100)
            return saldo_interessi
        except mysql.connector.Error as err:
            print(f"Errore : {err}")
        finally:
            cursor.close()
            connection.close()
            
    # restituisce il saldo disponibile del conto di risparmio
    def get_saldo_disponibile(self, id_conto):
        return self.visualizza_saldo(id_conto)