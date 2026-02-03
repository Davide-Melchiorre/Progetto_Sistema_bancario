from src.Banca import Banca
from src.Bonifico import Bonifico
from src.Conto import Conto
from src.Sportello_atm import Sportello_atm
from src.Carta_di_Debito import CartaDiDebito
from src.Carta_di_credito import CartaDiCredito
from src.Conto_corrente import Conto_corrente
from src.Conto_risparmio import Conto_risparmio
from src.ClienteFacade import ClienteFacade
from src.Interfacce import Interfaccia_autenticazione,Interfaccia_salva,Interfaccia_stampa
from abc import ABC, abstractmethod 
import mysql.connector
from src.connessione_db import DB_CONNNESIONE

# restituisce un dizionario di filiali e chiede all'utente di selezionarne una
def seleziona_filiale(banca):
    lista_filiali = banca.lista_filiali()
    if not lista_filiali:
        print("Non esistono filiali")
        return None
    
    filiali = {}
    for i in lista_filiali:
        chiave = i['codice_filiale'].upper()
        valore = i['id_filiale']
        filiali[chiave] = valore

    print("\n-- Seleziona Filiale --")
    for i in lista_filiali:
        print(f"{i['codice_filiale']} in {i['indirizzo']}")
    
    while True:
        inp_codice = input("Inserisci codice della filiale : ")
        if inp_codice in filiali :
            return filiali[inp_codice]
        else :
            print("\nCodice sbagliato, non esiste una filiale con questo codice.")

#restituisce una lista di ATM e chiede all'utente di selezionarne uno per facilitare l'accesso
def seleziona_atm(banca):
    lista_atm = banca.lista_atm()
    if not lista_atm:
        print("Non esistono sportelli ATM")
        return None
    print("\n-- Seleziona Sportello ATM --")
    id_validi = []
    for i in lista_atm:
        print(f"Id : {i['id_atm']} - Filiale : {i['id_filiale']} - Stato : {i['stato_atm']}")
        id_validi.append(i['id_atm'])

    while True :
        id_scelto = int(input("Inserisci Id sportello : "))
        if id_scelto in id_validi:
            return id_scelto
        else:
            print("Id non presente. Lo sportello non esiste .")

#menu per l'amministratore della banca
def menu_admin(banca):
    while True:
        print("\n-- Menu Admin --")
        print("1. Crea Nuova Filiale")
        print("2. Crea Impiegato")
        print("3. Crea Cliente")
        print("4. Crea Sportello Atm")
        print("5. Logout")
        scelta = int(input(">> "))
        match scelta:
            case 1:
                print("\n")
                codice = input("Inserisci codice Filiale : ")
                indirizzo = input("Inserisci indizzo filiale : ")
                filiale = banca.crea_filiale(codice,indirizzo)
                if filiale:
                    print("Filiale creata con successo!")

            case 2 :
                print("\n")
                nome = input("Inserisci nome impiegato : ")
                cognome = input("Inserisci cognome : ")
                email = input("Inserisci email : ")
                password = input("Inserisci password : ")
                while True :
                    ruolo = input("Inserisci ruolo(Cassiere o Consulente Finanziario): ").strip().lower()
                    if ruolo == "cassiere":
                        ruolo_d = "Cassiere"
                        break
                    elif ruolo == "consulente finanziario":
                        ruolo_d = "Consulente Finanziario"
                        break
                    else :
                        print("Ruolo sbagliato, riprova")
                id_filiale = seleziona_filiale(banca)
                print("\n")
                if id_filiale :
                    if banca.crea_impiegato(nome,cognome,email,password,ruolo_d,id_filiale):
                        print(f"L'impiegato {nome} {cognome} è stato creato nel ruolo di {ruolo_d}")

            case 3:
                print("\n")
                nome = input("Inserisci nome Cliente : ")
                cognome = input("Inserisci cognome : ")
                cf = input("Inserisci codice fiscale : ")
                email = input("Inserisci email : ")
                password = input("Inserisci password : ")
                id_filiale = seleziona_filiale(banca)
                print("\n")
                if id_filiale :
                    if banca.crea_cliente(nome,cognome,cf,email,password,id_filiale):
                        print(f"Il cliente {nome} {cognome} è stato creato nella filiale {id_filiale}")

            case 4:
                print("\n")
                importo_iniz = float(input("Inserisci importo iniziale: "))
                id_filiale = seleziona_filiale(banca)
                print("\n")
                if id_filiale :
                    if banca.crea_sportello(id_filiale,importo_iniz):
                        print(f"Lo sportello è stato creato nella filiale {id_filiale}")

            case 5 :
                break

            case _:
                print("Scelta sbagliata.")


