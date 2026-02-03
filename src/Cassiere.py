from src.Impiegati import Impiegato
from src.Conto import Conto
from src.Transazione import Transazione
from src.Notifica import Notifica
from src.Contofactory import ContoFactory
import mysql.connector
from src.connessione_db import DB_CONNNESIONE

class Cassiere(Impiegato):
    def __init__(self,id_impiegato,nome,cognome,email, ruolo , id_filiale,password):
        super().__init__(id_impiegato,nome,cognome,email, ruolo , id_filiale,password)

    # trova il cliente associato a un conto
    def trova_cliente(self,id_conto):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary=True)
        try:
            sql = f"SELECT id_cliente FROM conti WHERE id_conto = {id_conto}"
            cursor.execute(sql)
            id_cliente = cursor.fetchone()
            if id_cliente:
                return id_cliente['id_cliente']
            return None
        finally:
            cursor.close()
            connection.close()

    # effettua un versamento su un conto, invia una notifica al cliente dopo le dovute verifiche e stampa l'operazione
    def effettua_versamento(self,id_conto,importo):
        try:
            versamento = Transazione(id_conto,None,importo,"Versamento",f"Versamento effettuato dal cassiere : {self.id_impiegato}")
            versamento.salva()
            id_cliente = self.trova_cliente(id_conto)
            if id_cliente:
                messaggio = f"Hai ricevuto un versamento di {importo} € sul conto {id_conto}."
                notifica = Notifica(id_cliente, messaggio)
                notifica.salva()
            self.stampa_operazione(id_conto, "Versamento",importo)
            return True
        except Exception as err:
            print(f"Errore : {err}")
            return False

    # effettua un prelievo su un conto , invia una notifica al cliente dopo le dovute verifiche e stampa l'operazione    
    def effettua_prelievo(self,id_conto,importo):
        try :
            conto_obj = ContoFactory.get_conto_da_id(id_conto)

            if not conto_obj:
                print("Conto non trovato.")
                return False
            if not conto_obj.verifica_transazione(id_conto, importo):
                print(f"Operazione negata, fondi insufficienti.")
                return False
            importo_prelievo = -abs(importo)
            prelievo = Transazione(id_conto,None,importo_prelievo,"Prelievo",f"Prelievo effettuato dal cassiere : {self.id_impiegato}")
            prelievo.salva()
            id_cliente = self.trova_cliente(id_conto)
            if id_cliente:
                messaggio = f"È stato effettuato un prelievo di {importo} € dal conto {id_conto}."
                Notifica(id_cliente, messaggio).salva()
            self.stampa_operazione(id_conto, "Prelievo",importo)
            return True
        except Exception as err:
            print(f"Errore : {err}")
            return False
        
    # stampa i dettagli dell'operazione effettuata dal cassiere    
    def stampa_operazione(self,id_conto,tipo,importo):
        print(f"Tipo : {tipo} ")
        print(f"Conto : {id_conto} ")
        print(f"Importo : {importo} ")
        print(f"Cassiere : {self.id_impiegato} , {self.nome}, {self.cognome}")