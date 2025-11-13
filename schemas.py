"""
Database Schemas for SMAN 1 Kertasari Website

Each Pydantic model corresponds to a MongoDB collection with the
collection name equal to the lowercase class name.

Examples:
- Announcement -> "announcement"
- Event -> "event"
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Announcement(BaseModel):
    """
    Announcements for the school homepage
    Collection: "announcement"
    """
    title: str = Field(..., description="Judul pengumuman")
    content: str = Field(..., description="Isi pengumuman")
    author: Optional[str] = Field(None, description="Penulis atau penanggung jawab")
    category: Optional[str] = Field("Umum", description="Kategori pengumuman")
    published: bool = Field(True, description="Status publikasi")
    date: Optional[datetime] = Field(None, description="Tanggal pengumuman")


class Event(BaseModel):
    """
    School events and agenda
    Collection: "event"
    """
    title: str = Field(..., description="Nama acara")
    description: Optional[str] = Field(None, description="Deskripsi acara")
    location: Optional[str] = Field(None, description="Lokasi acara")
    start_date: datetime = Field(..., description="Waktu mulai")
    end_date: Optional[datetime] = Field(None, description="Waktu selesai")
    organizer: Optional[str] = Field(None, description="Penanggung jawab")
