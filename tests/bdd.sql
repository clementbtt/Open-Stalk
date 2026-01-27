CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,      
    password_hash TEXT NOT NULL                     
);

CREATE TABLE IF NOT EXISTS campagnes (
    campagne_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    titre          TEXT NOT NULL,
    date_creation  DATETIME NOT NULL DEFAULT (datetime('now')),
    owner_id       INTEGER NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(user_id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS types_sources (
    type_source_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom            TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS types_entites (
    type_entite_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom            TEXT NOT NULL 
);

CREATE TABLE IF NOT EXISTS sujets_recherche (
    sujet_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    libelle      TEXT NOT NULL,
    campagne_id  INTEGER NOT NULL,
    date_ajout   DATETIME DEFAULT (datetime('now')),
    FOREIGN KEY (campagne_id) REFERENCES campagnes(campagne_id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS sources (
    source_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    type_source        INTEGER NOT NULL, 
    url                TEXT NOT NULL,    
    sujet_id           INTEGER, 
    campagne_id        INTEGER NOT NULL,
    FOREIGN KEY (sujet_id) REFERENCES sujets_recherche(sujet_id) ON DELETE CASCADE,
    FOREIGN KEY (campagne_id) REFERENCES campagnes(campagne_id) ON DELETE CASCADE,
    FOREIGN KEY (type_source) REFERENCES types_sources(type_source_id)
);


CREATE TABLE IF NOT EXISTS entites (
    entite_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    element         TEXT NOT NULL,             
    type_osint_id   INTEGER NOT NULL,          
    niveau_confiance INTEGER DEFAULT 100,
    UNIQUE (element, type_osint_id),     
    FOREIGN KEY (type_osint_id) REFERENCES types_entites(type_entite_id)
);


CREATE TABLE IF NOT EXISTS artefacts (
    artefact_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id       INTEGER NOT NULL,          
    date_collecte   DATETIME NOT NULL DEFAULT (datetime('now')),
    url             TEXT,                      
    contenu_brut    TEXT,
    contenu_hash    TEXT,
    status_code     INTEGER,
    headers         TEXT,                   
    FOREIGN KEY (source_id) REFERENCES sources(source_id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS relations (
    relation_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    artefact_id     INTEGER NOT NULL,
    entite_id       INTEGER NOT NULL,
    contexte_extrait TEXT,                   
    FOREIGN KEY (artefact_id) REFERENCES artefacts(artefact_id) ON DELETE CASCADE,
    FOREIGN KEY (entite_id) REFERENCES entites(entite_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS audit_logs (
    log_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER,
    username        TEXT,
    action          TEXT NOT NULL,
    campaign_name   TEXT,
    target_details  TEXT,
    ip_address      TEXT,
    timestamp       DATETIME DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
);

INSERT INTO types_sources (nom) VALUES ('GitHub API'); 
INSERT INTO types_sources (nom) VALUES ('Wikipedia');  
INSERT INTO types_sources (nom) VALUES ('Personnal URL');  
INSERT INTO types_sources (nom) VALUES ('Personnal File');

INSERT INTO types_entites (nom) VALUES ('email');      
INSERT INTO types_entites (nom) VALUES ('pseudo');  
INSERT INTO types_entites (nom) VALUES ('twitter');
INSERT INTO types_entites (nom) VALUES ('instagram');
INSERT INTO types_entites (nom) VALUES ('website');  
INSERT INTO types_entites (nom) VALUES ('ip');
INSERT INTO types_entites (nom) VALUES ('facebook');
