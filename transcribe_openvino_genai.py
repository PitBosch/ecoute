#!/usr/bin/env python3
"""
Script semplice per trascrizione con OpenVINO GenAI
"""

import sys
import os
import TranscriberModels

def main():
    if len(sys.argv) < 2:
        print("❌ Uso: python transcribe_openvino_genai.py <file_audio.wav>")
        print("Esempio: python transcribe_openvino_genai.py recording.wav")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    
    if not os.path.exists(audio_file):
        print(f"❌ File non trovato: {audio_file}")
        sys.exit(1)
    
    print("🚀 Avvio trascrizione con OpenVINO GenAI...")
    print(f"📁 File: {audio_file}")
    print()
    
    try:
        # Inizializza il modello OpenVINO GenAI
        print("⚙️  Caricamento modello...")
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
        
        # Trascrivi il file
        print("🎤 Trascrizione in corso...")
        transcription = model.get_transcription(audio_file)
        
        print("📝 RISULTATO:")
        print("=" * 50)
        if transcription:
            print(transcription)
        else:
            print("⚠️  Nessuna trascrizione ottenuta")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\n⏹️  Interrotto dall'utente")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Errore durante la trascrizione: {e}")
        print("\n💡 Assicurati di aver installato le dipendenze:")
        print("   pip install openvino-genai pyaudio numpy soundfile")
        sys.exit(1)

if __name__ == "__main__":
    main()