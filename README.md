# CSV to Calendar

---

- Versione: 1.3

---

- [CSV to Calendar](#csv-to-calendar)
  - [Descrizione](#descrizione)
  - [Requisiti](#requisiti)
    - [Dipendenze Python](#dipendenze-python)
    - [File richiesti](#file-richiesti)
  - [Utilizzo](#utilizzo)
    - [Passaggi](#passaggi)
    - [File ics](#file-ics)
  - [Gestione degli errori](#gestione-degli-errori)
  - [Personalizzazioni](#personalizzazioni)
    - [Cambiare il delimitatore del CSV](#cambiare-il-delimitatore-del-csv)
    - [Cambiare il fuso orario](#cambiare-il-fuso-orario)
  - [Esempio di esecuzione](#esempio-di-esecuzione)
    - [Input](#input)
    - [Output](#output)
  - [Changelog](#changelog)

## Descrizione

<!-- markdownlint-disable MD033 -->
<div align=center>

![logo](./logo.png)

</div>

---

Questo script converte un file CSV contenente eventi in un file ICS compatibile con applicazioni calendario (Google Calendar, Apple Calendar, etc.). Lo script utilizza un file JSON per definire gli orari dei turni associati agli eventi.

---

## Requisiti

### Dipendenze Python

Le seguenti librerie sono necessarie:

- **ics**: per generare il file ICS
- **pytz**: per gestire i fusi orari

Installa le dipendenze con:

```bash
pip install -r requirements
```

### File richiesti

1. **CSV degli eventi**
   - Nome: `events.csv`
   - Formato:
     - Separatore: `;`
     - Colonne:
       1. Nome evento
       2. Data (formato: `DD/MM/YY`)
       3. Nome turno
   - Esempio:
  
     ```csv
     Evento 1;17/12/24;Mattina
     Evento 2;18/12/24;Pomeriggio
     Evento 3;19/12/24;Notturno
     ```

2. **JSON dei turni**
   - Nome: `shifts.json`
   - Formato:
     - Chiave: Nome turno
     - Valore: Orario (formato: `HH:MM - HH:MM`)
   - Esempio:

     ```json
     {
         "Mattina": "06:00 - 14:00",
         "Pomeriggio": "14:00 - 22:00",
         "Notturno": "22:00 - 06:00"
     }
     ```

---

## Utilizzo

### Passaggi

1. **Assicurati che i file richiesti siano presenti**
   - `events.csv` e `shifts.json` devono trovarsi nella stessa directory dello script.

2. **Esegui lo script**

   ```bash
   python main.py
   ```

3. **Risultato**
   - Verrà generato un file `calendar.ics` nella stessa directory dello script.

### File ics

Il file `calendar.ics` conterrà tutti gli eventi definiti nel CSV, con gli orari calcolati dai turni definiti nel JSON.

---

## Gestione degli errori

- **Turno non trovato**:
  
  - Messaggio di avviso:

    ```bash
    Warning: Shift 'Turno Non Esistente' not found in shifts.json. Skipping event 'Evento'.
    ```

  - Assicurati che tutti i turni nel CSV siano presenti in `shifts.json`.

- **File mancante**:
  - Messaggio di errore:

    ```bash
    Error: events.csv not found in the current directory.
    ```

  - Verifica che il file indicato sia nella directory corretta.

---

## Personalizzazioni

### Cambiare il delimitatore del CSV

Se il file CSV utilizza un delimitatore diverso (es. `,`):

1. Modifica questa riga nel file `main.py`:

   ```python
   reader = csv.reader(file, delimiter=';')
   ```

   con:

   ```python
   reader = csv.reader(file, delimiter=',')
   ```

### Cambiare il fuso orario

Il fuso orario è configurato su `Europe/Rome`. Per modificarlo:

1. Modifica questa riga:

   ```python
   local_timezone = pytz.timezone("Europe/Rome")
   ```

   con il fuso orario desiderato (es. `UTC` o `America/New_York`).

---

## Esempio di esecuzione

### Input

**CSV (`events.csv`)**:

```csv
Evento 1;17/12/24;Mattina
Evento 2;18/12/24;Pomeriggio
Evento 3;19/12/24;Notturno
```

**JSON (`shifts.json`)**:

```json
{
    "Mattina": "06:00 - 14:00",
    "Pomeriggio": "14:00 - 22:00",
    "Notturno": "22:00 - 06:00"
}
```

### Output

**ICS (`calendar.ics`)**:
Un evento nel formato ICS:

```ics
BEGIN:VEVENT
SUMMARY:Evento 1
DTSTART:20241217T060000
DTEND:20241217T140000
END:VEVENT
```

---

## Changelog

- 05/12/2024 : Creazione Script. -> Versione 1.0
- 06/12/2024 : Miglioramento dello script. -> Versione 1.1
- 06/12/2024 : Risolti problemi sulle turnazioni notturne. -> Versione 1.2
- 06/12/2024 : Bug Fix -> Versione 1.2.1
- 29/12/2024 : Migliorata compatibilità con Google Calendar. -> Versione 1.3

---

Se hai bisogno di ulteriori dettagli o modifiche, non esitare a chiedere!