#menu per gli impiegati della banca
def menu_impiegati(banca, impiegato):
    while True :
        print("\n")
        print("-- Gestione Impiegati --")
        print("1. Visualizza dati personali")
        if impiegato.ruolo == "Cassiere":
            print("2. Effettua un versamento per il cliente")
            print("3. Effettua un prelievo dal conto del cliente")

        if impiegato.ruolo == "Consulente Finanziario":
            print("2. Crea nuovo Conto per il cliente")
            print("3. Crea nuova carta per il cliente")
        print("4. Logout")
        scelta = int(input(">> "))
        match scelta:
            case 1:
                informazioni = impiegato.visualizza_dati_impiegato()
                if informazioni :
                    print("Profilo impiegato : ")
                    print(f"\tNome : {informazioni['nome']} {informazioni['cognome']}")
                    print(f"\tEmail : {informazioni['email']}")
                    print(f"\tRuolo : {informazioni['ruolo']}")
                    print(f"\tFiliale : {informazioni['id_filiale']}")
                else : 
                    print("Errore")

            case 2:
                if impiegato.ruolo == "Cassiere":
                    id_conto = int(input("Inserisci l'id conto del cliente : "))
                    importo = float(input("Inserisci l'importo da versare : "))
                    impiegato.effettua_versamento(id_conto, importo)

                elif impiegato.ruolo == "Consulente Finanziario":
                    id_cliente = int(input("Inserisci l'id del cliente : "))
                    numero_conto = input("Inserisci il numero del conto : ")
                    while True :
                        tipo = input("Inserisci il tipo del conto (Conto corrente o Conto Risparmio): ").strip().lower()
                        if tipo == "conto corrente":
                            tipo_d = "Conto corrente"
                            valore = float(input("Inserisci il Limite scoperto o Fido in € : "))
                            break
                        elif tipo == "conto risparmio":
                            tipo_d = "Conto Risparmio"
                            valore = float(input("Inserisci il Tasso di interesse in % : "))
                            break
                        else :
                            print("Tipo conto sbagliato, riprova")
                    impiegato.apri_nuovo_conto(id_cliente,numero_conto,tipo_d,valore)

            case 3:
                if impiegato.ruolo == "Cassiere":
                    id_cliente = int(input("Inserisci l'id del cliente : "))
                    importo = float(input("Inserisci l'importo da prelevare : "))
                    impiegato.effettua_prelievo(id_cliente, importo)
                elif impiegato.ruolo == "Consulente Finanziario":
                    id_cliente = int(input("Inserisci Id cliente proprietario : "))
                    id_conti_clienti = impiegato.leggi_conti_clienti(id_cliente)
                    if not id_conti_clienti:
                        print("Il cliente non ha conti aperti.")
                        break
                    lista_id_validi =[]
                    for c in id_conti_clienti:
                        print(f"Id : {c['id_conto']} - {c['tipo_conto']}")
                        lista_id_validi.append(c['id_conto'])
                    id_conto = int(input("Inserisci Id conto da collegare : "))
                    if id_conto not in lista_id_validi:
                        print("Id conto non valido.")
                        break
                    numero_carta = int(input("Inserisci numero carta : "))
                    pin = int(input("Inserisci pin carta : "))
                    data_scadenza = input("Insersci data scadenza : ")
                    while True :
                        tipo = input("Inserisci il tipo di carta (Debito o Credito): ").strip().lower()
                        if tipo == "debito":
                            tipo_c = "Debito"
                            plafond_mensile = 0.0
                            break
                        elif tipo == "credito":
                            tipo_c = "Credito"
                            plafond_mensile = float(input("Inserisci il Plafond mensile in € : "))
                            break
                        else :
                            print("Tipo conto sbagliato, riprova")
                    impiegato.crea_nuova_carta(id_cliente,id_conto,numero_carta,pin,data_scadenza,tipo_c , plafond_mensile)


            case 4:
                break
            case _ :
                print("Scelta sbagliata.")

