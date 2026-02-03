import mysql.connector
from src.connessione_db import DB_CONNNESIONE
from abc import ABC, abstractmethod 
from src.Interfacce import Interfaccia_salva,Interfaccia_stampa

class Carta(Interfaccia_salva,Interfaccia_stampa) :
    def __init__(self,id_carta,numero_carta,pin,tipo_carta,id_conto,id_cliente,data_scadenza):
        self.id_carta = id_carta
        self.numero_carta = numero_carta
        self.pin = pin
        self.tipo_carta = tipo_carta
        self.id_conto = id_conto
        self.id_cliente = id_cliente 
        self.data_scadenza = data_scadenza

    # metodo magico per gestire l'attributo opzionale plafond_mensile
    def __getattr__(self,item):
        if item == "plafond_mensile":
            return 0.0

    # salva la carta nel database    
    def salva(self):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary = True)
        try:
            sql = f"""
                INSERT INTO carte (numero_carta,pin_hash,tipo_carta,id_conto_collegato,id_cliente,plafond_mensile,data_scadenza)
                VALUES ('{self.numero_carta}','{self.pin}','{self.tipo_carta}',{self.id_conto},{self.id_cliente},{self.plafond_mensile},'{self.data_scadenza}')
                """
            cursor.execute(sql)
            connection.commit()
            self.id_carta= cursor.lastrowid
            print(f"Carta '{self.id_carta}' creata!")
        except mysql.connector.Error as err:
            print(f"Errore : {err}")
        finally:
            cursor.close()
            connection.close()
    
    # verifica se il pin inserito corrisponde a quello della carta
    def verifica_pin(self, pin_inserito):
        if not pin_inserito:
            print("Pin sbagliato.")
            return False
        
        if self.pin and pin_inserito == self.pin:
            return True
        
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary=True)
        try:
            sql = f"SELECT pin_hash FROM carte WHERE numero_carta = '{self.numero_carta}'"
            cursor.execute(sql)
            pin_cercato = cursor.fetchone()
            if pin_cercato and pin_cercato['pin_hash'] == pin_inserito:
                return True
            else:
                return False
        except mysql.connector.Error as err:
            print(f"Errore: {err}")
            return False
        finally:
            cursor.close()
            connection.close()

    # metodo astratto che poi verra gestito dalle sottoclassi per inserire la stringa aggiuntiva per la stampa della carta
    def get_info_per_stampa(self):
        return ""
    
    # metodo astratto per effettuare un pagamento con la carta      
    @abstractmethod
    def effettua_pagamento(self, importo, pin_inserito):
        pass