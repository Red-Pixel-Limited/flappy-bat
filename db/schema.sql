CREATE TABLE settings(
    id INTEGER PRIMARY KEY NOT NULL,
    volume INTEGER NOT NULL DEFAULT 100
);

CREATE TABLE players (
    username TEXT PRIMARY KEY NOT NULL,
    password BLOB NOT NULL,
    salt BLOB NOT NULL,
    scores INTEGER NOT NULL DEFAULT 0,
    settings_id INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (settings_id) 
        REFERENCES settings(id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

INSERT INTO settings (id) VALUES (1);
