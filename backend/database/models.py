"""
SQLAlchemy ORM models for Videos and Prompts tables matching exact database specification.
"""
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(String(64), primary_key=True, index=True)
    filename = Column(String(256), nullable=False)
    file_path = Column(String(512), nullable=False)
    file_size_bytes = Column(Integer, nullable=False)
    duration_seconds = Column(Float, default=0.0)
    resolution = Column(String(32), default="1920x1080")
    status = Column(String(32), default="uploaded")
    style_preset = Column(String(32), default="standard")
    poster_url = Column(String(512), nullable=True)
    analysis_json = Column(JSON, nullable=True)
    prompts_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    prompts = relationship("Prompt", back_populates="video", cascade="all, delete-orphan")


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(String(64), primary_key=True, index=True)
    video_id = Column(String(64), ForeignKey("videos.id"), nullable=False)
    prompt_style = Column(String(32), default="standard") # standard | creative
    prompt_content = Column(Text, nullable=False)
    analysis_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    video = relationship("Video", back_populates="prompts")


# Alias for legacy compatibility
VideoTask = Video
