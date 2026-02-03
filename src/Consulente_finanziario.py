from src.Impiegati import Impiegato
from src.Conto import Conto
import mysql.connector
from src.connessione_db import DB_CONNNESIONE
from src.Conto_corrente import Conto_corrente
from src.Conto_risparmio import Conto_risparmio
from src.Carta_di_credito import CartaDiCredito
from src.Carta_di_Debito import CartaDiDebito
from src.Contofactory import ContoFactory

class Consulente_finanziario(Impiegato):
    def __init__(self,id_impiegato,nome,cognome,email, ruolo , id_filiale,password):
        super().__init__(id_impiegato,nome,cognome,email, ruolo , id_filiale,password)

    # apre un nuovo conto per un cliente dopo aver ricevuto i dati necessari
    def apri_nuovo_conto(self,id_cliente,numero_conto,tipo_conto,valore):
        try :
                nuovo_conto = ContoFactory.get_conto(tipo_conto,numero_conto,id_cliente,valore)
                nuovo_conto.salva()
                return True
        except Exception as err:
            print(f"Errore : {err}")
            return False
        
    # recupera i conti associati a un cliente    
    def leggi_conti_clienti(self,id_cliente):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary=True)
        try :
            sql = f"SELECT * FROM conti WHERE id_cliente = {id_cliente}"
            cursor.execute(sql)
            id_conti_cliente = cursor.fetchall()
            return id_conti_cliente
        except mysql.connector.Error as err:
            print(f"Errore : {err}")
            return []
        finally:
            cursor.close()
            connection.close()
    
    # crea una nuova carta (debito o credito) per un cliente associata a un conto
    def crea_nuova_carta(self,id_cliente,id_conto,numero_carta,pin,data_scadenza,tipo_carta,plafond_mensile = 0.0):
        if tipo_carta == "Debito":
            nuova_carta = CartaDiDebito(None,numero_carta,pin,id_conto,id_cliente,data_scadenza)
            nuova_carta.salva()
            return True
        elif tipo_carta == "Credito":
            nuova_carta = CartaDiCredito(None,numero_carta,pin,id_conto,id_cliente,data_scadenza, plafond_mensile)
            nuova_carta.salva()
            return True
        else :
            print("Tipo carta sbagliato")
            return False