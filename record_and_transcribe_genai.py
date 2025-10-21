#!/usr/bin/env python3
"""
Script per registrare audio dal microfono e trascriverlo con OpenVINO GenAI
Basato sul codice originale fornito dall'utente
"""

import pyaudio
import numpy as np
import tempfile
import soundfile as sf
import time
import sys
import TranscriberModels

def record_audio(duration=5, sample_rate=16000, chunk_size=1024):
    """
    Registra audio dal microfono per la durata specificata
    """
    print(f"🎤 Registrazione audio per {duration} secondi...")
    
    # Inizializza PyAudio
    audio = pyaudio.PyAudio()
    
    # Configura il stream audio
    stream = audio.open(
        format=pyaudio.paFloat32,
        channels=1,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size
    )
    
    frames = []
    
    print("🔴 REGISTRAZIONE IN CORSO... Parla ora!")
    
    # Registra per la durata specificata
    for i in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)
        
        # Mostra progress bar semplice
        progress = (i + 1) / (sample_rate / chunk_size * duration)
        bar_length = 30
        filled_length = int(bar_length * progress)
        bar = "█" * filled_length + "░" * (bar_length - filled_length)
        print(f"\r[{bar}] {progress*100:.1f}%", end="", flush=True)
    
    print("\n✅ Registrazione completata!")
    
    # Chiudi il stream
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    # Converti in array numpy
    audio_data = np.frombuffer(b''.join(frames), dtype=np.float32)
    return audio_data, sample_rate

def save_audio_to_temp_file(audio_data, sample_rate):
    """Salva l'audio in un file temporaneo"""
    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    sf.write(temp_file.name, audio_data, sample_rate)
    return temp_file.name

def main():
    # Parametri configurabili
    duration = 5  # secondi
    if len(sys.argv) > 1:
        try:
            duration = int(sys.argv[1])
        except ValueError:
            print("❌ Durata deve essere un numero intero")
            sys.exit(1)
    
    print("🚀 TRASCRIZIONE LIVE CON OPENVINO GENAI")
    print("=" * 50)
    print(f"⏱️  Durata registrazione: {duration} secondi")
    print("🎯 Lingua: Italiano")
    print()
    
    try:
        # Carica il modello OpenVINO GenAI
        print("⚙️  Caricamento modello OpenVINO GenAI...")
        model = TranscriberModels.get_model(
            use_api=False,
            language="it",
            use_ollama=False,
            use_openvino=False,
            use_voxtral=False,
            use_openvino_genai=True
        )
        print("✅ Modello caricato!")
        print()
        
        while True:
            print("Premi INVIO per iniziare la registrazione (o 'q' per uscire)...")
            user_input = input().strip().lower()
            
            if user_input == 'q':
                print("👋 Arrivederci!")
                break
            
            # Registra audio dal microfono
            print()
            audio_sample, sample_rate = record_audio(duration=duration)
            
            # Salva in file temporaneo
            temp_audio_file = save_audio_to_temp_file(audio_sample, sample_rate)
            
            try:
                # Trascrivi l'audio registrato
                print("🔄 Trascrizione in corso...")
                start_time = time.time()
                result = model.get_transcription(temp_audio_file)
                end_time = time.time()
                
                print()
                print("📝 TRASCRIZIONE:")
                print("=" * 30)
                if result:
                    print(result)
                else:
                    print("⚠️  Nessun testo rilevato")
                print("=" * 30)
                print(f"⏱️  Tempo di elaborazione: {end_time - start_time:.2f}s")
                print()
                
            finally:
                # Pulizia file temporaneo
                import os
                try:
                    os.unlink(temp_audio_file)
                except:
                    pass
                    
    except KeyboardInterrupt:
        print("\n⏹️  Interrotto dall'utente")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Errore: {e}")
        print("\n💡 Assicurati di aver installato le dipendenze:")
        print("   pip install openvino-genai pyaudio numpy soundfile")
        sys.exit(1)

if __name__ == "__main__":
    print("Uso: python record_and_transcribe_genai.py [durata_secondi]")
    print("Esempio: python record_and_transcribe_genai.py 10")
    print()
    main()