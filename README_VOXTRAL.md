# 🎙️ Ecoute con Voxtral-Mini-3B-2507

Questo documento spiega come utilizzare il modello **Voxtral-Mini-3B-2507** di Mistral AI nel progetto ecoute.

## 🌟 Caratteristiche di Voxtral

Voxtral-Mini-3B-2507 è un modello avanzato di Mistral AI che combina:

- **Trascrizione vocale** ad alta precisione
- **Comprensione audio** avanzata
- **Supporto multilingue** nativo (8 lingue)
- **Contesto lungo** (32k token, fino a 30 minuti di audio)
- **Rilevamento automatico** della lingua
- **Funzionalità Q&A** direttamente dall'audio

### Lingue Supportate

✅ **Italiano** (it) - Supporto nativo  
✅ **Inglese** (en) - Supporto nativo  
✅ **Spagnolo** (es) - Supporto nativo  
✅ **Francese** (fr) - Supporto nativo  
✅ **Tedesco** (de) - Supporto nativo  
✅ **Portoghese** (pt) - Supporto nativo  
✅ **Hindi** (hi) - Supporto nativo  
✅ **Olandese** (nl) - Supporto nativo  

## 📋 Requisiti di Sistema

### Hardware
- **GPU consigliata**: NVIDIA con almeno 10GB VRAM (RTX 3080/4070 o superiore)
- **CPU**: Supporta anche CPU ma molto più lento
- **RAM**: Minimo 16GB, consigliato 32GB
- **Spazio disco**: 10GB liberi per il modello

### Software
- Python 3.8+
- CUDA 11.8+ (per GPU NVIDIA)

## 🚀 Installazione

### 1. Installa le dipendenze

```bash
# Installa le dipendenze base
pip install -r requirements.txt

# Verifica che tutte le dipendenze Voxtral siano installate
pip install transformers>=4.30.0 mistral_common[audio]>=1.8.1 accelerate>=0.20.0
```

### 2. Verifica l'installazione

```bash
# Esegui il test di Voxtral
python test_voxtral.py
```

Se tutto funziona correttamente, vedrai:
```
✅ Voxtral-Mini-3B caricato con successo - GPU: True
✅ Test Voxtral completato con successo!
```

## 🎯 Utilizzo

### Interfaccia Moderna (Consigliata)

```bash
# Avvia con Voxtral per italiano
python run_modern.py --voxtral

# Avvia con Voxtral per inglese
python run_modern.py --voxtral --lang=en

# Avvia con Voxtral per spagnolo
python run_modern.py --voxtral --lang=es
```

### Interfaccia Classica

```bash
# Avvia con Voxtral
python main.py --voxtral

# Con lingua specifica (modifica nel codice)
python main.py --voxtral --lang=en
```

### Test e Confronti

```bash
# Test completo di Voxtral
python test_voxtral.py

# Confronto con altri modelli
python test_voxtral.py --compare
```

## ⚡ Performance

### Tempi di Avvio
- **Primo avvio**: 30-60 secondi (download del modello)
- **Avvii successivi**: 10-20 secondi (caricamento da cache)

### Velocità di Trascrizione
- **GPU RTX 4070**: ~2-3x tempo reale
- **GPU RTX 3080**: ~1.5-2x tempo reale  
- **CPU Intel i7**: ~0.3x tempo reale (molto lento)

### Memoria
- **GPU VRAM**: ~9.5GB in bf16
- **RAM sistema**: ~4-6GB aggiuntivi

## 🔧 Configurazione Avanzata

### Ottimizzazione GPU

Se hai una GPU con meno di 10GB VRAM, puoi provare:

```python
# In TranscriberModels.py, modifica la classe VoxtralTranscriber:
self.model = VoxtralForConditionalGeneration.from_pretrained(
    self.model_id, 
    torch_dtype=torch.float16,  # Usa float16 invece di bfloat16
    device_map="auto",
    load_in_8bit=True  # Quantizzazione 8-bit per ridurre VRAM
)
```

### Fallback CPU

Per forzare l'uso della CPU (lento ma funziona senza GPU):

```python
# Modifica in TranscriberModels.py:
device_map="cpu"  # Invece di "auto"
```

## 🚨 Risoluzione Problemi

### Errore: "CUDA out of memory"
```bash
# Soluzione 1: Chiudi altre applicazioni GPU
# Soluzione 2: Usa quantizzazione 8-bit
# Soluzione 3: Usa CPU (molto lento)
```

### Errore: "ImportError: Voxtral dependencies not available"
```bash
pip install --upgrade transformers mistral_common[audio] accelerate
```

### Errore: "No module named 'mistral_common'"
```bash
pip install mistral_common[audio]
```

### Trascrizione lenta o bloccata
- Verifica che la GPU sia utilizzata: guarda i log di avvio
- Controlla Task Manager per utilizzo GPU
- Riavvia l'applicazione se necessario

## 📊 Confronto Modelli

| Modello | Precisione | Velocità | VRAM | Lingue | Funzioni Extra |
|---------|------------|----------|------|--------|----------------|
| **Voxtral-Mini-3B** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 9.5GB | 8 | Q&A, Comprensione |
| FasterWhisper | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 2GB | 100+ | Solo trascrizione |
| OpenVINO Whisper | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 1GB | 100+ | Solo trascrizione |
| OpenAI API | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 0 | 100+ | Solo trascrizione |

## 🔄 Passaggio tra Modelli

Puoi cambiare modello riavviando l'applicazione con parametri diversi:

```bash
# Voxtral
python run_modern.py --voxtral

# FasterWhisper (veloce, locale)
python run_modern.py

# OpenVINO (ottimizzato CPU)
python run_modern.py --openvino

# OpenAI API (precisione massima, richiede internet)
python run_modern.py --api
```

## 📚 Funzionalità Avanzate

### Comprensione Audio (Solo Voxtral)

Voxtral può rispondere a domande sull'audio:

```python
# Esempio d'uso avanzato
transcriber = VoxtralTranscriber()

# Trascrizione semplice
text = transcriber.get_transcription("audio.wav")

# Comprensione con domanda
summary = transcriber.get_audio_understanding(
    "audio.wav", 
    "Riassumi i punti principali di questa conversazione"
)
```

## 🎯 Best Practices

1. **GPU**: Usa sempre GPU per Voxtral se disponibile
2. **Audio**: Qualità audio migliore = trascrizioni migliori
3. **Lingue**: Specifica la lingua se nota per migliori risultati
4. **Memoria**: Chiudi altre applicazioni GPU-intensive durante l'uso
5. **Aggiornamenti**: Mantieni aggiornate le dipendenze

## 📞 Supporto

Per problemi specifici di Voxtral:

1. Controlla i log nell'applicazione
2. Esegui `python test_voxtral.py` per diagnostica
3. Verifica la versione delle dipendenze:
   ```bash
   pip list | grep -E "(transformers|mistral|accelerate)"
   ```

## 🔗 Link Utili

- [Voxtral su Hugging Face](https://huggingface.co/mistralai/Voxtral-Mini-3B-2507)
- [Documentazione Mistral AI](https://docs.mistral.ai/)
- [Transformers Documentation](https://huggingface.co/docs/transformers/)

---

**Nota**: Voxtral-Mini-3B-2507 è un modello potente ma richiede risorse hardware significative. Per uso su hardware limitato, considera FasterWhisper o OpenVINO. 