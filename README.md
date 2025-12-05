# Valutazione di Modelli Multimodali (MLLM) su Documenti Storici (Dataset CM1)

Questo repository contiene il codice, i dati e i risultati dell'analisi comparativa condotta per valutare le capacità di estrazione *zero-shot* di diversi modelli multimodali (MLLM) sul dataset **CM1**.

L'obiettivo è l'estrazione strutturata di informazioni anagrafiche (`Name`, `Vorname`, `Geb-Dat`) da documenti storici manoscritti complessi.

## 🧠 Modelli Analizzati

1.  **GPT-4o** (Baseline SOTA - Cloud API)
2.  **Qwen3-VL 8B** (Open Source - Esecuzione Locale)
3.  **PaliGemma** (Google)
4.  **Donut** (Document Understanding Transformer)
5.  **Qwen2.5-VL**

## 📊 Sintesi dei Risultati

La sperimentazione ha dimostrato che i modelli open-source standard faticano in modalità zero-shot. Tuttavia, l'applicazione di tecniche di **Prompt Engineering** (normalizzazione date ISO e maiuscole) ha permesso al modello **Qwen3-VL (8B)** di raggiungere prestazioni competitive con lo stato dell'arte.

### Tabella Comparativa (Metriche Finali)

| Modello | Setup | CER Globale | TED (Struttura) | Note |
| :--- | :--- | :--- | :--- | :--- |
| **GPT-4o** | Optimized Prompt | **0.08** (8%) | **0.94** | Performance eccellente e stabile. |
| **Qwen3-VL 8B** | Optimized Prompt | **0.18** (18%) | **0.64** | Ottimo OCR, leggermente instabile su casi limite. |
| **PaliGemma** | Zero-shot | 0.91 (91%) | 0.38 | Non adatto senza fine-tuning specifico. |

*Nota: Le metriche per Qwen3-VL (Optimized) sono calcolate su un campione statisticamente significativo di 50 documenti.*

## 📂 Struttura del Repository

* `notebooks/`: Contiene i Jupyter Notebook utilizzati per l'inferenza dei modelli (Colab).
* `scripts/`: Script Python per la valutazione (`evaluate.py`) e la gestione del dataset.
* `data/`: File JSON di Ground Truth e predizioni generate dai modelli.
* `results/`: Report dettagliati in formato CSV.

## 🚀 Riproducibilità

### 1. Requisiti
Installare le dipendenze necessarie:
```bash
pip install -r requirements.txt
