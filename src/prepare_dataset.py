import re
from pathlib import Path
from typing import List

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
EXT = BASE / "data" / "external"
PROC = BASE / "data" / "processed"
PROC.mkdir(parents=True, exist_ok=True)

# <- jeśli plik nazywa się inaczej, zmień tutaj:
INPUT = EXT / "dataset.csv"
OUTPUT = PROC / "clean_dataset.csv"

# oczekiwane kolumny (nie wszystkie muszą być w wejściu)
FEATURE_COLS = [
    "danceability","energy","valence","tempo","loudness",
    "acousticness","instrumentalness","liveness","speechiness",
    "key","mode","duration_ms","time_signature"
]
META_COLS = [
    "track_id","uri","track_name","name","title","artist","artists",
    "album","release_date","popularity","rank","snapshot_date","artist_genres"
]

def normalize_text(s: str) -> str:
    if pd.isna(s):
        return ""
    s = str(s).strip()
    s = re.sub(r"\s+", " ", s)
    return s

def main():
    if not INPUT.exists():
        raise SystemExit(f"Nie znaleziono {INPUT}. Umieść dataset w data/external/dataset.csv")

    df = pd.read_csv(INPUT)

    # --- mapowanie alternatywnych nazw na docelowe ---
    rename_map = {}
    # nazwy utworu
    if "name" in df.columns and "track_name" not in df.columns:
        rename_map["name"] = "track_name"
    if "title" in df.columns and "track_name" not in df.columns:
        rename_map["title"] = "track_name"
    # artyści
    if "artists" in df.columns and "artist" not in df.columns:
        rename_map["artists"] = "artist"
    # id
    if "id" in df.columns and "track_id" not in df.columns:
        rename_map["id"] = "track_id"
    if "spotify_id" in df.columns and "track_id" not in df.columns:
        rename_map["spotify_id"] = "track_id"

    df = df.rename(columns=rename_map)

    # --- standaryzacja typów ---
    # teksty
    for c in ["track_name","artist","album","release_date","uri","artist_genres"]:
        if c in df.columns:
            df[c] = df[c].map(normalize_text)

    # liczby
    numeric_cols = FEATURE_COLS + ["popularity","rank"]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # --- deduplikacja ---
    if "track_id" in df.columns:
        df = df.drop_duplicates(subset=["track_id"], keep="first")
    else:
        # fallback: deduplikacja po (track_name, artist)
        keep_keys = [c for c in ["track_name","artist"] if c in df.columns]
        if keep_keys:
            df = df.drop_duplicates(subset=keep_keys, keep="first")

    # --- sanity: kolumny docelowe w ładnej kolejności ---
    ordered = []
    for c in ["track_id","uri","track_name","artist","album","artist_genres","release_date","popularity","rank"]:
        if c in df.columns: ordered.append(c)
    for c in FEATURE_COLS:
        if c in df.columns: ordered.append(c)
    # dodać resztę na koniec
    ordered += [c for c in df.columns if c not in ordered]

    df = df[ordered]

    # --- krótkie staty (wypis do konsoli) ---
    print(f"[INFO] Wejście: {INPUT.name} -> wiersze={len(df)} kolumny={len(df.columns)}")
    present_feats = [c for c in FEATURE_COLS if c in df.columns]
    print(f"[INFO] Dostępne feature’y: {present_feats}")

    # jaki % braków w kluczowych cechach
    core = [c for c in ["danceability","energy","valence"] if c in df.columns]
    if core:
        na_rate = df[core].isna().mean().round(3)
        print("[INFO] NaN rate (core feats):")
        print(na_rate.to_string())
        # opcjonalnie: odfiltruj rekordy bez core features
        # df = df.dropna(subset=core)

    # --- zapis ---
    df.to_csv(OUTPUT, index=False)
    print(f"[OK] Zapisano: {OUTPUT} (rows={len(df)}, cols={len(df.columns)})")

if __name__ == "__main__":
    main()
