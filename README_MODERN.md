# 🎙️ Ecoute Modern - Trascrizioni Audio Avanzate

Una versione moderna e migliorata di Ecoute con interfaccia PyQt6 e database SQLite per la gestione delle trascrizioni.

## ✨ Nuove Funzionalità

### 🎨 Interfaccia Moderna
- **Design Dark Mode**: Interfaccia moderna con tema scuro
- **Layout Responsive**: Sidebar con lista trascrizioni e area principale
- **Toolbar Integrata**: Accesso rapido alle funzioni principali
- **Status Bar**: Feedback in tempo reale sullo stato dell'app

### 💾 Gestione Database
- **SQLite Locale**: Database integrato per salvare le trascrizioni
- **Auto-Save**: Salvataggio automatico durante la trascrizione
- **Cronologia**: Accesso a tutte le trascrizioni precedenti
- **Ricerca**: Trova rapidamente le trascrizioni salvate

### 🔧 Miglioramenti Tecnici
- **Bug Fix**: Risolto l'errore di cambio lingua
- **Performance**: Interfaccia più fluida e reattiva
- **Stabilità**: Gestione migliorata degli errori

## 🚀 Avvio Rapido

### Versione Moderna (Consigliata)
```bash
python run_modern.py
```

### Versione Classica (Fallback)
```bash
python main.py
```

## 📋 Requisiti

### Dipendenze Python
```bash
pip install PyQt6 sqlalchemy
```

### Dipendenze Sistema
- **FFmpeg**: Necessario per l'elaborazione audio
- **Python 3.8+**: Versione minima supportata

## 🎯 Come Usare

### 1. Avvio dell'App
- Lancia `run_modern.py` per l'interfaccia moderna
- L'app creerà automaticamente il database SQLite

### 2. Trascrizione in Tempo Reale
- La registrazione si avvia automaticamente
- Parla nel microfono o riproduci audio
- La trascrizione apparirà in tempo reale

### 3. Gestione Trascrizioni
- **Salva**: Clicca "💾 Salva" per salvare la trascrizione
- **Titolo**: Inserisci un titolo personalizzato
- **Lingua**: Cambia lingua dal menu a tendina
- **Cronologia**: Clicca su una trascrizione nella sidebar per caricarla

### 4. Funzioni Avanzate
- **Cancella**: Pulisce la trascrizione corrente
- **Esporta**: Esporta in vari formati (in sviluppo)
- **Ricerca**: Cerca nelle trascrizioni salvate

## 🔧 Configurazione

### Lingue Supportate
- 🇮🇹 Italiano (`it`)
- 🇬🇧 Inglese (`en`)
- 🇪🇸 Spagnolo (`es`)
- 🇫🇷 Francese (`fr`)
- 🇩🇪 Tedesco (`de`)

### Modelli di Trascrizione
- **Faster Whisper**: Modello locale predefinito
- **OpenAI API**: Usa `--api` per l'API OpenAI
- **Ollama**: Usa `--ollama` per Ollama Whisper

## 🐛 Risoluzione Problemi

### Errore "str object has no attribute get_transcription"
✅ **Risolto** nella versione moderna!

### FFmpeg non trovato
```bash
# Windows (con chocolatey)
choco install ffmpeg

# macOS (con homebrew)
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt install ffmpeg
```

### Dipendenze PyQt6
```bash
pip install PyQt6 PyQt6-tools
```

## 📁 Struttura Database

Il database SQLite (`ecoute.db`) contiene:
- **transcriptions**: Trascrizioni salvate
- **folders**: Organizzazione in cartelle (futuro)

## 🔮 Roadmap

### Prossime Funzionalità
- [ ] **Cartelle**: Organizzazione gerarchica delle trascrizioni
- [ ] **Esportazione**: PDF, DOCX, TXT
- [ ] **Ricerca Avanzata**: Filtri per data, lingua, contenuto
- [ ] **Backup**: Esportazione/importazione del database
- [ ] **Temi**: Tema chiaro e personalizzazioni
- [ ] **Hotkeys**: Scorciatoie da tastiera
- [ ] **Plugin**: Sistema di estensioni

### Miglioramenti Tecnici
- [ ] **Drag & Drop**: Spostamento trascrizioni
- [ ] **Auto-backup**: Backup automatico
- [ ] **Cloud Sync**: Sincronizzazione cloud
- [ ] **Real-time Collaboration**: Collaborazione in tempo reale

## 🤝 Contributi

Contributi benvenuti! Apri un issue o una pull request per:
- Bug fixes
- Nuove funzionalità
- Miglioramenti UI/UX
- Documentazione

## 📄 Licenza

Vedi file `LICENSE` per dettagli.

---

**Buona trascrizione! 🎙️✨** 