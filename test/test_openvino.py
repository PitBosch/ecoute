#!/usr/bin/env python3
"""
Test per il modello OpenVINO Whisper
"""

import sys
import os
import TranscriberModels
import tempfile
import numpy as np
import soundfile as sf

def create_test_audio():
    """Crea un file audio di test"""
    # Crea un segnale audio sinusoidale di 3 secondi
    sample_rate = 16000
    duration = 3.0
    frequency = 440  # La nota A4
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    # Salva in un file temporaneo
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    sf.write(temp_file.name, audio_data, sample_rate)
    
    return temp_file.name

def test_openvino_model():
    """Test del modello OpenVINO"""
    print("🧪 TESTING OpenVINO Whisper Model")
    print("=" * 50)
    
    try:
        # Test di importazione
        print("📦 Testando importazione OpenVINO...")
        model = TranscriberModels.get_model(use_api=False, language="it", use_ollama=False, use_openvino=True)
        print("✅ Modello OpenVINO per l'italiano caricato con successo")
        
        # Test di trascrizione con audio fittizio
        print("\n🎵 Testando trascrizione con audio di test...")
        test_audio_path = create_test_audio()
        
        try:
            transcription = model.get_transcription(test_audio_path)
            print(f"📝 Trascrizione ricevuta: '{transcription}'")
            
            if transcription:
                print("✅ Test di trascrizione completato con successo")
            else:
                print("⚠️  Trascrizione vuota (normale per audio sintetizzato)")
                
        except Exception as e:
            print(f"❌ Errore durante la trascrizione: {e}")
            
        finally:
            # Pulisci file temporaneo
            try:
                os.unlink(test_audio_path)
            except:
                pass
                
    except ImportError as e:
        print(f"❌ Errore di importazione: {e}")
        print("💡 Installare le dipendenze con: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Errore generico: {e}")
        return False
        
    print("\n🎉 Test OpenVINO completato!")
    return True

def test_languages():
    """Test delle lingue supportate"""
    print("\n🌍 TESTING Lingue Supportate")
    print("=" * 50)
    
    languages = ["it", "en", "es", "fr", "de"]
    
    for lang in languages:
        try:
            print(f"📝 Testando lingua: {lang}")
            model = TranscriberModels.get_model(use_api=False, language=lang, use_ollama=False, use_openvino=True)
            print(f"✅ Lingua {lang} supportata")
        except Exception as e:
            print(f"❌ Errore con lingua {lang}: {e}")

def main():
    """Funzione principale"""
    print("🚀 ECOUTE - Test OpenVINO Whisper")
    print("=" * 50)
    
    # Test del modello OpenVINO
    success = test_openvino_model()
    
    if success:
        # Test delle lingue
        test_languages()
    
    print("\n" + "=" * 50)
    print("🏁 Test completati!")

if __name__ == "__main__":
    main() 