from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class Folder(Base):
    __tablename__ = 'folders'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey('folders.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    parent = relationship("Folder", remote_side=[id])
    children = relationship("Folder", back_populates="parent")
    transcriptions = relationship("Transcription", back_populates="folder")

class Transcription(Base):
    __tablename__ = 'transcriptions'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    language = Column(String(10), nullable=False, default='it')
    folder_id = Column(Integer, ForeignKey('folders.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    folder = relationship("Folder", back_populates="transcriptions")

class DatabaseManager:
    def __init__(self, db_path='ecoute.db'):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
        # Aggiungo le classi come attributi per facilitare l'accesso
        self.Transcription = Transcription
        self.Folder = Folder
        
        self._create_default_folder()
    
    def _create_default_folder(self):
        default_folder = self.session.query(Folder).filter_by(name="Trascrizioni", parent_id=None).first()
        if not default_folder:
            default_folder = Folder(name="Trascrizioni", parent_id=None)
            self.session.add(default_folder)
            self.session.commit()
    
    def create_transcription(self, title, content, language='it', folder_id=None):
        if folder_id is None:
            default_folder = self.session.query(Folder).filter_by(name="Trascrizioni", parent_id=None).first()
            folder_id = default_folder.id if default_folder else None
            
        transcription = Transcription(
            title=title,
            content=content,
            language=language,
            folder_id=folder_id
        )
        self.session.add(transcription)
        self.session.commit()
        return transcription
    
    def get_transcriptions(self, folder_id=None):
        if folder_id:
            return self.session.query(Transcription).filter_by(folder_id=folder_id).all()
        return self.session.query(Transcription).all()
    
    def update_transcription(self, transcription_id, title=None, content=None):
        transcription = self.session.query(Transcription).filter_by(id=transcription_id).first()
        if transcription:
            if title:
                transcription.title = title
            if content:
                transcription.content = content
            transcription.updated_at = datetime.utcnow()
            self.session.commit()
        return transcription 