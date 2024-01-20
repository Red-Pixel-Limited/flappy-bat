# Flappy Bat

![bat](./images/bat_mid.png)

## Setup 

### Setup Database

To create database
```bash
cd db
sqlite3 -init schema.sql players.db .quit
```

### Activate Environment

#### Unix

```bash
 source .venv/bin/activate                 
 python3 -m pip install -r requirements.txt
```

#### Windows

TBD

### Deactivate Environment

#### Unix

To close environment
```bash
deactivate
```
To remove environment
```bash
rm -rf venv
```

#### Windows

TBD
