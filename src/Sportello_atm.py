import mysql.connector
from src.connessione_db import DB_CONNNESIONE 
from src.Transazione import Transazione
from src.Conto import Conto
from src.Carta import Carta
from src.Carta_di_credito import CartaDiCredito
from src.Carta_di_Debito import CartaDiDebito
from src.Contofactory import ContoFactory

class Sportello_atm():
    def __init__(self,id_atm,stato_atm,id_filiale,importo_disponibile):
        self.id_atm = id_atm
        self.stato_atm = stato_atm
        self.id_filiale = id_filiale
        self.importo_disponibile = float(importo_disponibile)

    # salva lo sportello ATM nel database
    def salva(self):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary = True)
        try:
            sql = f"""
                INSERT INTO sportelli_atm (id_filiale,stato_atm,importo_disponibile)
                VALUES ({self.id_filiale},'{self.stato_atm}',{self.importo_disponibile})
                """
            cursor.execute(sql)
            connection.commit()
            self.id_atm= cursor.lastrowid
            print(f"Sportello '{self.id_atm}' creato!")
        except mysql.connector.Error as err:
            print(f"Errore : {err}")
        finally:
            cursor.close()
            connection.close()

    # effettua il login della carta nell'ATM
    def login(self,id_carta,pin):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary = True)
        dati_carta = None
        try:
            sql = f"SELECT * FROM carte WHERE id_carta = {id_carta}"
            cursor.execute(sql)
            lista = cursor.fetchall()
            if lista :
                dati_carta = lista[0]
        except mysql.connector.Error as err:
            print(f"Errore : {err}")
        finally:
            cursor.close()
            connection.close()

        if not dati_carta :
            return False
        
        tipo = dati_carta['tipo_carta']
        if "Debito" in tipo or "debito" in tipo:
            carta_tmp = CartaDiDebito(
                dati_carta['id_carta'], 
                dati_carta['numero_carta'], 
                dati_carta['pin_hash'], 
                dati_carta['id_conto_collegato'], 
                dati_carta['id_cliente'], 
                dati_carta['data_scadenza']
            )
        elif "Credito" in tipo or "credito" in tipo:
            carta_tmp = CartaDiCredito(
                dati_carta['id_carta'], 
                dati_carta['numero_carta'], 
                dati_carta['pin_hash'], 
                dati_carta['id_conto_collegato'], 
                dati_carta['id_cliente'], 
                dati_carta['data_scadenza'],
                dati_carta['plafond_mensile']
            )
        
        if carta_tmp.verifica_pin(pin):
            print ("Login effetuato")
            return carta_tmp
        else:
            print("Dati inseriti sbagliati")
            return None
        
    # effettua un prelievo tramite ATM dopo aver verificato lo stato dell'ATM, i fondi disponibili e il conto collegato alla carta
    def prelievo_atm(self,cartao , importo):
        if self.stato_atm != "Attivo":
            print("Sportello fuori servizio")
            return False
        
        if float(self.importo_disponibile) < float(importo):
            print("Importo rischiesto troppo alto per questo sportello.")
            return False
        
        conto_tmp = ContoFactory.get_conto_da_id(cartao.id_conto)
        if not conto_tmp:
            return False
        
        if not conto_tmp.verifica_transazione(cartao.id_conto,importo):
            print("Fondi insufficienti sul conto")
            return False

        pagamento = Transazione(cartao.id_conto, cartao.id_carta, -abs(importo), "Prelievo ATM", f"Prelievo effettuato tramite sportello : {self.id_atm}")
        pagamento.salva()

        self.aggiorna_saldo_atm(-abs(importo))
        print("Operazione effettuata con successo")
        return True
    
    # aggiorna il saldo disponibile nell'ATM dopo un prelievo o un deposito
    def aggiorna_saldo_atm(self,importo):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary = True)
        try:
            nuovo_saldo = float(self.importo_disponibile) + float(importo)
            sql = f"UPDATE sportelli_atm SET importo_disponibile = {nuovo_saldo} WHERE id_atm = {self.id_atm}"
            cursor.execute(sql)
            connection.commit()
            self.importo_disponibile = nuovo_saldo
        except mysql.connector.Error as err:
            print(f"Errore : {err}")
        finally:
            cursor.close()
            connection.close()
