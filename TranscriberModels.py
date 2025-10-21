import torch
from faster_whisper import WhisperModel
from openai import OpenAI
import subprocess
import json
import tempfile
import os
import soundfile as sf
from keys import OPENAI_API_KEY

# OpenVINO imports
try:
    from transformers.pipelines import pipeline
    from optimum.intel.openvino import OVModelForSpeechSeq2Seq
    from transformers import AutoProcessor
    OPENVINO_AVAILABLE = True
except ImportError:
    OPENVINO_AVAILABLE = False

# Voxtral imports
try:
    from transformers import VoxtralForConditionalGeneration, AutoProcessor as VoxtralProcessor
    VOXTRAL_AVAILABLE = True
except ImportError:
    VOXTRAL_AVAILABLE = False

# OpenVINO GenAI imports
try:
    import openvino_genai as ov_genai
    import numpy as np
    OPENVINO_GENAI_AVAILABLE = True
    # pyaudio è opzionale (necessario solo per registrazione live)
    try:
        import pyaudio
        PYAUDIO_AVAILABLE = True
    except ImportError:
        PYAUDIO_AVAILABLE = False
        print("[WARNING] PyAudio non disponibile - registrazione live disabilitata")
except ImportError:
    OPENVINO_GENAI_AVAILABLE = False

def get_model(use_api, language="it", use_ollama=False, use_openvino=False, use_voxtral=False, use_openvino_genai=False):
    if use_voxtral:
        return VoxtralTranscriber(language=language)
    elif use_openvino_genai:
        return OpenVINOGenAITranscriber(language=language)
    elif use_openvino:
        return OpenVINOWhisperTranscriber(language=language)
    elif use_ollama:
        return OllamaWhisperTranscriber(language=language)
    elif use_api:
        return APIWhisperTranscriber(language=language)
    else:
        return FasterWhisperTranscriber(language=language)

class OllamaWhisperTranscriber:
    def __init__(self, language="it"):
        print(f"[INFO] Inizializzando Ollama Whisper per lingua: {language}...")
        self.language = language
        # Verifica che Ollama sia installato
        try:
            subprocess.run(["ollama", "--version"], capture_output=True, check=True)
            print("[INFO] Ollama trovato e funzionante")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("[ERROR] Ollama non trovato. Installa Ollama da https://ollama.ai")
            raise

    def get_transcription(self, wav_file_path):
        try:
            # Comando per trascrivere con Ollama Whisper
            cmd = [
                "ollama", "run", "whisper",
                "--model", "whisper",
                "--language", self.language,
                "--file", wav_file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return result.stdout.strip()
            
        except subprocess.CalledProcessError as e:
            print(f"Errore Ollama Whisper: {e}")
            return ''
        except Exception as e:
            print(f"Errore generico: {e}")
            return ''

class FasterWhisperTranscriber:
    def __init__(self, language="it"):
        print(f"[INFO] Loading Faster Whisper model for language: {language}...")
        # Usiamo un modello multilingue invece di tiny.en
        model_name = "medium" if language == "it" else "tiny.en"
        self.model = WhisperModel(model_name, device="cuda" if torch.cuda.is_available() else "cpu", 
                                 compute_type="float32" if torch.cuda.is_available() else "int8")
        self.language = language
        print(f"[INFO] Faster Whisper using GPU: {torch.cuda.is_available()}")
        print(f"[INFO] Language set to: {language}")

    def get_transcription(self, wav_file_path):
        try:
            # Per l'italiano, specifichiamo la lingua per migliorare l'accuratezza
            if self.language == "it":
                segments, _ = self.model.transcribe(wav_file_path, language="it", beam_size=5)
            else:
                segments, _ = self.model.transcribe(wav_file_path, beam_size=5)
            full_text = " ".join(segment.text for segment in segments)
            return full_text.strip()
        except Exception as e:
            print(e)
            return ''

class APIWhisperTranscriber:
    def __init__(self, api_key=None, language="it"):
        # Usa la chiave API dal file keys.py se non viene fornita una chiave specifica
        if api_key is None:
            api_key = OPENAI_API_KEY
        self.client = OpenAI(api_key=api_key)
        self.language = language
    
    def get_transcription(self, wav_file_path):
        try:
            with open(wav_file_path, "rb") as audio_file:
                result = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=self.language
                )
            return result.text.strip()
        except Exception as e:
            print(e)
            return ''

