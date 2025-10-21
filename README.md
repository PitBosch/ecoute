# Ecoute - Riconoscimento Vocale Multilingue

Ecoute è un'applicazione di riconoscimento vocale in tempo reale che supporta multiple lingue, inclusa l'italiano. L'applicazione può trascrivere sia l'audio dal microfono che l'audio riprodotto dagli altoparlanti del sistema.

## Caratteristiche

- **Supporto Multilingue**: Italiano, Inglese, Spagnolo, Francese, Tedesco, Portoghese, Hindi, Olandese
- **Riconoscimento in Tempo Reale**: Trascrizione simultanea di microfono e altoparlanti
- **Interfaccia Grafica Moderna**: UI intuitiva con PyQt6 e CustomTkinter
- **Modelli Avanzati**: 
  - 🚀 **Voxtral-Mini-3B-2507** (Nuovo!) - Comprensione audio avanzata
  - Faster Whisper locali
  - OpenVINO Whisper ottimizzato 
  - OpenAI Whisper API
  - Ollama Whisper
- **Cambio Lingua Dinamico**: Possibilità di cambiare lingua durante l'uso
- **Database Locale**: Salvataggio automatico delle trascrizioni

## Installazione

1. **Clona il repository**:
   ```bash
   git clone <repository-url>
   cd ecoute
   ```

2. **Installa le dipendenze**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Installa FFmpeg** (richiesto per l'elaborazione audio):
   - **Windows**: Scarica da [ffmpeg.org](https://ffmpeg.org/download.html) e aggiungi al PATH
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

## Utilizzo

### 🚀 Con Voxtral-Mini-3B (Nuovo!)
```bash
# Setup automatico
python setup_voxtral.py

# Interfaccia moderna (consigliata)
python run_modern.py --voxtral

# Interfaccia classica
python main.py --voxtral
```
*Nota: Richiede GPU con 10GB+ VRAM per prestazioni ottimali*

### Avvio Base (FasterWhisper)
```bash
# Interfaccia moderna
python run_modern.py

# Interfaccia classica
python main.py
```

### Con OpenVINO (Ottimizzato CPU)
```bash
python run_modern.py --openvino
```

### Con Ollama
```bash
python main.py --ollama
```
*Nota: Richiede Ollama installato da https://ollama.ai*

### Con OpenAI API
```bash
python run_modern.py --api
```
*Nota: Richiede una chiave API OpenAI configurata nell'ambiente*

### Controlli dell'Interfaccia

- **Menu Lingua**: Seleziona la lingua per il riconoscimento vocale
- **Area Trascrizione**: Visualizza le trascrizioni in tempo reale
- **Pulsante "Cancella Trascrizione"**: Pulisce la cronologia delle trascrizioni

## Lingue Supportate

### Voxtral-Mini-3B (Supporto Nativo)
- 🇮🇹 **Italiano** (it) - Eccellente
- 🇺🇸 **Inglese** (en) - Eccellente  
- 🇪🇸 **Spagnolo** (es) - Eccellente
- 🇫🇷 **Francese** (fr) - Eccellente
- 🇩🇪 **Tedesco** (de) - Eccellente
- 🇵🇹 **Portoghese** (pt) - Eccellente
- 🇮🇳 **Hindi** (hi) - Eccellente
- 🇳🇱 **Olandese** (nl) - Eccellente

### Altri Modelli (100+ lingue)
Tutti gli altri modelli supportano 100+ lingue tramite Whisper

## Modelli di Trascrizione

### 1. **Ollama Whisper** ⭐ **RACCOMANDATO**
- **Velocità**: Molto veloce
- **Accuratezza**: Alta
- **Costo**: Gratuito
- **Requisiti**: Ollama installato
- **Comando**: `python main.py --ollama`

### 2. **Faster Whisper** (Default)
- **Velocità**: Media
- **Accuratezza**: Buona
- **Costo**: Gratuito
- **Requisiti**: GPU opzionale
- **Comando**: `python main.py`

### 3. **OpenAI Whisper API**
- **Velocità**: Alta
- **Accuratezza**: Molto alta
- **Costo**: $0.006/minuto
- **Requisiti**: Chiave API
- **Comando**: `python main.py --api`

## Configurazione

### Variabili d'Ambiente

Per utilizzare l'API OpenAI:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Parametri Audio

I parametri di registrazione possono essere modificati in `AudioRecorder.py`:
- `RECORD_TIMEOUT`: Timeout per la registrazione (default: 3 secondi)
- `ENERGY_THRESHOLD`: Soglia di energia per il rilevamento vocale
- `DYNAMIC_ENERGY_THRESHOLD`: Soglia dinamica abilitata/disabilitata

## Struttura del Progetto

```
ecoute/
├── main.py                 # Punto di ingresso principale
├── AudioRecorder.py        # Gestione registrazione audio
├── AudioTranscriber.py     # Trascrizione audio
├── TranscriberModels.py    # Modelli di riconoscimento vocale
├── custom_speech_recognition/  # Libreria personalizzata
└── requirements.txt        # Dipendenze Python
```

## Risoluzione Problemi

### Errore "pyaudiowpatch could not be resolved"
Assicurati di aver installato PyAudioWPatch:
```bash
pip install PyAudioWPatch
```

### Errore FFmpeg
Verifica che FFmpeg sia installato e accessibile dal PATH:
```bash
ffmpeg -version
```

### Problemi di Performance
- Per migliori performance, utilizza una GPU CUDA
- Il modello "base" è più accurato ma più lento del modello "tiny"

## 📚 Documentazione Aggiuntiva

- 🎙️ **[Guida Voxtral](README_VOXTRAL.md)** - Setup e utilizzo del modello Voxtral-Mini-3B-2507
- 🔧 **[Guida OpenVINO](README_OPENVINO.md)** - Ottimizzazione CPU con Intel OpenVINO
- 🎯 **[Interfaccia Moderna](README_MODERN.md)** - Guida all'interfaccia PyQt6

## Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file `LICENSE` per i dettagli.

## Contributi

I contributi sono benvenuti! Per favore:
1. Fai un fork del progetto
2. Crea un branch per la tua feature
3. Committa le modifiche
4. Apri una Pull Request

## Supporto

Per problemi o domande, apri una issue su GitHub.
