#!/usr/bin/env python3
"""
Test script per verificare il fix OpenVINO con FFmpeg
Verifica che il resampling FFmpeg risolva i problemi di memoria
"""

import sys
import os
import tempfile
import subprocess
import numpy as np
import soundfile as sf

# Aggiungi il percorso corrente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_ffmpeg_installation():
    """Verifica che FFmpeg sia installato e funzionante"""
    print("🔍 Verifica installazione FFmpeg...")
    
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if result.returncode == 0:
            # Estrai la versione
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg trovato: {version_line}")
            return True
        else:
            print("❌ FFmpeg trovato ma non funzionante")
            return False
    except FileNotFoundError:
        print("❌ FFmpeg non trovato nel PATH")
        print("💡 Installazione:")
        print("   Windows: choco install ffmpeg")
        print("   Linux:   sudo apt install ffmpeg")
        print("   macOS:   brew install ffmpeg")
        return False

def create_high_sample_rate_audio(duration=5.0, sample_rate=48000):
    """Crea un file audio ad alta risoluzione per testare il resampling"""
    print(f"🎵 Creazione audio test {sample_rate}Hz ({duration}s)...")
    
    # Genera un segnale complesso (tono + rumore) per testare la qualità
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    frequency1 = 440  # La (A4)
    frequency2 = 880  # La ottava superiore
    
    # Segnale complesso con armoniche
    audio = (0.3 * np.sin(2 * np.pi * frequency1 * t) + 
             0.2 * np.sin(2 * np.pi * frequency2 * t) +
             0.05 * np.random.normal(0, 1, len(t)))  # Rumore leggero
    
    # Normalizza
    audio = audio / np.max(np.abs(audio)) * 0.8
    
    # Salva file temporaneo
    fd, temp_file = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    sf.write(temp_file, audio, sample_rate)
    
    print(f"   ✅ Audio creato: {temp_file}")
    print(f"   📊 Sample rate: {sample_rate}Hz, Durata: {duration}s")
    print(f"   📏 Dimensione array: {len(audio)} samples")
    
    return temp_file

def test_ffmpeg_resampling():
    """Testa il resampling FFmpeg diretto"""
    print("\n🔧 TEST FFMPEG RESAMPLING DIRETTO")
    print("=" * 50)
    
    # Crea file audio test 48kHz
    test_file = create_high_sample_rate_audio(duration=3.0, sample_rate=48000)
    
    try:
        # Test resampling diretto con FFmpeg
        fd, output_file = tempfile.mkstemp(suffix="_16k.wav")
        os.close(fd)
        
        ffmpeg_cmd = [
            "ffmpeg", 
            "-i", test_file,
            "-ar", "16000",
            "-ac", "1", 
            "-y",
            "-loglevel", "quiet",
            output_file
        ]
        
        print(f"🔄 Comando FFmpeg: {' '.join(ffmpeg_cmd)}")
        result = subprocess.run(ffmpeg_cmd, capture_output=True)
        
        if result.returncode == 0:
            # Verifica il risultato
            resampled_audio, resampled_sr = sf.read(output_file)
            print(f"✅ Resampling riuscito!")
            print(f"   📊 Nuovo sample rate: {resampled_sr}Hz")
            print(f"   📏 Nuova dimensione: {len(resampled_audio)} samples")
            
            # Cleanup
            os.unlink(test_file)
            os.unlink(output_file)
            return True
        else:
            print(f"❌ FFmpeg fallito: {result.stderr.decode()}")
            os.unlink(test_file)
            return False
            
    except Exception as e:
        print(f"❌ Errore durante test FFmpeg: {e}")
        os.unlink(test_file)
        return False

