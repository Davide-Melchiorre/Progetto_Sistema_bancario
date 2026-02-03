import mysql.connector
from src.connessione_db import DB_CONNNESIONE
from src.Conto import Conto
from src.Interfacce import Interfaccia_salva, Interfaccia_autenticazione

class Cliente(Interfaccia_salva,Interfaccia_autenticazione):
    def __init__(self ,id_cliente,nome, cognome , cf , email,password ,id_filiale):
        self.id_cliente = id_cliente
        self.nome = nome
        self.cognome = cognome 
        self.cf = cf
        self.email = email
        self.password = password
        self.id_filiale = id_filiale

    # salva il cliente nel database
    def salva (self):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary = True)
        try :
            sql = f"""
                INSERT INTO clienti (nome,cognome,codice_fiscale,email,password_hash,id_filiale)
                VALUES ('{self.nome}','{self.cognome}','{self.cf}','{self.email}','{self.password}','{self.id_filiale}')
                """
            cursor.execute(sql)
            connection.commit()
            self.id_cliente = cursor.lastrowid
            print(f"Cliente : '{self.id_cliente}' Creato ")
        except mysql.connector.Error as err :
            print(f"Errore : {err}")
        finally:
            cursor.close()
            connection.close()

    # effettua il login del cliente
    def login (self,email_cliente : str , password_inserita : str):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary = True)
        try :
            sql = f"SELECT * FROM clienti WHERE email = '{email_cliente}' AND password_hash = '{password_inserita}' "
            cursor.execute(sql)
            riga = cursor.fetchone()
            if riga :
                cliente = Cliente(
                        id_cliente = riga['id_cliente'],
                        nome = riga['nome'],
                        cognome = riga['cognome'],
                        cf = riga['codice_fiscale'],
                        email = riga['email'],
                        password = riga['password_hash'],
                        id_filiale=riga['id_filiale']
                )
                return cliente
            else :
                return False
        except mysql.connector.Error as err :
            print(f"Errore : {err}")
        finally:
            cursor.close()
            connection.close()
    
    # recupera i conti associati al cliente
    def recupera_conti(self):
        if self.id_cliente is None :
            print (f"Cliente non trovato, id sbagliato")
            return []
        
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary = True)
        try : 
            sql = f"SELECT * FROM conti WHERE id_cliente = '{self.id_cliente}'"
            cursor.execute(sql)
            conti_aperti = cursor.fetchall()
            return conti_aperti
        except mysql.connector.Error as err :
            print(f"Errore : {err}")
            return []
        finally:
            cursor.close()
            connection.close()

    # legge le notifiche del cliente
    def leggi_notifiche(self):
        if self.id_cliente is None :
            print (f"Cliente non trovato, id sbagliato.")
            return []
        
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary = True)
        try : 
            sql = f"SELECT * FROM notifiche WHERE id_cliente = '{self.id_cliente}'"
            cursor.execute(sql)
            notifiche = cursor.fetchall()
            return notifiche
        except mysql.connector.Error as err :
            print(f"Errore : {err}")
            return []
        finally:
            cursor.close()
            connection.close()

    # recupera le carte associate al cliente
    def recupera_carte(self):
        if self.id_cliente is None:
            return []
        
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary=True)
        try:
            sql = f"SELECT * FROM carte WHERE id_cliente = {self.id_cliente}"
            cursor.execute(sql)
            carte_cliente = cursor.fetchall()
            return carte_cliente
        except mysql.connector.Error as err:
            print(f"Errore: {err}")
            return []
        finally:
            cursor.close()
            connection.close()
    