import threading
from AudioTranscriber import AudioTranscriber
import customtkinter as ctk
import AudioRecorder 
import queue
import time
import sys
import TranscriberModels
import subprocess

def write_in_textbox(textbox, text):
    textbox.delete("0.0", "end")
    textbox.insert("0.0", text)

def update_transcript_UI(transcriber, textbox):
    transcript_string = transcriber.get_transcript()
    write_in_textbox(textbox, transcript_string)
    textbox.after(300, update_transcript_UI, transcriber, textbox)

def clear_context(transcriber, speaker_queue, mic_queue):
    transcriber.clear_transcript_data()

    with speaker_queue.mutex:
        speaker_queue.queue.clear()
    with mic_queue.mutex:
        mic_queue.queue.clear()

def change_language(transcriber, speaker_queue, mic_queue, language_var):
    """Cambia la lingua del modello di trascrizione"""
    new_language = language_var.get()
    print(f"[INFO] Cambiando lingua a: {new_language}")
    
    # Determina quale modello usare
    use_ollama = '--ollama' in sys.argv
    use_api = '--api' in sys.argv
    use_openvino = '--openvino' in sys.argv
    use_voxtral = '--voxtral' in sys.argv
    use_openvino_genai = '--openvino-genai' in sys.argv
    
    # Ricrea il modello con la nuova lingua
    new_model = TranscriberModels.get_model(use_api=use_api, language=new_language, use_ollama=use_ollama, use_openvino=use_openvino, use_voxtral=use_voxtral, use_openvino_genai=use_openvino_genai)
    # Non usare model_var.set() perché converte l'oggetto in stringa
    # Aggiorna direttamente il modello nel trascrittore
    transcriber.update_model(new_model)
    
    # Pulisci il contesto
    clear_context(transcriber, speaker_queue, mic_queue)

def create_ui_components(root, transcriber, speaker_queue, mic_queue):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    root.title("Ecoute - Riconoscimento Vocale")
    root.geometry("1000x700")

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    
    main_frame = ctk.CTkFrame(root)
    main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_rowconfigure(1, weight=0)
    main_frame.grid_rowconfigure(2, weight=0)

    # Frame per i controlli
    controls_frame = ctk.CTkFrame(main_frame)
    controls_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
    controls_frame.grid_columnconfigure(0, weight=1)
    controls_frame.grid_columnconfigure(1, weight=0)
    controls_frame.grid_columnconfigure(2, weight=0)

    # Label per la lingua
    language_label = ctk.CTkLabel(controls_frame, text="Lingua:", font=("Arial", 14))
    language_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

    # Menu a tendina per la lingua
    language_var = ctk.StringVar(value="it")
    language_menu = ctk.CTkOptionMenu(
        controls_frame,
        values=["it", "en", "es", "fr", "de"],
        variable=language_var,
        command=lambda x: change_language(transcriber, speaker_queue, mic_queue, language_var)
    )
    language_menu.grid(row=0, column=1, padx=10, pady=10)

    # Label per mostrare la lingua corrente
    current_language_label = ctk.CTkLabel(controls_frame, text="Italiano", font=("Arial", 12))
    current_language_label.grid(row=0, column=2, padx=10, pady=10)

    # Aggiorna la label quando cambia la lingua
    def update_language_label(*args):
        lang_map = {"it": "Italiano", "en": "Inglese", "es": "Spagnolo", "fr": "Francese", "de": "Tedesco"}
        current_language_label.configure(text=lang_map.get(language_var.get(), language_var.get()))

    language_var.trace("w", update_language_label)

    transcript_textbox = ctk.CTkTextbox(
        main_frame, 
        font=("Arial", 20), 
        text_color='#FFFCF2', 
        wrap="word"
    )
    transcript_textbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    clear_button = ctk.CTkButton(
        main_frame, 
        text="Cancella Trascrizione", 
        command=lambda: clear_context(transcriber, speaker_queue, mic_queue)
    )
    clear_button.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 10))

    return transcript_textbox, language_var

def main():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("ERROR: The ffmpeg library is not installed. Please install ffmpeg and try again.")
        return

    root = ctk.CTk()
    speaker_queue = queue.Queue()
    mic_queue = queue.Queue()

    user_audio_recorder = AudioRecorder.DefaultMicRecorder()
    user_audio_recorder.record_into_queue(mic_queue)

    time.sleep(2)

    speaker_audio_recorder = AudioRecorder.DefaultSpeakerRecorder()
    speaker_audio_recorder.record_into_queue(speaker_queue)

    # Determina quale modello usare
    use_ollama = '--ollama' in sys.argv
    use_api = '--api' in sys.argv
    use_openvino = '--openvino' in sys.argv
    use_voxtral = '--voxtral' in sys.argv
    use_openvino_genai = '--openvino-genai' in sys.argv
    
    initial_model = TranscriberModels.get_model(use_api=use_api, language="it", use_ollama=use_ollama, use_openvino=use_openvino, use_voxtral=use_voxtral, use_openvino_genai=use_openvino_genai)

    transcriber = AudioTranscriber(user_audio_recorder.source, speaker_audio_recorder.source, initial_model)
    transcribe = threading.Thread(target=transcriber.transcribe_audio_queue, args=(speaker_queue, mic_queue))
    transcribe.daemon = True
    transcribe.start()

    transcript_textbox, language_var = create_ui_components(root, transcriber, speaker_queue, mic_queue)

    print("PRONTO - Supporto Italiano Attivo")

    update_transcript_UI(transcriber, transcript_textbox)

    root.mainloop()

if __name__ == "__main__":
    main()