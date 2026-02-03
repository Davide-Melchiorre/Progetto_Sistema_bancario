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

if __name__ == "__main__":
    creazione_tabelle()