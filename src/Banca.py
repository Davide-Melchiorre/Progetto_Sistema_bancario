import mysql.connector
from src.connessione_db import DB_CONNNESIONE 
from src.Cliente import Cliente
from src.Impiegati import Impiegato
from src.Cassiere import Cassiere
from src.Consulente_finanziario import Consulente_finanziario
from src.Sportello_atm import Sportello_atm
from src.Filiale import Filiale

class Banca:
    def __init__(self, nome_banca = "Banca 1"):
        self.nome_banca = nome_banca
        self.utente_corrente = None

    #verifica se l'email esiste già in una tabella specifica che viene passata come parametro
    def verifica_email(self, email, tabella):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary=True)
        try:
            sql = f"SELECT * FROM {tabella} WHERE email = '{email}'"
            cursor.execute(sql)
            riga = cursor.fetchone()
            if riga:
                return True
            else:
                return False
        except mysql.connector.Error as err:
            print(f"Errore : {err}")
            return False
        finally:
            cursor.close()
            connection.close()
    
    # effettua il login di un utente, che può essere un cliente o un impiegato
    def login(self,tipo_utente,email,password):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary = True)
        try :
            if tipo_utente == "Cliente":
                nome_tab = "clienti"
            elif tipo_utente == "Impiegato":
                nome_tab = "impiegati"
            sql = f"SELECT * FROM {nome_tab} WHERE email = '{email}' AND password_hash = '{password}'"
            cursor.execute(sql)
            dati = cursor.fetchone()

            if dati :
                if tipo_utente == "Cliente":
                    self.utente_corrente = Cliente(
                        dati['id_cliente'],
                        dati['nome'],
                        dati['cognome'],
                        dati['codice_fiscale'],
                        dati['email'],
                        dati['password_hash'],
                        dati['id_filiale']
                    )
                else :
                    ruolo = dati['ruolo']
                    if ruolo == "Cassiere":
                        self.utente_corrente = Cassiere(
                            dati['id_impiegato'],
                            dati['nome'],
                            dati['cognome'],
                            dati['email'],
                            dati['ruolo'],
                            dati['id_filiale'],
                            dati['password_hash']
                        )
                    elif ruolo == "Consulente Finanziario":
                        self.utente_corrente = Consulente_finanziario(
                            dati['id_impiegato'],
                            dati['nome'],
                            dati['cognome'],
                            dati['email'],
                            dati['ruolo'],
                            dati['id_filiale'],
                            dati['password_hash']
                        )  
                    else : 
                        self.utente_corrente = Impiegato(
                            dati['id_impiegato'],
                            dati['nome'],
                            dati['cognome'],
                            dati['email'],
                            dati['ruolo'],
                            dati['id_filiale'],
                            dati['password_hash']
                        )
                return True
            return False
        except mysql.connector.Error as err:
            print(f"Errore : {err}")
        finally:
            cursor.close()
            connection.close()
    
    #effettua il logout dell'utente corrente
    def logout(self):
        self.utente_corrente = None

    # crea una nuova filiale e la salva nel database
    def crea_filiale(self,codice,indirizzo):
        nuova_filiale = Filiale(codice,indirizzo)
        nuova_filiale.salva()
        return nuova_filiale.id_filiale
    
    # crea un nuovo cliente e lo salva nel database
    def crea_cliente(self,nome,cognome,cf,email,password,id_filiale):
        if self.verifica_email(email, "clienti"):
            print("L'email inserita è gia stata utilizzata.")
            return False
        if self.verifica_email(email, "impiegati"):
            print("L'email inserita è gia stata utilizzata.")
            return False
        nuovo_cliente = Cliente(None,nome,cognome,cf,email,password,id_filiale)
        nuovo_cliente.salva()
        return True
    
    # crea un nuovo impiegato e lo salva nel database
    def crea_impiegato(self,nome,cognome,email,password,ruolo,id_filiale):
        if self.verifica_email(email, "clienti"):
            print("L'email inserita è gia stata utilizzata.")
            return False
        if self.verifica_email(email, "impiegati"):
            print("L'email inserita è gia stata utilizzata.")
            return False
        nuovo_impiegato = Impiegato(None,nome,cognome,email,ruolo,id_filiale,password)
        nuovo_impiegato.salva()
        return True
    
    # crea un nuovo sportello ATM e lo salva nel database
    def crea_sportello(self,id_filiale,importo_disponibile):
        nuovo_sportello = Sportello_atm(None,"Attivo",id_filiale,importo_disponibile)
        nuovo_sportello.salva()
        return nuovo_sportello.id_atm
    
    # restituisce la lista delle filiali presenti nel database
    def lista_filiali(self):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM filiali"
            cursor.execute(sql)
            filiali = cursor.fetchall()
            return filiali
        except mysql.connector.Error as err:
            print(f"Errore: {err}")
            return []
        finally:
            cursor.close()
            connection.close()

    # restituisce la lista degli sportelli ATM presenti nel database
    def lista_atm(self):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM sportelli_atm"
            cursor.execute(sql)
            sportelli = cursor.fetchall()
            return sportelli
        except mysql.connector.Error as err:
            print(f"Errore recupero ATM: {err}")
            return []
        finally:
            cursor.close()
            connection.close()