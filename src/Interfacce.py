from abc import ABC, abstractmethod

# interfaccia per il salvataggio nel database
class Interfaccia_salva(ABC):
    @abstractmethod
    def salva(self):
        pass


# interfaccia per la stampa delle informazioni
class Interfaccia_stampa(ABC):
    @abstractmethod
    def get_info_per_stampa(self) :
        pass


# interfaccia per l'autenticazione degli utenti
class Interfaccia_autenticazione(ABC):
    @abstractmethod
    def login(self, email, password):
        pass