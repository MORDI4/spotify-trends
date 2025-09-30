# Spotify Trends

Celem projektu jest przećwiczenie całego procesu pracy w data science – od zdobycia danych (Spotify API), przez ich oczyszczenie i analizę eksploracyjną (EDA), po stworzenie prostego modelu ML przewidującego popularność piosenek. Na koniec przygotowana zostanie wizualizacja i dokumentacja wyników w formie notatnika Jupyter i README. Dzięki temu projekt pokazuje pełny workflow ‘end-to-end’ w praktyce.

## ⚙️ Wymagania
Python 3.10+ i `pip`.

## 🚀 Szybki start
```bash
# 1) (opcjonalnie) wirtualne środowisko
python -m venv .venv
# Win: .venv\Scripts\activate   |   macOS/Linux: source .venv/bin/activate

# 2) Zależności
pip install -r requirements.txt

# 3) Kernel do Jupytera (jednorazowo)
python -m ipykernel install --user --name spotify-trends --display-name "Python (spotify-trends)"
