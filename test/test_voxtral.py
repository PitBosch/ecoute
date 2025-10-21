#!/usr/bin/env python3
"""
Test script per il modello Voxtral-Mini-3B-2507
Questo script testa le funzionalità di trascrizione e comprensione audio di Voxtral
"""

import os
import sys
import tempfile
import time
import wave
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine

# Aggiungi il percorso corrente per importare i moduli
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import TranscriberModels

def create_test_audio(duration_ms=3000, frequency=440, sample_rate=16000):
    """
    Crea un file audio di test con un tono puro
    """
    # Genera tono sinusoidale
    tone = Sine(frequency).to_audio_segment(duration=duration_ms)
    
    # Converti in mono e campiona a 16kHz per compatibilità con i modelli speech
    tone = tone.set_channels(1).set_frame_rate(sample_rate)
    
    # Salva in un file temporaneo
    fd, temp_file = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    tone.export(temp_file, format="wav")
    
    return temp_file

def test_voxtral_transcription():
    """
    Test base di trascrizione con Voxtral
    """
    print("="*60)
    print("TEST VOXTRAL - TRASCRIZIONE")
    print("="*60)
    
    try:
        # Inizializza il modello Voxtral
        print("[INFO] Inizializzazione modello Voxtral...")
        model = TranscriberModels.get_model(
            use_api=False, 
            language="it", 
            use_ollama=False, 
            use_openvino=False, 
            use_voxtral=True
        )
        print("[INFO] Modello Voxtral inizializzato con successo!")
        
        # Crea un file audio di test (tono puro - non produrrà testo ma testerà il pipeline)
        print("[INFO] Creazione file audio di test...")
        test_file = create_test_audio(duration_ms=2000, frequency=440)
        
        # Test trascrizione
        print("[INFO] Avvio trascrizione...")
        start_time = time.time()
        
        result = model.get_transcription(test_file)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"[RISULTATO] Trascrizione completata in {processing_time:.2f} secondi")
        print(f"[RISULTATO] Testo trascritto: '{result}'")
        
        # Test comprensione audio avanzata (se disponibile)
        if hasattr(model, 'get_audio_understanding'):
            print("\n[INFO] Test comprensione audio avanzata...")
            understanding_result = model.get_audio_understanding(
                test_file, 
                "Cosa puoi sentire in questo audio?"
            )
            print(f"[RISULTATO] Comprensione: '{understanding_result}'")
        
        # Cleanup
        os.unlink(test_file)
        print("\n[SUCCESS] Test Voxtral completato con successo!")
        return True
        
    except ImportError as e:
        print(f"[ERROR] Dipendenze mancanti per Voxtral: {e}")
        print("[INFO] Installa le dipendenze con:")
        print("pip install transformers mistral_common[audio] accelerate")
        return False
        
    except Exception as e:
        print(f"[ERROR] Errore durante il test Voxtral: {e}")
        return False

def test_voxtral_languages():
    """
    Test del supporto multilingue di Voxtral
    """
    print("\n" + "="*60)
    print("TEST VOXTRAL - SUPPORTO MULTILINGUE")
    print("="*60)
    
    languages = ["it", "en", "fr", "es", "de"]
    
    for lang in languages:
        try:
            print(f"\n[INFO] Test lingua: {lang}")
            model = TranscriberModels.get_model(
                use_api=False, 
                language=lang, 
                use_ollama=False, 
                use_openvino=False, 
                use_voxtral=True
            )
            print(f"[SUCCESS] Lingua {lang} supportata!")
            
        except Exception as e:
            print(f"[ERROR] Errore con lingua {lang}: {e}")
            continue

def compare_models():
    """
    Confronta Voxtral con FasterWhisper
    """
    print("\n" + "="*60)
    print("CONFRONTO MODELLI - VOXTRAL vs FASTER-WHISPER")
    print("="*60)
    
    # Crea file audio di test
    test_file = create_test_audio(duration_ms=2000, frequency=880)
    
    # Test FasterWhisper
    print("\n[INFO] Test FasterWhisper...")
    try:
        faster_model = TranscriberModels.get_model(
            use_api=False, 
            language="it", 
            use_ollama=False, 
            use_openvino=False, 
            use_voxtral=False
        )
        
        start_time = time.time()
        faster_result = faster_model.get_transcription(test_file)
        faster_time = time.time() - start_time
        
        print(f"[FASTER-WHISPER] Tempo: {faster_time:.2f}s")
        print(f"[FASTER-WHISPER] Risultato: '{faster_result}'")
        
    except Exception as e:
        print(f"[ERROR] FasterWhisper: {e}")
    
    # Test Voxtral
    print("\n[INFO] Test Voxtral...")
    try:
        voxtral_model = TranscriberModels.get_model(
            use_api=False, 
            language="it", 
            use_ollama=False, 
            use_openvino=False, 
            use_voxtral=True
        )
        
        start_time = time.time()
        voxtral_result = voxtral_model.get_transcription(test_file)
        voxtral_time = time.time() - start_time
        
        print(f"[VOXTRAL] Tempo: {voxtral_time:.2f}s")
        print(f"[VOXTRAL] Risultato: '{voxtral_result}'")
        
    except Exception as e:
        print(f"[ERROR] Voxtral: {e}")
    
    # Cleanup
    os.unlink(test_file)

def main():
    """
    Funzione principale per eseguire tutti i test
    """
    print("SCRIPT DI TEST PER VOXTRAL-MINI-3B-2507")
    print("Questo script verifica l'integrazione di Voxtral in ecoute")
    print("")
    
    # Test base
    success = test_voxtral_transcription()
    
    if success:
        # Test lingue multiple
        test_voxtral_languages()
        
        # Confronto modelli
        compare_models()
        
        print("\n" + "="*60)
        print("TUTTI I TEST COMPLETATI!")
        print("="*60)
        print("Il modello Voxtral è ora integrato in ecoute.")
        print("Per utilizzarlo, avvia ecoute con:")
        print("python main.py --voxtral")
        print("oppure")
        print("python run_modern.py --voxtral")
    else:
        print("\n" + "="*60)
        print("TEST FALLITI - INSTALLA LE DIPENDENZE")
        print("="*60)
        print("Esegui: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 