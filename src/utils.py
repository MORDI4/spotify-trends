from pathlib import Path

# Ścieżki do danych
DATA_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

def ensure_dirs():
    """Utwórz katalogi data/raw i data/processed, jeśli nie istnieją."""
    