class OpenVINOWhisperTranscriber:
    def __init__(self, language='it'):
        self.language = language
        # Usa un modello OpenVINO reale disponibile su HuggingFace
        self.model_id = "OpenVINO/whisper-tiny-int8-ov"
        self.model_path = "whisper-large-v3-turbo-int8-ov"  # Modello base che può essere convertito automaticamente
        
        try:
            print(f"[INFO] Caricamento modello OpenVINO: {self.model_path}")
            
            # Usa OVModelForSpeechSeq2Seq direttamente con AutoProcessor
            self.processor = AutoProcessor.from_pretrained(self.model_path)
            self.model = OVModelForSpeechSeq2Seq.from_pretrained(self.model_path)
            
            print("[INFO] Modello OpenVINO caricato con successo")
        except Exception as e:
            print(f"[ERROR] Errore durante il caricamento del modello OpenVINO: {e}")
            raise

    def get_transcription(self, wav_file_path):
        try:
            # Carica il file audio usando soundfile
            import soundfile as sf
            audio, sample_rate = sf.read(wav_file_path)
            
            # RESAMPLING AUTOMATICO A 16kHz CON FFMPEG (molto più efficiente)
            if sample_rate != 16000:
                try:
                    import subprocess
                    import tempfile
                    import os
                    
                    print(f"[INFO] OpenVINO: Resampling da {sample_rate}Hz a 16000Hz con FFmpeg")
                    
                    # Crea file temporaneo per l'output resampled
                    fd, temp_resampled_file = tempfile.mkstemp(suffix=".wav")
                    os.close(fd)
                    
                    # Comando FFmpeg per resampling efficiente
                    ffmpeg_cmd = [
                        "ffmpeg", 
                        "-i", wav_file_path,
                        "-ar", "16000",  # Target sample rate
                        "-ac", "1",      # Mono
                        "-y",            # Overwrite output
                        "-loglevel", "quiet",  # Suppress FFmpeg logs
                        temp_resampled_file
                    ]
                    
                    # Esegui FFmpeg
                    result = subprocess.run(ffmpeg_cmd, capture_output=True)
                    
                    if result.returncode == 0:
                        # Ricarica l'audio resampled
                        audio, sample_rate = sf.read(temp_resampled_file)
                        print(f"[INFO] OpenVINO: Resampling completato con FFmpeg")
                        os.unlink(temp_resampled_file)  # Cleanup
                    else:
                        print(f"[WARNING] FFmpeg fallito, uso librosa come fallback")
                        os.unlink(temp_resampled_file)
                        # Fallback a librosa/scipy solo se FFmpeg fallisce
                        try:
                            import librosa
                            audio = librosa.resample(audio, orig_sr=sample_rate, target_sr=16000)
                            sample_rate = 16000
                        except ImportError:
                            try:
                                from scipy import signal
                                resampling_factor = 16000 / sample_rate
                                new_length = int(len(audio) * resampling_factor)
                                audio = signal.resample(audio, new_length)
                                sample_rate = 16000
                            except ImportError:
                                print("[ERROR] FFmpeg, librosa e scipy non disponibili per resampling")
                                print(f"[INFO] Tentativo con sample rate originale: {sample_rate}Hz")
                                
                except Exception as e:
                    print(f"[WARNING] Errore durante resampling FFmpeg: {e}, uso fallback")
                    # Fallback a librosa/scipy
                    try:
                        import librosa
                        audio = librosa.resample(audio, orig_sr=sample_rate, target_sr=16000)
                        sample_rate = 16000
                    except ImportError:
                        try:
                            from scipy import signal
                            resampling_factor = 16000 / sample_rate
                            new_length = int(len(audio) * resampling_factor)
                            audio = signal.resample(audio, new_length)
                            sample_rate = 16000
                        except ImportError:
                            print("[ERROR] Nessun metodo di resampling disponibile")
                            print(f"[INFO] Tentativo con sample rate originale: {sample_rate}Hz")
            
            # Preprocessa l'audio con il sample rate corretto
            inputs = self.processor(
                audio,
                sampling_rate=16000,  # Forza sempre 16kHz per Whisper
                return_tensors="pt"
            )
            
            # Genera la trascrizione
            if self.language == "it":
                # Forza la lingua italiana
                predicted_ids = self.model.generate(
                    inputs["input_features"],
                    language="italian",
                    task="transcribe"
                )
            else:
                predicted_ids = self.model.generate(inputs["input_features"])
            
            # Decodifica il testo
            transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
            return transcription.strip()
            
        except Exception as e:
            print(f"[ERROR] Errore durante la trascrizione OpenVINO: {e}")
            return ''

