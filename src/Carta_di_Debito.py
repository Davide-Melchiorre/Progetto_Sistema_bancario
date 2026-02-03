from src.Carta import Carta
from src.Conto import Conto
from src.Transazione import Transazione
from src.Notifica import Notifica
from src.Contofactory import ContoFactory

class CartaDiDebito(Carta):
    def __init__(self, id_carta, numero_carta, pin, id_conto, id_cliente, data_scadenza):
        super().__init__(id_carta, numero_carta, pin, "Carta Di Debito", id_conto, id_cliente, data_scadenza)

    # effettua un pagamento con la carta di debito dopo aver verificato il pin e la disponibilità del conto
    def effettua_pagamento(self,importo , pin_inserito):
        if not self.verifica_pin(pin_inserito):
            return False
        oggetto_temp = ContoFactory.get_conto_da_id(self.id_conto)
        if oggetto_temp and oggetto_temp.verifica_transazione(self.id_conto, importo):
            pagamento = Transazione(self.id_conto,self.id_carta,-abs(importo),"carta di debito", "Pagamento con carta di debito")
            pagamento.salva()
            messaggio = f"Pagamento di {importo} € effettuato con Carta di Debito."
            Notifica(self.id_cliente, messaggio).salva()
            print("Pagamento effettuato.")
            return True
        else :
            print("Fondi non disponibili")
            return False
        