import sys
import threading
import queue
import time
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QSplitter, QTextEdit, QListWidget, 
                             QListWidgetItem, QPushButton, QLabel, QComboBox,
                             QLineEdit, QMessageBox, QDialog, QDialogButtonBox,
                             QFormLayout, QFrame, QScrollArea, QToolBar, QStatusBar)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QIcon, QAction, QPalette, QColor

from AudioTranscriber import AudioTranscriber
import AudioRecorder
import TranscriberModels
from database import DatabaseManager

class ModernEcouteApp(QMainWindow):
    def __init__(self, use_api=False, use_ollama=False, use_openvino=False, use_voxtral=False, use_openvino_genai=False, language="it"):
        super().__init__()
        self.db = DatabaseManager()
        self.current_transcription = None
        self.current_folder_id = None
        self.is_recording = True  # Attiva la registrazione di default
        
        # Store model parameters
        self.use_api = use_api
        self.use_ollama = use_ollama
        self.use_openvino = use_openvino
        self.use_voxtral = use_voxtral
        self.use_openvino_genai = use_openvino_genai
        self.language = language
        
        # Setup audio components
        self.setup_audio()
        
        # Setup UI
        self.setup_ui()
        self.setup_styles()
        
        # Setup timer for UI updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_transcript_display)
        self.timer.start(300)  # Update every 300ms
        
        # Load initial data
        self.load_transcriptions()
        
    def setup_audio(self):
        """Inizializza i componenti audio"""
        self.speaker_queue = queue.Queue()
        self.mic_queue = queue.Queue()
        
        # Setup audio recorders
        self.user_audio_recorder = AudioRecorder.DefaultMicRecorder()
        self.user_audio_recorder.record_into_queue(self.mic_queue)
        
        time.sleep(1)  # Wait for mic to initialize
        
        self.speaker_audio_recorder = AudioRecorder.DefaultSpeakerRecorder()
        self.speaker_audio_recorder.record_into_queue(self.speaker_queue)
        
        # Setup transcriber
        initial_model = TranscriberModels.get_model(
            use_api=self.use_api, 
            language=self.language, 
            use_ollama=self.use_ollama, 
            use_openvino=self.use_openvino, 
            use_voxtral=self.use_voxtral,
            use_openvino_genai=self.use_openvino_genai
        )
        self.transcriber = AudioTranscriber(
            self.user_audio_recorder.source, 
            self.speaker_audio_recorder.source, 
            initial_model
        )
        
        # Start transcription thread
        self.transcribe_thread = threading.Thread(
            target=self.transcriber.transcribe_audio_queue, 
            args=(self.speaker_queue, self.mic_queue)
        )
        self.transcribe_thread.daemon = True
        self.transcribe_thread.start()
        
    def setup_ui(self):
        """Configura l'interfaccia utente"""
        self.setWindowTitle("Ecoute - Trascrizioni Moderne")
        self.setGeometry(100, 100, 1400, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left sidebar
        self.create_sidebar(splitter)
        
        # Right main area
        self.create_main_area(splitter)
        
        # Set splitter proportions
        splitter.setSizes([300, 1100])
        
        # Create toolbar
        self.create_toolbar()
        
        # Create status bar
        self.create_status_bar()
        
    def create_sidebar(self, parent):
        """Crea la sidebar sinistra"""
        sidebar = QFrame()
        sidebar.setFixedWidth(300)
        sidebar.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout(sidebar)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header = QLabel("📁 Trascrizioni")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(header)
        
        # New transcription button
        new_btn = QPushButton("➕ Nuova Trascrizione")
        new_btn.clicked.connect(self.create_new_transcription)
        layout.addWidget(new_btn)
        
        # Transcriptions list
        self.transcriptions_list = QListWidget()
        self.transcriptions_list.itemClicked.connect(self.load_transcription)
        layout.addWidget(self.transcriptions_list)
        
        parent.addWidget(sidebar)
        
    def create_main_area(self, parent):
        """Crea l'area principale"""
        main_area = QFrame()
        layout = QVBoxLayout(main_area)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Controls header
        controls_layout = QHBoxLayout()
        
        # Language selector
        controls_layout.addWidget(QLabel("Lingua:"))
        self.language_combo = QComboBox()
        self.language_combo.addItems(["it", "en", "es", "fr", "de"])
        self.language_combo.currentTextChanged.connect(self.change_language)
        controls_layout.addWidget(self.language_combo)
        
        controls_layout.addStretch()
        
        # Recording status
        self.recording_status = QLabel("🔴 Registrazione Attiva")
        self.recording_status.setFont(QFont("Arial", 10))
        controls_layout.addWidget(self.recording_status)
        
        layout.addLayout(controls_layout)
        
        # Title input
        title_layout = QHBoxLayout()
        title_layout.addWidget(QLabel("Titolo:"))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Inserisci il titolo della trascrizione...")
        title_layout.addWidget(self.title_input)
        layout.addLayout(title_layout)
        
        # Main text area
        self.text_area = QTextEdit()
        self.text_area.setFont(QFont("Arial", 12))
        self.text_area.setPlaceholderText("La trascrizione apparirà qui in tempo reale...")
        layout.addWidget(self.text_area)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Salva")
        save_btn.clicked.connect(self.save_transcription)
        buttons_layout.addWidget(save_btn)
        
        clear_btn = QPushButton("🗑️ Cancella")
        clear_btn.clicked.connect(self.clear_transcription)
        buttons_layout.addWidget(clear_btn)
        
        export_btn = QPushButton("📤 Esporta")
        export_btn.clicked.connect(self.export_transcription)
        buttons_layout.addWidget(export_btn)
        
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        parent.addWidget(main_area)
        
    def create_toolbar(self):
        """Crea la toolbar"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # File actions
        new_action = QAction("Nuovo", self)
        new_action.triggered.connect(self.create_new_transcription)
        toolbar.addAction(new_action)
        
        save_action = QAction("Salva", self)
        save_action.triggered.connect(self.save_transcription)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Recording actions
        self.record_action = QAction("Ferma Registrazione", self)
        self.record_action.triggered.connect(self.toggle_recording)
        toolbar.addAction(self.record_action)
        
    def create_status_bar(self):
        """Crea la status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Pronto - Supporto Italiano Attivo")
        
    def setup_styles(self):
        """Applica gli stili moderni"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QFrame {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 8px;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 2px solid #555555;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QListWidget {
                background-color: #1e1e1e;
                border: 1px solid #555555;
                border-radius: 6px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #555555;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
            }
            QComboBox {
                background-color: #1e1e1e;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px;
                min-width: 60px;
            }
            QLineEdit {
                background-color: #1e1e1e;
                border: 1px solid #555555;
                border-radius: 4px;
                padding: 5px;
            }
            QLabel {
                color: #ffffff;
            }
            QToolBar {
                background-color: #3c3c3c;
                border: none;
                spacing: 3px;
            }
            QStatusBar {
                background-color: #3c3c3c;
                color: #ffffff;
            }
        """)
        
    def load_transcriptions(self):
        """Carica le trascrizioni dal database"""
        self.transcriptions_list.clear()
        transcriptions = self.db.get_transcriptions()
        
        for transcription in transcriptions:
            item = QListWidgetItem(f"📝 {transcription.title}")
            item.setData(Qt.ItemDataRole.UserRole, transcription.id)
            self.transcriptions_list.addItem(item)
            
    def load_transcription(self, item):
        """Carica una trascrizione selezionata"""
        transcription_id = item.data(Qt.ItemDataRole.UserRole)
        transcription = self.db.session.query(self.db.Transcription).filter_by(id=transcription_id).first()
        
        if transcription:
            self.current_transcription = transcription
            self.title_input.setText(transcription.title)
            self.text_area.setPlainText(transcription.content)
            self.language_combo.setCurrentText(transcription.language)
            
    def create_new_transcription(self):
        """Crea una nuova trascrizione"""
        self.current_transcription = None
        self.title_input.clear()
        self.text_area.clear()
        self.title_input.setPlaceholderText("Nuova trascrizione...")
        
    def save_transcription(self):
        """Salva la trascrizione corrente"""
        title = self.title_input.text() or f"Trascrizione {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        content = self.text_area.toPlainText()
        language = self.language_combo.currentText()
        
        if self.current_transcription:
            # Update existing
            self.db.update_transcription(self.current_transcription.id, title, content)
        else:
            # Create new
            self.current_transcription = self.db.create_transcription(title, content, language)
            
        self.load_transcriptions()
        self.status_bar.showMessage(f"Trascrizione '{title}' salvata!", 3000)
        
    def clear_transcription(self):
        """Cancella la trascrizione corrente"""
        self.transcriber.clear_transcript_data()
        self.text_area.clear()
        
    def export_transcription(self):
        """Esporta la trascrizione"""
        # TODO: Implementare esportazione
        QMessageBox.information(self, "Esportazione", "Funzionalità di esportazione in arrivo!")
        
    def change_language(self, language):
        """Cambia la lingua del modello"""
        self.language = language
        new_model = TranscriberModels.get_model(
            use_api=self.use_api, 
            language=language, 
            use_ollama=self.use_ollama, 
            use_openvino=self.use_openvino, 
            use_voxtral=self.use_voxtral,
            use_openvino_genai=self.use_openvino_genai
        )
        self.transcriber.update_model(new_model)
        self.clear_transcription()
        self.status_bar.showMessage(f"Lingua cambiata a: {language}", 3000)
        
    def toggle_recording(self):
        """Attiva/disattiva la registrazione"""
        self.is_recording = not self.is_recording
        if self.is_recording:
            self.recording_status.setText("🔴 Registrazione Attiva")
            self.record_action.setText("Ferma Registrazione")
        else:
            self.recording_status.setText("⏸️ Registrazione Pausa")
            self.record_action.setText("Avvia Registrazione")
            
    def update_transcript_display(self):
        """Aggiorna il display della trascrizione"""
        if self.is_recording:
            transcript = self.transcriber.get_transcript()
            if transcript and transcript.strip():
                print(f"[DEBUG] Trascrizione ricevuta: {transcript[:100]}...")  # Debug
                self.text_area.setPlainText(transcript)
                # Auto-scroll to bottom
                cursor = self.text_area.textCursor()
                cursor.movePosition(cursor.MoveOperation.End)
                self.text_area.setTextCursor(cursor)
                
    def closeEvent(self, event):
        """Gestisce la chiusura dell'applicazione"""
        self.db.session.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # Set dark theme
    app.setStyle('Fusion')
    
    # Parse command line arguments
    use_ollama = '--ollama' in sys.argv
    use_api = '--api' in sys.argv
    use_openvino = '--openvino' in sys.argv
    use_voxtral = '--voxtral' in sys.argv
    use_openvino_genai = '--openvino-genai' in sys.argv
    
    # Determine language
    language = "it"  # Default
    for arg in sys.argv:
        if arg.startswith('--lang='):
            language = arg.split('=')[1]
    
    # Show which model is being used
    model_type = "FasterWhisper (Local)"
    if use_openvino_genai:
        model_type = "OpenVINO GenAI (Local)"
    elif use_voxtral:
        model_type = "Voxtral-Mini-3B (Local)"
    elif use_openvino:
        model_type = "OpenVINO Whisper (Local)"
    elif use_ollama:
        model_type = "Ollama Whisper (Local)"
    elif use_api:
        model_type = "OpenAI Whisper (API)"
    
    print(f"🎙️  Avvio Ecoute Modern con {model_type}")
    print(f"🌍 Lingua: {language}")
    
    window = ModernEcouteApp(
        use_api=use_api, 
        use_ollama=use_ollama, 
        use_openvino=use_openvino, 
        use_voxtral=use_voxtral,
        use_openvino_genai=use_openvino_genai,
        language=language
    )
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 