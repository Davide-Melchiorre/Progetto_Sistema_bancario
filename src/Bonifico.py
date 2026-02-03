import mysql.connector
from src.connessione_db import DB_CONNNESIONE 
from src.Transazione import Transazione
from src.Conto import Conto
from src.Notifica import Notifica
from src.Contofactory import ContoFactory

class Bonifico (Transazione):
    def __init__(self, id_conto_sorgente,importo, descrizione,id_conto_destinatario):
        super().__init__(id_conto_sorgente, None,-abs(importo), "Bonifico", "Bonifico in uscita")
        self.id_conto_destinatario = id_conto_destinatario
        self.importo_reale = abs(importo)

    # Trova l'id del cliente partendo dall'id del conto associato
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

    # effettua il bonifico tra due conti dopo aver verificato diversi parametri
    def esegui_bonifico(self):
        if self.id_conto_sorgente == self.id_conto_destinatario :
            print("Operazione Bloccata! Stai cercando di inviare denaro allo stesso conto.")
            return False
        oggetto_temp = ContoFactory.get_conto_da_id(self.id_conto_sorgente)
        if not oggetto_temp:
            print("Conto sorgente non trovato.")
            return False
        saldo_disponibile = oggetto_temp.verifica_transazione(self.id_conto_sorgente,self.importo_reale)
        if saldo_disponibile:
            self.salva()
            pagamento = Transazione(self.id_conto_destinatario,None,self.importo_reale,"Bonifico in entrata", f"Bonifico effettuato da {self.id_conto_sorgente}")
            pagamento.salva()
            id_destinatario_cliente = self.trova_cliente(self.id_conto_destinatario)
            if id_destinatario_cliente:
                messaggio = f"Hai ricevuto un bonifico di {self.importo_reale} €"
                Notifica(id_destinatario_cliente, messaggio).salva()
            id_mittente_cliente = self.trova_cliente(self.id_conto_sorgente)
            if id_mittente_cliente:
                messaggio_mitt = f"Hai inviato un bonifico di {self.importo_reale} €"
                Notifica(id_mittente_cliente, messaggio_mitt).salva()
            print("\nBonifico effettuato.")
            return True
        else :
            print("Fondi non disponibili")
            return False