import mysql.connector
from src.connessione_db import DB_CONNNESIONE 
from src.Interfacce import Interfaccia_salva,Interfaccia_autenticazione

class Impiegato(Interfaccia_salva,Interfaccia_autenticazione):
    def __init__(self,id_impiegato,nome,cognome,email, ruolo , id_filiale,password):
        self.id_impiegato = id_impiegato
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.ruolo = ruolo
        self.id_filiale = id_filiale
        self.password = password

    # salva l'impiegato nel database
    def salva(self):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary = True)
        if self.id_filiale is not None :
            modifica_id_filiale = self.id_filiale
        else :
            modifica_id_filiale = "NULL"
        try : 
            sql = f"""
                INSERT INTO impiegati (nome,cognome,email,ruolo,id_filiale,password_hash)
                VALUES ('{self.nome}','{self.cognome}','{self.email}','{self.ruolo}',{modifica_id_filiale},'{self.password}')
                """
            cursor.execute(sql)
            connection.commit()
            self.id_impiegato = cursor.lastrowid
            print(f"Impiegato : '{self.id_impiegato}' Creato ")
        except mysql.connector.Error as err :
            print(f"Errore : {err}")
        finally:
            cursor.close()
            connection.close()
    
    # effettua il login dell'impiegato
    def login (self,email_cliente : str , password_inserita : str):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary = True)
        try :
            sql = f"SELECT * FROM impiegati WHERE email = '{email_cliente}' AND password_hash = '{password_inserita}' "
            cursor.execute(sql)
            riga = cursor.fetchone()
            if riga :
                impiegato = Impiegato(
                        id_impiegato = riga['id_impiegato'],
                        nome = riga['nome'],
                        cognome = riga['cognome'],
                        email = riga['email'],
                        ruolo = riga['ruolo'],
                        password = riga['password_hash'],
                        id_filiale = riga['id_filiale']
                )
                return impiegato
            else :
                return False
        except mysql.connector.Error as err :
            print(f"Errore : {err}")
        finally:
            cursor.close()
            connection.close()

    # mostra i dati della filiale associata all'impiegato
    def visualizza_filiale(self):
        if self.id_filiale is None :
            print (f"Impiegato non trovato, id sbagliato")
            return []
        
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary = True)
        try : 
            sql = f"SELECT * FROM filiali WHERE id_filiale = '{self.id_filiale}'"
            cursor.execute(sql)
            dati_filiale = cursor.fetchone()
            return dati_filiale
        except mysql.connector.Error as err :
            print(f"Errore : {err}")
            return []
        finally:
            cursor.close()
            connection.close()
    
    # mostra i dati dell'impiegato
    def visualizza_dati_impiegato(self):
        if self.id_impiegato is None :
            print (f"Impiegato non trovato, id sbagliato")
            return []
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary = True)
        try : 
            sql = f"SELECT * FROM impiegati WHERE id_impiegato = '{self.id_impiegato}'"
            cursor.execute(sql)
            dati_impiegato = cursor.fetchone()
            return dati_impiegato
        except mysql.connector.Error as err :
            print(f"Errore : {err}")
            return []
        finally:
            cursor.close()
            connection.close()
