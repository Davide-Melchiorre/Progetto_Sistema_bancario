import mysql.connector
from connessione_db import DB_CONNNESIONE 

# crea le tabelle necessarie nel database
def creazione_tabelle():
    try:
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS filiali (
            id_filiale INT AUTO_INCREMENT PRIMARY KEY,
            codice_filiale VARCHAR(20) UNIQUE NOT NULL,
            indirizzo VARCHAR(255) NOT NULL
        ) ENGINE=InnoDB;
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clienti (
            id_cliente INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            cognome VARCHAR(100) NOT NULL,
            codice_fiscale VARCHAR(16) UNIQUE NOT NULL,
            email VARCHAR(100),
            password_hash VARCHAR(255) NOT NULL,
            id_filiale INT,
            data_registrazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_filiale) REFERENCES filiali(id_filiale)
        ) ENGINE=InnoDB;
        """)
        print("Tabella 'clienti' creata.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS impiegati (
            id_impiegato INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            cognome VARCHAR(100) NOT NULL,
            email VARCHAR(100),
            ruolo VARCHAR(50) NOT NULL,
            id_filiale INT,
            password_hash VARCHAR(255) NOT NULL,
            FOREIGN KEY (id_filiale) REFERENCES filiali(id_filiale)
        ) ENGINE=InnoDB;
        """)
        print("Tabella 'impiegati' creata.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS conti (
            id_conto INT AUTO_INCREMENT PRIMARY KEY,
            numero_conto VARCHAR(50) UNIQUE NOT NULL,
            tipo_conto VARCHAR(20) NOT NULL,
            id_cliente INT NOT NULL,
            limite_scoperto DECIMAL(10, 2) DEFAULT 0,
            tasso_interesse DECIMAL(5, 2) DEFAULT 0,
            data_apertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_cliente) REFERENCES clienti(id_cliente)
        ) ENGINE=InnoDB;
        """)
        print("Tabella 'conti' creata.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS carte (
            id_carta INT AUTO_INCREMENT PRIMARY KEY,
            numero_carta VARCHAR(20) UNIQUE NOT NULL,
            pin_hash VARCHAR(255) NOT NULL,
            tipo_carta VARCHAR(20) NOT NULL,
            id_conto_collegato INT NOT NULL,
            id_cliente INT NOT NULL,
            plafond_mensile DECIMAL(10, 2) DEFAULT 0,
            data_scadenza VARCHAR(10),
            FOREIGN KEY (id_conto_collegato) REFERENCES conti(id_conto),
            FOREIGN KEY (id_cliente) REFERENCES clienti(id_cliente)
        ) ENGINE=InnoDB;
        """)
        print("Tabella 'carte' creata.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transazioni (
            id_transazione INT AUTO_INCREMENT PRIMARY KEY,
            id_conto_sorgente INT NOT NULL,
            id_carta INT,
            importo DECIMAL(10, 2) NOT NULL,
            tipo_transazione VARCHAR(50) NOT NULL,
            descrizione VARCHAR(255),
            data_ora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_conto_sorgente) REFERENCES conti(id_conto),
            FOREIGN KEY (id_carta) REFERENCES carte(id_carta)
        ) ENGINE=InnoDB;
        """)
        print("Tabella 'transazioni' creata.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifiche (
            id_notifica INT AUTO_INCREMENT PRIMARY KEY,
            id_cliente INT NOT NULL,
            messaggio TEXT NOT NULL,
            data_creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (id_cliente) REFERENCES clienti(id_cliente)
        ) ENGINE=InnoDB;
        """)
        print("Tabella 'notifiche' creata.")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sportelli_atm (
            id_atm INT AUTO_INCREMENT PRIMARY KEY,
            id_filiale INT NOT NULL,
            stato_atm VARCHAR(30) NOT NULL,
            importo_disponibile DECIMAL(10, 2) NOT NULL,
            FOREIGN KEY (id_filiale) REFERENCES filiali(id_filiale)
        ) ENGINE=InnoDB;
        """)
        print("Tabella 'sportelli_atm' creata.")

        #sql_admin = """
           # INSERT INTO impiegati (nome, cognome, email, ruolo, id_filiale, password_hash)
            #VALUES ('Davide', 'Melchiorre', 'admin@banca.it', 'Amministratore', NULL, 'Superadmin123')
            #"""
        #cursor.execute(sql_admin)        
        connection.commit()
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Errore: {err}")

def inserimento_dati():
    try:
        connection = mysql.connector.connect(**DB_CONNNESIONE)
        cursor = connection.cursor()
        sql_filiali = """
        INSERT INTO filiali (codice_filiale, indirizzo) VALUES 
        ('RM001', 'Via del Corso 10, Roma'),
        ('MI001', 'Piazza Duomo 5, Milano'),
        ('NA001', 'Via Toledo 20, Napoli');
        """
        cursor.execute(sql_filiali)
        sql_impiegati = """
        INSERT INTO impiegati (nome, cognome, email, ruolo, id_filiale, password_hash) VALUES 
        ('Davide', 'Melchiorre', 'admin@banca.it', 'Amministratore', NULL, 'admin123'),
        ('Luca', 'Bianchi', 'luca.cassiere@banca.it', 'Cassiere', 1, 'prova123'),
        ('Anna', 'Verdi', 'anna.consulente@banca.it', 'Consulente Finanziario', 2, 'prova123');
        """
        cursor.execute(sql_impiegati)

        sql_clienti = """
        INSERT INTO clienti (nome, cognome, codice_fiscale, email, password_hash, id_filiale) VALUES 
        ('Mario', 'Rossi', 'RSSMRA80A01H501U', 'mario.rossi@email.com', 'Prova123, 1),
        ('Giulia', 'Neri', 'NREGLL90B02F205Z', 'giulia.neri@email.com', 'password234', 2);
        """
        cursor.execute(sql_clienti)
        sql_conti = """
        INSERT INTO conti (numero_conto, tipo_conto, id_cliente, limite_scoperto, tasso_interesse) VALUES 
        ('IT010000001', 'Conto corrente', 1, 1000.00, 0),
        ('IT010000002', 'Conto Risparmio', 1, 0, 2.5),
        ('IT020000001', 'Conto corrente', 2, 500.00, 0);
        """
        cursor.execute(sql_conti)
        sql_carte = """
        INSERT INTO carte (numero_carta, pin_hash, tipo_carta, id_conto_collegato, id_cliente, plafond_mensile, data_scadenza) VALUES 
        ('1234567891234456', '123', 'Debito', 1, 1, 0, '12/28'),
        ('7264849502847493', '456', 'Credito', 1, 1, 3000.00, '12/29'),
        ('9274957364837495', '789', 'Debito', 3, 2, 0, '05/27');
        """
        cursor.execute(sql_carte)
        sql_atm = """
        INSERT INTO sportelli_atm (id_filiale, stato_atm, importo_disponibile) VALUES 
        (1, 'Attivo', 50000.00),
        (2, 'Fuori Servizio', 0.00);
        """
        cursor.execute(sql_atm)
        sql_transazioni = """
        INSERT INTO transazioni (id_conto_sorgente, id_carta, importo, tipo_transazione, descrizione) VALUES 
        (1, NULL, 1000.00, 'Bonifico Entrata', 'Stipendio'),
        (1, 1, -50.00, 'Pagamento POS', 'Spesa Supermercato'),
        (1, NULL, -100.00, 'Bonifico Uscita', 'Regalo');
        """
        cursor.execute(sql_transazioni)
        connection.commit()
        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Errore: {err}")

if __name__ == "__main__":
    creazione_tabelle()
    #inserimento_dati()