#menu per i clienti della banca
def menu_cliente(banca,cliente):
    while True :
        print("\n")
        print(f"-- Benvenuto : {cliente.nome} {cliente.cognome} --")
        print("1. Visualizza Conti e Saldi")
        print("2. Visualizza Carte intestate")
        print("3. Paga con Carta")
        print("4. Esegui bonifico")
        print("5. Leggi notifiche")
        print("6. Logout")
        scelta = int(input(">> "))
        match scelta :
            case 1 : 
                conti = cliente.recupera_conti()
                if not conti:
                    print("Non esistono conti per questo cliente.")
                else :
                    print("-- Conti aperti --")
                    conto_tmp = Conto(None,None,None)
                    for c in conti:
                        id_conto = c['id_conto']
                        tipo_conto = c['tipo_conto']
                        if tipo_conto  == "Conto corrente" :
                            conto_tmp = Conto_corrente(c['numero_conto'], c['id_cliente'], c['limite_scoperto'])
                            saldo_r = conto_tmp.visualizza_saldo(id_conto)
                            saldo_d = conto_tmp.visualizza_saldo_spendibile(id_conto)
                            print(f"\tNumero conto : {c['numero_conto']}")
                            print(f"\tTipo conto : {c['tipo_conto']}")
                            print(f"\tSaldo Reale : {saldo_r} € ")
                            print(f"\tSaldo disponibile : {saldo_d} € ")
                            print("\n")
                        elif tipo_conto  == "Conto Risparmio" :
                            conto_tmp = Conto_risparmio(c['numero_conto'], c['id_cliente'], c['tasso_interesse'])
                            saldo = conto_tmp.visualizza_saldo(id_conto)
                            print(f"\tNumero conto : {c['numero_conto']}")
                            print(f"\tTipo conto : {c['tipo_conto']}")
                            print(f"\tSaldo Reale : {saldo} € ")
                            print("\n")

            case 2 :
                print("\n-- Le tue carte --")
                carte = cliente.recupera_carte()
                if not carte :
                    print("Non ci sono carte associate al cliente")
                    break
                else :
                    carte = cliente.recupera_carte()
                    if not carte :
                        print("Non ci sono carte associate al cliente")
                        break
                    for c in carte :
                        stringa_plafond = ""
                        if "Credito" in c['tipo_carta']:
                            carta_tmp = CartaDiCredito( 
                                c['id_carta'], 
                                c['numero_carta'], 
                                c['pin_hash'], 
                                c['id_conto_collegato'], 
                                c['id_cliente'], 
                                c['data_scadenza'], 
                                c['plafond_mensile']
                            )
                            residuo = carta_tmp.get_plafond_residuo()
                            stringa_plafond = f" - Plafond Residuo : {residuo} € "
                        print(f"Id : {c['id_carta']} - {c['tipo_carta']} - Numero : {c['numero_carta']} {stringa_plafond}")
                    
            case 3 :
                print("-- Le tue carte --")
                facade = ClienteFacade(cliente)
                print("\n-- PAGA CON CARTA --")
                carte_disponibili = facade.get_carte_formattate()
                if not carte_disponibili:
                    print("Non hai carte abilitate per i pagamenti.")
                else:
                    for c in carte_disponibili:
                        info_extra = c.get_info_per_stampa()
                        print(f"ID: {c.id_carta} - {c.tipo_carta} - Num: {c.numero_carta}{info_extra}")

                totale = facade.get_saldo_totale_patrimonio()
                print(f"Patrimonio Totale: {totale} €")
                print("\n")
                id_c = int(input("Id Carta: "))
                pin = input("PIN: ")
                imp = float(input("Importo: "))
                
                esito = facade.paga_con_carta_facile(id_c, pin, imp)
                print(f"Esito: {esito}")

            case 4 :
                print("\n-- Nuovo Bonifico -- ")
                conti = cliente.recupera_conti()
                if not conti:
                    print("Non ci sono conti aperti .")
                    break
                lista_id_conti = []
                for c in conti :
                    lista_id_conti.append(c['id_conto'])

                print("Seleziona un id conto da cui effettuare il bonifico :")
                print(lista_id_conti)
                id_sorgente = int(input("Seleziona Id conto : "))
                if id_sorgente not in lista_id_conti :
                    print("Non puoi effettuare il bonifico da un conto non tuo . ")
                    break

                id_destinatario = int(input("Inserisci Id conto destinatario : "))
                importo = float(input("Importo : "))
                causale = input("Inserisci Causale : ")
                bonifico = Bonifico(id_sorgente,importo,causale,id_destinatario)
                bonifico.esegui_bonifico()

            case 5: 
                notifiche = cliente.leggi_notifiche()
                print("\n -- Notifiche -- ")
                if not notifiche:
                    print("Non ci sono notifiche.")
                else :
                    for n in notifiche:
                        print(f"{n['messaggio']} in data : {n['data_creazione']}")

            case 6: 
                break

            case _:
                print("Scelta sbagliata.")