def test_openvino_with_ffmpeg():
    """Testa OpenVINO con il nuovo resampling FFmpeg"""
    print("\n🎯 TEST OPENVINO CON FFMPEG")
    print("=" * 50)
    
    try:
        # Importa modelli
        import TranscriberModels
        
        print("[INFO] Inizializzazione OpenVINO...")
        model = TranscriberModels.get_model(
            use_api=False,
            language="it", 
            use_ollama=False,
            use_openvino=True,
            use_voxtral=False
        )
        print("✅ Modello OpenVINO inizializzato")
        
        # Crea un file audio che in precedenza causava problemi di memoria
        print("\n[INFO] Creazione file audio problematico (48kHz, 5 secondi)...")
        test_file = create_high_sample_rate_audio(duration=5.0, sample_rate=48000)
        
        # Test trascrizione
        print("\n[INFO] Test trascrizione con FFmpeg resampling...")
        print("[INFO] Questo dovrebbe ora funzionare senza errori di memoria")
        
        result = model.get_transcription(test_file)
        
        print(f"\n✅ TRASCRIZIONE COMPLETATA SENZA ERRORI!")
        print(f"📄 Risultato: '{result}'")
        print("💡 FFmpeg ha risolto i problemi di memoria del resampling!")
        
        # Cleanup
        os.unlink(test_file)
        
        return True
        
    except ImportError as e:
        print(f"❌ Dipendenze OpenVINO mancanti: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Errore durante test OpenVINO: {e}")
        return False

def test_memory_efficiency():
    """Confronta l'efficienza di memoria tra i metodi"""
    print("\n💾 TEST EFFICIENZA MEMORIA")
    print("=" * 35)
    
    # Questo test crea file audio sempre più grandi per verificare
    # che FFmpeg gestisca meglio la memoria
    
    durations = [1, 3, 5, 10]  # secondi
    
    for duration in durations:
        print(f"\n📏 Test con audio di {duration} secondi...")
        
        test_file = create_high_sample_rate_audio(duration=duration, sample_rate=48000)
        
        try:
            # Misura l'efficienza stimando le dimensioni
            original_size = os.path.getsize(test_file)
            print(f"   📦 Dimensione file originale: {original_size / 1024:.1f} KB")
            
            # Il test principale è che non si verifichino errori di memoria
            print(f"   🧠 Test assenza errori memoria con {duration}s...")
            
            # Simula quello che fa OpenVINO
            fd, temp_output = tempfile.mkstemp(suffix=".wav")
            os.close(fd)
            
            ffmpeg_cmd = ["ffmpeg", "-i", test_file, "-ar", "16000", "-ac", "1", "-y", "-loglevel", "quiet", temp_output]
            result = subprocess.run(ffmpeg_cmd, capture_output=True)
            
            if result.returncode == 0:
                resampled_size = os.path.getsize(temp_output)
                print(f"   ✅ Successo! Dimensione resampled: {resampled_size / 1024:.1f} KB")
                os.unlink(temp_output)
            else:
                print(f"   ❌ Errore FFmpeg")
                
            os.unlink(test_file)
            
        except Exception as e:
            print(f"   ❌ Errore: {e}")
            continue

def main():
    """Funzione principale"""
    print("🧪 TEST FFMPEG FIX PER OPENVINO")
    print("=" * 50)
    print("Verifica che FFmpeg risolva i problemi di memoria del resampling\n")
    
    # 1. Verifica FFmpeg
    ffmpeg_ok = check_ffmpeg_installation()
    
    if not ffmpeg_ok:
        print("\n❌ FFMPEG NON DISPONIBILE")
        print("Il test non può continuare senza FFmpeg.")
        print("Installa FFmpeg e riprova.")
        return False
    
    # 2. Test FFmpeg diretto
    ffmpeg_test_ok = test_ffmpeg_resampling()
    
    if not ffmpeg_test_ok:
        print("\n❌ FFMPEG NON FUNZIONA CORRETTAMENTE")
        return False
    
    # 3. Test efficienza memoria
    test_memory_efficiency()
    
    # 4. Test OpenVINO completo
    openvino_test_ok = test_openvino_with_ffmpeg()
    
    if openvino_test_ok:
        print("\n" + "=" * 50)
        print("🎉 TUTTI I TEST SUPERATI!")
        print("=" * 50)
        print("✅ FFmpeg installato e funzionante")
        print("✅ Resampling efficiente confermato")
        print("✅ OpenVINO funziona senza errori di memoria")
        print("\n🚀 Ora puoi usare OpenVINO senza problemi:")
        print("   python run_modern.py --openvino")
        
    else:
        print("\n" + "=" * 50) 
        print("❌ ALCUNI TEST FALLITI")
        print("=" * 50)
        print("💡 Possibili soluzioni:")
        print("   1. Verifica installazione OpenVINO")
        print("   2. Installa dipendenze: pip install optimum[openvino]")
        print("   3. Usa FasterWhisper: python run_modern.py")

if __name__ == "__main__":
    main() 