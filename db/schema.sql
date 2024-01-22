CREATE TABLE settings(
    id INTEGER PRIMARY KEY NOT NULL,
    volume INTEGER NOT NULL DEFAULT 100,
    lift_key TEXT NOT NULL DEFAULT 'Space'
);

CREATE TABLE players (
    username TEXT PRIMARY KEY NOT NULL,
    lower_username TEXT NOT NULL,
    password BLOB NOT NULL,
    salt BLOB NOT NULL,
    scores INTEGER NOT NULL DEFAULT 0,
    settings_id INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (settings_id) 
        REFERENCES settings(id)
            ON DELETE CASCADE
            ON UPDATE NO ACTION
);

CREATE INDEX lower_cased_username_index ON players (lower_username);

INSERT INTO settings (id) VALUES (1);