class OpenVINOGenAITranscriber:
    def __init__(self, language='it'):
        self.language = language
        self.model_path = "whisper-large-v3-turbo-int8"
        
        if not OPENVINO_GENAI_AVAILABLE:
            print("[ERROR] OpenVINO GenAI non disponibile. Installa con: pip install openvino-genai")
            raise ImportError("OpenVINO GenAI dependencies not available")
        
        # Lista di dispositivi da provare in ordine di preferenza
        devices_to_try = ["NPU"]  # Solo CPU per ora, più stabile
        
        self.pipe = None
        for device in devices_to_try:
            try:
                print(f"[INFO] Tentativo caricamento modello OpenVINO GenAI: {self.model_path}")
                print(f"[INFO] Dispositivo: {device}")
                
                # Inizializza la pipeline Whisper
                self.pipe = ov_genai.WhisperPipeline(self.model_path, device)
                self.device = device
                
                print(f"[INFO] ✅ Modello OpenVINO GenAI caricato con successo su {device}")
                print(f"[INFO] Lingua impostata: {language}")
                break
                
            except Exception as e:
                print(f"[WARNING] ❌ Errore con dispositivo {device}: {e}")
                if device == devices_to_try[-1]:  # Ultimo dispositivo nella lista
                    print(f"[ERROR] Tutti i dispositivi falliti. Ultimo errore: {e}")
                    print("[ERROR] Verifica che il modello sia presente e OpenVINO GenAI sia installato correttamente")
                    raise
                else:
                    print(f"[INFO] Tentativo con prossimo dispositivo...")
        
        if self.pipe is None:
            raise RuntimeError("Impossibile caricare il modello OpenVINO GenAI su nessun dispositivo")

    def get_transcription(self, wav_file_path):
        if self.pipe is None:
            print("[ERROR] Modello non inizializzato correttamente")
            return ''
        try:
            return self.pipe.generate(wav_file_path)
        except Exception as e:
            print(f"[ERROR] Errore durante la trascrizione OpenVINO GenAI: {e}")
            return ''

class VoxtralTranscriber:
    def __init__(self, language="it"):
        print(f"[INFO] Inizializzando Voxtral-Mini-3B per lingua: {language}...")
        
        if not VOXTRAL_AVAILABLE:
            print("[ERROR] Voxtral non disponibile. Installa con: pip install transformers mistral_common")
            raise ImportError("Voxtral dependencies not available")
        
        self.language = language
        self.model_id = "mistralai/Voxtral-Mini-3B-2507"
        
        # Mappa delle lingue per Voxtral
        self.language_mapping = {
            "it": "italian",
            "en": "english", 
            "es": "spanish",
            "fr": "french",
            "de": "german",
            "pt": "portuguese",
            "hi": "hindi",
            "nl": "dutch"
        }
        
        try:
            print(f"[INFO] Caricamento modello Voxtral: {self.model_id}")
            
            # Carica il processore e il modello
            self.processor = VoxtralProcessor.from_pretrained(self.model_id)
            self.model = VoxtralForConditionalGeneration.from_pretrained(
                self.model_id, 
                torch_dtype=torch.bfloat16,
                device_map="auto" if torch.cuda.is_available() else "cpu"
            )
            
            print(f"[INFO] Voxtral caricato con successo - GPU: {torch.cuda.is_available()}")
            print(f"[INFO] Lingua impostata: {self.language}")
            
        except Exception as e:
            print(f"[ERROR] Errore durante il caricamento di Voxtral: {e}")
            raise

    def get_transcription(self, wav_file_path):
        try:
            # Crea la conversazione per la trascrizione
            conversation = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "audio",
                            "path": wav_file_path,
                        },
                    ],
                }
            ]
            
            # Applica il template di chat
            inputs = self.processor.apply_chat_template(conversation)
            inputs = inputs.to(self.model.device, dtype=torch.bfloat16)
            
            # Genera la trascrizione
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=500,
                    temperature=0.0,  # Per trascrizione precisa
                    do_sample=False
                )
            
            # Decodifica il risultato
            transcription = self.processor.batch_decode(
                outputs[:, inputs.input_ids.shape[1]:], 
                skip_special_tokens=True
            )[0]
            
            return transcription.strip()
            
        except Exception as e:
            print(f"[ERROR] Errore durante la trascrizione Voxtral: {e}")
            return ''
    
    def get_audio_understanding(self, wav_file_path, question="Trascrivi questo audio"):
        """
        Metodo avanzato per comprensione audio con domande personalizzate
        """
        try:
            conversation = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "audio",
                            "path": wav_file_path,
                        },
                        {
                            "type": "text", 
                            "text": question
                        }
                    ],
                }
            ]
            
            inputs = self.processor.apply_chat_template(conversation)
            inputs = inputs.to(self.model.device, dtype=torch.bfloat16)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=500,
                    temperature=0.2,
                    top_p=0.95
                )
            
            result = self.processor.batch_decode(
                outputs[:, inputs.input_ids.shape[1]:], 
                skip_special_tokens=True
            )[0]
            
            return result.strip()
            
        except Exception as e:
            print(f"[ERROR] Errore durante la comprensione audio Voxtral: {e}")
            return ''
            return ''