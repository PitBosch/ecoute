# OpenVINO Whisper Integration

## Descrizione

Questa implementazione integra il modello **OpenVINO distil-whisper-large-v3-int8-ov** nel progetto Ecoute, offrendo trascrizioni audio ottimizzate e performanti.

## Caratteristiche

- ✅ **Modello ottimizzato**: Utilizza il modello OpenVINO compresso INT8 per prestazioni superiori
- ✅ **Supporto multilingue**: Supporta italiano, inglese, spagnolo, francese e tedesco
- ✅ **Resampling automatico**: Converte automaticamente qualsiasi sample rate (48kHz, 44.1kHz, ecc.) a 16kHz richiesto da Whisper
- ✅ **Efficienza energetica**: Ottimizzato per CPU con consumi ridotti
- ✅ **Compatibilità**: Integrato con l'architettura esistente di Ecoute
- ✅ **Fallback intelligente**: Usa librosa (preferito) o scipy per il resampling audio

## Installazione

### Passo 1: Installare le dipendenze

```bash
pip install -r requirements.txt
```

Le nuove dipendenze includono:
- `optimum[openvino]>=1.23.0`
- `transformers>=4.30.0`
- `datasets>=2.14.0`
- `soundfile>=0.12.0`

### Passo 2: Test dell'installazione

```bash
python test_openvino.py
```

## Utilizzo

### Interfaccia a riga di comando

Avvia Ecoute con il modello OpenVINO:

```bash
python main.py --openvino
```

### Interfaccia moderna

```bash
python run_modern.py
```

*Nota: L'interfaccia moderna attualmente usa il modello predefinito. Il supporto per la selezione del modello nell'UI sarà aggiunto in futuro.*

### Utilizzo programmatico

```python
import TranscriberModels

# Crea un trascrittore OpenVINO
model = TranscriberModels.get_model(
    use_api=False,
    language="it",
    use_ollama=False,
    use_openvino=True
)

# Trascrivi un file audio
transcription = model.get_transcription("path/to/audio.wav")
print(transcription)
```

## Prestazioni

### Vantaggi del modello OpenVINO

- **Velocità**: Fino a 3x più veloce del modello standard
- **Memoria**: Utilizzo ridotto di memoria RAM
- **CPU**: Ottimizzato per processori Intel (ma funziona su tutti i processori)
- **Accuratezza**: Mantiene alta accuratezza con compressione INT8

### Confronto modelli

| Modello | Velocità | Memoria | Accuratezza | Uso consigliato |
|---------|----------|---------|-------------|------------------|
| OpenVINO | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Produzione |
| Faster Whisper | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Sviluppo |
| API | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Cloud |
| Ollama | ⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | Locale |

## Supporto lingue

Il modello supporta le seguenti lingue:

- 🇮🇹 **Italiano** (`it`)
- 🇬🇧 **Inglese** (`en`)
- 🇪🇸 **Spagnolo** (`es`)
- 🇫🇷 **Francese** (`fr`)
- 🇩🇪 **Tedesco** (`de`)

## Risoluzione problemi

### Errore di importazione

```
❌ Errore di importazione: No module named 'optimum'
```

**Soluzione**: Installare le dipendenze:
```bash
pip install optimum[openvino]
```

### Errore di memoria

```
❌ Errore generico: CUDA out of memory
```

**Soluzione**: Il modello OpenVINO è ottimizzato per CPU. Questo errore non dovrebbe verificarsi.

### Modello non trovato

```
❌ Errore durante il caricamento del modello OpenVINO
```

**Soluzione**: Il modello verrà scaricato automaticamente al primo utilizzo. Assicurarsi di avere una connessione internet.

## Sviluppo

### Struttura del codice

```
TranscriberModels.py
├── OpenVINOWhisperTranscriber    # Classe principale
├── get_model()                   # Factory function
└── OPENVINO_AVAILABLE           # Flag disponibilità
```

### Aggiungere nuove lingue

Per aggiungere supporto per nuove lingue:

1. Verificare che il modello OpenVINO le supporti
2. Aggiornare la lista nelle interfacce utente
3. Testare con `test_openvino.py`

## 🔧 Fix Resampling Automatico

### Problema Risolto

**Prima del fix:** OpenVINO richiedeva audio a 16kHz esattamente, causando errori con file audio a 48kHz (comuni su Windows).

**Errore tipico:**
```
[ERROR] The model corresponding to this feature extractor: WhisperFeatureExtractor was trained using a sampling rate of 16000. Please make sure that the provided raw_speech input was sampled with 16000 and not 48000.
```

### Soluzione Implementata

Il sistema ora:

1. **Rileva automaticamente** il sample rate del file audio
2. **Converte automaticamente** a 16kHz se necessario 
3. **Usa FFmpeg** (principale), **librosa** (fallback 1) o **scipy** (fallback 2) per il resampling
4. **Ottimizza l'uso della memoria** con FFmpeg per evitare errori di allocazione
5. **Mantiene la qualità** durante la conversione con algoritmi efficienti

### Test del Fix

```bash
# Testa il resampling automatico
python test_openvino_fix.py
```

Il test:
- ✅ Crea un file audio a 48kHz
- ✅ Verifica che OpenVINO lo converta automaticamente a 16kHz
- ✅ Conferma che la trascrizione funzioni senza errori

### Dipendenze per Resampling

```bash
# Metodo principale (prestazioni ottimali e efficienza memoria)
# FFmpeg deve essere installato e disponibile nel PATH del sistema
ffmpeg -version  # Verifica installazione

# Windows: Scarica da https://ffmpeg.org/ o usa chocolatey
choco install ffmpeg

# Linux: 
sudo apt install ffmpeg  # Ubuntu/Debian
sudo yum install ffmpeg  # RHEL/CentOS

# macOS:
brew install ffmpeg
```

**Fallback automatici** (se FFmpeg non è disponibile):
```bash
# Fallback 1: librosa (buone prestazioni ma uso memoria maggiore)
pip install librosa>=0.10.0

# Fallback 2: scipy (base, prestazioni limitate)  
pip install scipy>=1.10.0
```

### Ordine di Priorità Resampling

1. 🥇 **FFmpeg** (consigliato) - Efficiente, basso uso memoria
2. 🥈 **librosa** (fallback) - Buone prestazioni, più memoria
3. 🥉 **scipy** (ultimo fallback) - Prestazioni base

### Sample Rate Supportati

Il sistema gestisce automaticamente:
- 🎵 **48kHz** (qualità professionale, comune su Windows)  
- 🎵 **44.1kHz** (qualità CD)
- 🎵 **22kHz** (qualità radio)
- 🎵 **16kHz** (target per Whisper)
- 🎵 **8kHz** (qualità telefonica)

## Riferimenti

- [Modello OpenVINO](https://huggingface.co/OpenVINO/distil-whisper-large-v3-int8-ov)
- [Documentazione OpenVINO](https://docs.openvino.ai/)
- [Optimum Intel](https://huggingface.co/docs/optimum/intel/index)

## Licenza

Questo modello è distribuito sotto licenza MIT. Vedere il [modello originale](https://huggingface.co/OpenVINO/distil-whisper-large-v3-int8-ov) per i dettagli completi della licenza. 