#menu per lo sportello ATM
def menu_sportello(banca,cliente):
    print("\n-- Sportello ATM --")
    id_atm_selezionato = seleziona_atm(banca)
    connection = mysql.connector.connect(**DB_CONNNESIONE)
    cursor = connection.cursor(dictionary=True)
    try:
        sql = f"SELECT * FROM sportelli_atm WHERE id_atm = {id_atm_selezionato}"
        cursor.execute(sql)
        dati_atm = cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Errore: {err}")
        return
    finally:
        cursor.close()
        connection.close()

    atm_ogg = Sportello_atm(
        dati_atm['id_atm'], 
        dati_atm['stato_atm'], 
        dati_atm['id_filiale'], 
        dati_atm['importo_disponibile']
    )

    if atm_ogg.stato_atm != "Attivo":
        print("\nSportello fuori servizio.")
        return
    
    print("\nCliente connesso allo sportello. Inserire la carta ...")
    id_carta = int(input("Inserisci Id carta : "))
    pin = input("Inserisci pin carta : ")
    carta_selezionata = atm_ogg.login(id_carta,pin)
    if not carta_selezionata:
        return
    
    while True :
        print("\n -- Menu Sportello Atm --")
        print("1. Prelievo Contanti")
        print("2. Visualizza Saldo")
        print("3. Logout(Restituisci carta)")
        scelta = int(input(">> "))
        match scelta:
            case 1: 
                importo = float(input("Inserisci l'importo da prelevare : "))
                if atm_ogg.prelievo_atm(carta_selezionata,importo):
                    print("Prelieva l'importo selezionato in contanti")
                else:
                    print("Operazione fallita")

            case 2 :
                conto_tmp = Conto(None,None,None)
                saldo = conto_tmp.visualizza_saldo(carta_selezionata.id_conto)
                print(f"\nIl tuo saldo attuale è : {saldo} €")

            case 3:
                print("Grazie per aver utilizzato lo sportello. Ritirare la carta .")
                break

            case _:
                print("Scelta sbagliata.")

#main principale che gestisce il flusso del programma
if __name__ == "__main__":
    mia_banca = Banca("Banca 1")
    while True :
        print("\n-- Benvenuto nella Banca --")
        print("1. Menu Impiegati")
        print("2. Menu Clienti")
        print("3. Sportello Atm")
        print("4. Logout")
        scelta = int(input(">> "))
        match scelta :
            case 1 :
                print("\n -- Menu Impiegati --")
                print("Inserisci le credenziali per entrare : ")
                email = input("Email : ")
                password = input("Password : ")
                if mia_banca.login("Impiegato",email,password):
                    utente = mia_banca.utente_corrente
                    if utente.ruolo == "Amministratore":
                        menu_admin(mia_banca)
                    else :
                        menu_impiegati(mia_banca,utente)

                    mia_banca.logout()
                else :
                    print("Email o password sbagliati.")
            
            case 2 :
                print("\n-- Menu Clienti -- ")
                print("Inserisci le credenziali per entrare : ")
                email = input("Email : ")
                password = input("Password : ")
                if mia_banca.login("Cliente", email,password):
                    cliente = mia_banca.utente_corrente
                    menu_cliente(mia_banca,cliente)
                    mia_banca.logout()
                else :
                    print("Email o password sbagliati.")

            case 3:
                menu_sportello(mia_banca, None)

            case 4 :
                print("Chiusura totale del sistema .")
                break

            case _:
                print("Scelta sbagliata.")