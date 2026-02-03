from src.Carta import Carta
from src.Conto import Conto
from src.Transazione import Transazione
from src.Notifica import Notifica
from src.connessione_db import DB_CONNNESIONE
import mysql.connector

class CartaDiCredito(Carta):
    def __init__(self, id_carta, numero_carta, pin, id_conto, id_cliente, data_scadenza,plafond_mensile):
        super().__init__(id_carta, numero_carta, pin, "Carta Di Credito", id_conto, id_cliente, data_scadenza)
        self.plafond_mensile = float(plafond_mensile)

    # calcola le spese totali effettuate con la carta di credito senza considerare il plafond
    def calcola_spese(self):
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor(dictionary=True)
        try :
            sql = f"""
                SELECT SUM(importo) AS somma_imp 
                FROM transazioni 
                WHERE id_carta = {self.id_carta} 
                AND importo < 0
                """
            cursor.execute(sql)
            riga_importo = cursor.fetchone()
            if riga_importo is None or riga_importo['somma_imp'] is None:
                return 0.0
            
            spese = float(abs(riga_importo['somma_imp']))
            return spese
        except mysql.connector.Error as err:
            print(f"Errore: {err}")
            return 0.0
        finally:
            cursor.close()
            connection.close()

    # verifica se il pagamento rientra nel plafond mensile
    def verifica_plafond(self,importo):
        spese_attuali = self.calcola_spese()
        if spese_attuali + importo <= self.plafond_mensile:
            return True
        else:
            return False
        
    # restituisce il plafond residuo disponibile
    def get_plafond_residuo(self):
        spese_totali = self.calcola_spese()
        return self.plafond_mensile - spese_totali
    
    # restituisce la stringa aggiuntiva per la stampa delle info della carta di credito
    def get_info_per_stampa(self):
        residuo = self.get_plafond_residuo()
        return f" - Plafond Residuo: {residuo} €"
    
    # effettua un pagamento con la carta di credito dopo aver verificato il pin e il plafond    
    def effettua_pagamento(self,importo, pin_ins):
        if not self.verifica_pin(pin_ins):
            return False
        if self.verifica_plafond(importo):
            saldo = self.calcola_spese()
            plafond_residuo = self.plafond_mensile - saldo
            if plafond_residuo >= importo :
                pagamento = Transazione(self.id_conto,self.id_carta,-abs(importo),"carta di Credito", "Pagamento con carta di Credito")
                pagamento.salva()
                messaggio = f"Pagamento di {importo} € effettuato con Carta di Credito."
                Notifica(self.id_cliente, messaggio).salva()
                print("\nPagamento effettuato.")
                return True
            else :
                print("Fondi non disponibili")
                return False
        else:
            print("impossibile eseguire l'operazione")
            return False