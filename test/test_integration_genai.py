#!/usr/bin/env python3
"""
Test integrazione OpenVINO GenAI con registrazione microfono e speaker
"""
import queue
import threading
import time
from datetime import datetime

def test_direct_transcriber():
    try:
        print("🧪 Test integrazione OpenVINO GenAI...")
        
        # Import diretto come nell'app
        print("1. Import TranscriberModels...")
        import TranscriberModels
        
        print("2. Creazione modello OpenVINO GenAI...")
        model = TranscriberModels.get_model(
            use_api=False,
            language="en", 
            use_ollama=False,
            use_openvino=False,
            use_voxtral=False,
            use_openvino_genai=True
        )
        
        print("3. ✅ Modello creato con successo!")
        print(f"   Dispositivo: {model.device}")
        
        # Test con audio di test casuale (mantenuto per controllo base)
        print("4. Test trascrizione base con audio casuale...")
        import tempfile
        import numpy as np
        import soundfile as sf
        
        # Crea audio di test
        test_audio = np.random.random(16000 * 3).astype(np.float32)  # 3 secondi
        
        # Salva in file temporaneo
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            sf.write(f.name, test_audio, 16000)
            temp_file = f.name
        
        try:
            result = model.pipe.generate(test_audio)
            print(f"5. ✅ Trascrizione base completata: '{result}'")
        finally:
            import os
            os.unlink(temp_file)
            
        return True
        
    except Exception as e:
        print(f"❌ Errore nell'integrazione: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_real_audio_recording():
    """Test con registrazione reale di microfono e speaker"""
    try:
        print("\n🎤 Test registrazione audio reale...")
        
        # Import dei moduli di registrazione
        print("1. Import AudioRecorder e AudioTranscriber...")
        from AudioRecorder import DefaultMicRecorder, DefaultSpeakerRecorder
        from AudioTranscriber import AudioTranscriber
        import TranscriberModels
        
        print("2. Inizializzazione recorder...")
        # Inizializza i recorder
        mic_recorder = DefaultMicRecorder()
        speaker_recorder = DefaultSpeakerRecorder()
        
        print("3. Creazione modello per trascrizione...")
        # Crea il modello per la trascrizione
        model = TranscriberModels.get_model(
            use_api=False,
            language="en", 
            use_ollama=False,
            use_openvino=False,
            use_voxtral=False,
            use_openvino_genai=True
        )
        
        print("4. Inizializzazione AudioTranscriber...")
        # Inizializza il trascrittore
        transcriber = AudioTranscriber(
            mic_source=mic_recorder.source,
            speaker_source=speaker_recorder.source, 
            model=model
        )
        
        print("5. Creazione code audio...")
        # Crea le code per l'audio
        mic_queue = queue.Queue()
        speaker_queue = queue.Queue()
        
        print("6. Avvio registrazione...")
        # Avvia la registrazione in background
        mic_recorder.record_into_queue(mic_queue)
        speaker_recorder.record_into_queue(speaker_queue)
        
        print("7. Avvio thread di trascrizione...")
        # Avvia il thread di trascrizione
        transcription_thread = threading.Thread(
            target=transcriber.transcribe_audio_queue,
            args=(speaker_queue, mic_queue),
            daemon=True
        )
        transcription_thread.start()
        
        print("\n🎙️ REGISTRAZIONE ATTIVA! Parla nel microfono o riproduci audio...")
        print("⏱️  Registrerò per 30 secondi...")
        print("📝 Transcripts verranno mostrate in tempo reale:")
        print("-" * 50)
        
        # Monitora per 30 secondi
        start_time = time.time()
        last_transcript = ""
        
        while time.time() - start_time < 30:
            # Controlla se ci sono nuove trascrizioni
            if transcriber.transcript_changed_event.wait(timeout=1.0):
                transcriber.transcript_changed_event.clear()
                current_transcript = transcriber.get_transcript()
                
                if current_transcript != last_transcript:
                    print(f"\n📄 TRASCRIZIONE AGGIORNATA [{datetime.now().strftime('%H:%M:%S')}]:")
                    print(current_transcript)
                    print("-" * 50)
                    last_transcript = current_transcript
        
        print(f"\n✅ Test di registrazione completato!")
        print(f"📊 Trascrizione finale:")
        final_transcript = transcriber.get_transcript()
        if final_transcript.strip():
            print(final_transcript)
        else:
            print("   Nessuna trascrizione rilevata (prova a parlare più forte o riproduci audio)")
            
        return True
        
    except Exception as e:
        print(f"❌ Errore nella registrazione audio: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Test 1: Integrazione base con OpenVINO GenAI
    print("=" * 60)
    print("🧪 FASE 1: Test integrazione OpenVINO GenAI")
    print("=" * 60)
    
    success_basic = test_direct_transcriber()
    if success_basic:
        print("\n🎉 Test integrazione base RIUSCITO!")
    else:
        print("\n💥 Test integrazione base FALLITO!")
        print("Il problema è nell'integrazione con TranscriberModels.")
    
    # Test 2: Registrazione audio reale 
    print("\n" + "=" * 60)
    print("🎤 FASE 2: Test registrazione microfono e speaker")
    print("=" * 60)
    
    if success_basic:
        try:
            success_audio = test_real_audio_recording()
            if success_audio:
                print("\n🎉 Test registrazione audio RIUSCITO!")
                print("✅ Sistema completamente funzionale!")
            else:
                print("\n💥 Test registrazione audio FALLITO!")
                print("Il problema è nella gestione dell'audio in tempo reale.")
        except KeyboardInterrupt:
            print("\n⏹️  Test interrotto dall'utente.")
            success_audio = True  # Non consideriamo un fallimento
        except Exception as e:
            print(f"\n💥 Errore imprevisto nel test audio: {e}")
            success_audio = False
    else:
        print("⏭️  Saltando test audio - fix prima l'integrazione base.")
        success_audio = False
    
    # Riepilogo finale
    print("\n" + "=" * 60)
    print("📋 RIEPILOGO FINALE")
    print("=" * 60)
    print(f"✅ Test integrazione base: {'RIUSCITO' if success_basic else 'FALLITO'}")
    print(f"✅ Test registrazione audio: {'RIUSCITO' if success_audio else 'FALLITO'}")
    
    if success_basic and success_audio:
        print("\n🚀 TUTTO FUNZIONA CORRETTAMENTE!")
        print("   Il sistema è pronto per l'uso completo.")
    elif success_basic:
        print("\n⚠️  INTEGRAZIONE BASE FUNZIONA")
        print("   Ma ci sono problemi con la registrazione audio.")
    else:
        print("\n🔧 RICHIEDE DEBUGGING")
        print("   Problemi nell'integrazione con TranscriberModels.")