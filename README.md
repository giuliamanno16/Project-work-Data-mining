# Valutazione di Modelli Multimodali (MLLM) su Documenti Storici (Dataset CM1 )

Questo repository contiene il codice, i dati e i risultati dell'analisi comparativa condotta per valutare le capacità di estrazione *zero-shot* di diversi modelli multimodali (MLLM) sul dataset **CM1**.

L'obiettivo è l'estrazione strutturata di informazioni anagrafiche (`Name`, `Vorname`, `Geb-Dat`) da documenti storici manoscritti complessi.

## 🧠 Modelli Analizzati

1.  **GPT-4o** 
2.  **Qwen3-VL 8B** 
3.  **PaliGemma** 
4.  **Donut** 
5.  **Qwen2.5-VL**

## 📊 Sintesi dei Risultati

La sperimentazione ha dimostrato che i modelli open-source standard faticano in modalità zero-shot. Tuttavia, l'applicazione di tecniche di **Prompt Engineering** (normalizzazione date ISO e maiuscole) ha permesso al modello **Qwen3-VL (8B)** di raggiungere prestazioni competitive con lo stato dell'arte.

### Tabella Comparativa (Metriche Finali)

| Modello | Setup | CER Globale | TED (Struttura) | Note |
| :--- | :--- | :--- | :--- | :--- |
| **GPT-4o** | Optimized Prompt | **0.07** (7%) | **0.92** | Performance eccellente e stabile. |
| **Qwen3-VL 8B** | Optimized Prompt | **0.18** (18%) | **0.64** | Ottimo OCR, calcolato su 50 campioni. |
| **Qwen3-VL 8B** | Optimized Prompt | 0.22 (22%) | 0.68 | Calcolato su 10 campioni. |
| **PaliGemma** | Zero-shot | 0.91 (91%) | 0.38 | Non adatto senza fine-tuning specifico. |
| **Donut** | Zero-shot | N/A | N/A | Output incoerente, metriche non calcolabili. |
| **Qwen2.5-VL** | Zero-shot | N/A | N/A | Output incoerente, metriche non calcolabili. |

*Legenda:*
* **CER (Character Error Rate):** Minore è meglio (0.0 = perfetto).
* **TED (Tree Edit Distance):** Maggiore è meglio (1.0 = struttura perfetta).

## 📂 Struttura del Repository

* `inference_notebooks/`: Contiene i link ai Jupyter Notebook utilizzati per l'esecuzione dei modelli su Google Colab.
* `scripts/`: Script Python per la valutazione (`evaluate.py`).
* `data/`: File JSON di Ground Truth e predizioni generate dai modelli.
* `results/`: Report dettagliati in formato CSV.
* `evaluate_cm1.ipynb`: Notebook principale di analisi e visualizzazione dei grafici.

## 🚀 Notebook di Inferenza (Google Colab)

Per replicare gli esperimenti di inferenza senza occupare risorse locali, utilizzare i seguenti notebook Colab:

| Modello | Link al Notebook | Descrizione |
| :--- | :--- | :--- |
| **Qwen3-VL 8B** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1BY4mQD1t3mpYksCWsssAZsFFaCF61eH9?usp=share_link) | Inferenza locale via Ollama su GPU T4 |
| **PaliGemma** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1BY4mQD1t3mpYksCWsssAZsFFaCF61eH9?usp=share_link) | Inferenza Zero-shot tramite Hugging Face |
| **Donut** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1VY5JXD2rK4URdG13NNIFxtKE3K9xvvE1?usp=share_link) | Test vari checkpoint (Base, DocVQA) |
| **Qwen2.5-VL** | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/15a_furEJ7RcD-ir430cH0T7Xff7T0jww?usp=share_link) | Test modelli 3B/7B |

## 🛠 Metodologia di Valutazione

Per riprodurre le metriche (CER/TED) utilizzando lo script di valutazione standardizzato (che include normalizzazione del testo e allineamento ID):

1.  Installare le dipendenze:
    ```bash
    pip install -r requirements.txt
    ```

2.  Eseguire lo script di valutazione:
    ```bash
    python scripts/evaluate.py data/cm1_cover_test.json data/predictions/predictions_qwen3_8b_50samples.json results/risultati_qwen_8b_50samples.csv
    ```
