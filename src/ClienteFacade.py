import mysql.connector
from src.connessione_db import DB_CONNNESIONE
from src.Contofactory import ContoFactory
from src.Carta_di_credito import CartaDiCredito
from src.Carta_di_Debito import CartaDiDebito
from src.Notifica import Notifica

class ClienteFacade:
    #classe facade per semplificare l'interazione del cliente con il sistema bancario
    def __init__(self, cliente):
        self.cliente = cliente
    
    # restituisce il saldo totale quindi su tutti i conti del cliente
    def get_saldo_totale_patrimonio(self):
        conti = self.cliente.recupera_conti()
        totale = 0.0
        for c in conti:
            conto_obj = ContoFactory.get_conto_da_id(c['id_conto'])
            if conto_obj:
                totale += conto_obj.visualizza_saldo(c['id_conto'])
        return totale

    # restituisce le carte del cliente come oggetti formattati
    def get_carte_formattate(self):
        dati_carte = self.cliente.recupera_carte()
        carte_oggetti = []
        
        for c in dati_carte:
            tipo = c['tipo_carta']
            if "Credito" in tipo:
                carte_oggetti.append(CartaDiCredito(
                    c['id_carta'], 
                    c['numero_carta'], 
                    c['pin_hash'],
                    c['id_conto_collegato'], 
                    c['id_cliente'], 
                    c['data_scadenza'], 
                    c['plafond_mensile']
                ))
            else:
                carte_oggetti.append(CartaDiDebito(
                    c['id_carta'], 
                    c['numero_carta'], 
                    c['pin_hash'],
                    c['id_conto_collegato'], 
                    c['id_cliente'], 
                    c['data_scadenza']
                ))
        return carte_oggetti
    
    # effettua un pagamento con una carta selezionata
    def paga_con_carta_facile(self, id_carta, pin, importo):
        carte = self.get_carte_formattate()
        carta_selezionata = None
        for carta in carte:
            if carta.id_carta == id_carta:
                carta_selezionata = carta
                break
        if not carta_selezionata:
            return "Carta non trovata."
        if carta_selezionata.effettua_pagamento(importo, pin):
            return "Pagamento riuscito!"
        else:
            return "Pagamento fallito (PIN errato o fondi insufficienti)."