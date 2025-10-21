#!/usr/bin/env python3
"""
Test per il modello OpenVINO GenAI Whisper
"""

import sys
import os
import TranscriberModels
import tempfile
import numpy as np
import soundfile as sf
import time

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

def test_openvino_genai_model():
    """Test del modello OpenVINO GenAI"""
    print("🧪 TESTING OpenVINO GenAI Whisper Model")
    print("=" * 50)
    
    try:
        # Test di importazione
        print("📦 Testando importazione OpenVINO GenAI...")
        model = TranscriberModels.get_model(
            use_api=False, 
            language="it", 
            use_ollama=False, 
            use_openvino=False,
            use_voxtral=False,
            use_openvino_genai=True
        )
        print("✅ Modello OpenVINO GenAI per l'italiano caricato con successo")
        
        # Test di trascrizione con audio fittizio
        print("\n🎵 Testando trascrizione con audio di test...")
        test_audio_path = create_test_audio()
        
        try:
            start_time = time.time()
            transcription = model.get_transcription(test_audio_path)
            end_time = time.time()
            
            print(f"📝 Trascrizione ricevuta: '{transcription}'")
            print(f"⏱️  Tempo di trascrizione: {end_time - start_time:.2f} secondi")
            
            if transcription:
                print("✅ Test di trascrizione completato con successo")
            else:
                print("⚠️  Trascrizione vuota (normale per audio sintetizzato)")
                
        except Exception as e:
            print(f"❌ Errore durante la trascrizione: {e}")
            return False
        finally:
            # Pulizia file temporaneo
            try:
                os.unlink(test_audio_path)
            except:
                pass
        
        # Test con file audio reale se fornito
        if len(sys.argv) > 1:
            audio_file = sys.argv[1]
            if os.path.exists(audio_file):
                print(f"\n🎤 Testando con file audio reale: {audio_file}")
                try:
                    start_time = time.time()
                    transcription = model.get_transcription(audio_file)
                    end_time = time.time()
                    
                    print(f"📝 Trascrizione: '{transcription}'")
                    print(f"⏱️  Tempo di trascrizione: {end_time - start_time:.2f} secondi")
                    
                except Exception as e:
                    print(f"❌ Errore con file reale: {e}")
            else:
                print(f"❌ File audio non trovato: {audio_file}")
        
        print("\n🎉 Test OpenVINO GenAI completato!")
        return True
        
    except ImportError as e:
        print(f"❌ Dipendenze mancanti: {e}")
        print("💡 Installa con: pip install openvino-genai pyaudio numpy soundfile")
        return False
        
    except Exception as e:
        print(f"❌ Errore generico: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Avvio test OpenVINO GenAI...")
    print("Usage: python test_openvino_genai.py [audio_file.wav]")
    print()
    
    success = test_openvino_genai_model()
    sys.exit(0 if success else 1)