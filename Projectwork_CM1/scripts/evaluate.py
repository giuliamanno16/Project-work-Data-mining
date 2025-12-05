import json
import csv
import sys
import math
import Levenshtein
from zss import simple_distance, Node

def json_to_tree(entry_list):
    """
    Converte una lista di persone in un albero semplice per calcolare la TED.
    """
    root = Node("root")
    for person in entry_list:
        pnode = Node("person")
        for k, v in person.items():
            # Usa normalize_text anche qui per coerenza
            val_str = normalize_text(v)
            pnode.addkid(Node(f"{k}:{val_str}"))
        root.addkid(pnode)
    return root

def normalize_text(text):
    """
    Fondamentale: Adatta il testo (Maiuscolo, NaN, spazi)
    """
    if text is None:
        return ""
    if isinstance(text, float) and math.isnan(text):
        return ""
    
    # Converte in stringa, rimuove spazi e converte in MAIUSCOLO
    text_str = str(text).strip().upper()
    text_str = " ".join(text_str.split())
    
    return text_str

def cer(s1, s2):
    """
    Calcola Character Error Rate su testo NORMALIZZATO.
    """
    s1_norm = normalize_text(s1)
    s2_norm = normalize_text(s2)
    
    if not s1_norm and not s2_norm:
        return 0.0
        
    return Levenshtein.distance(s1_norm, s2_norm) / max(1, len(s1_norm), len(s2_norm))

def count_nodes(node):
    return 1 + sum(count_nodes(child) for child in node.children)

def compare_entries(gt_entries, pred_entries):
    # 1. CER Globale
    gt_text = " ".join([f"{p.get('Name','')} {p.get('Vorname','')} {p.get('Geb-Dat','')}" for p in gt_entries])
    pred_text = " ".join([f"{p.get('Name','')} {p.get('Vorname','')} {p.get('Geb-Dat','')}" for p in pred_entries])
    cer_global = cer(gt_text, pred_text)

    # 2. CER per Campo
    fields_to_eval = ["Name", "Vorname", "Geb-Dat"]
    field_cer_scores = {field: [] for field in fields_to_eval}
    
    max_len = max(len(gt_entries), len(pred_entries))
    
    for i in range(max_len):
        gt_person = gt_entries[i] if i < len(gt_entries) else {}
        pred_person = pred_entries[i] if i < len(pred_entries) else {}
        
        for field in fields_to_eval:
            gt_val = gt_person.get(field)
            pred_val = pred_person.get(field)
            field_cer = cer(gt_val, pred_val)
            field_cer_scores[field].append(field_cer)

    avg_cer_per_field = {}
    for field, scores in field_cer_scores.items():
        if scores:
            avg_cer_per_field[f"CER_{field}"] = sum(scores) / len(scores)
        else:
            avg_cer_per_field[f"CER_{field}"] = 0.0

    # 3. TED
    gt_tree = json_to_tree(gt_entries)
    pred_tree = json_to_tree(pred_entries)
    d = simple_distance(pred_tree, gt_tree)
    size = count_nodes(gt_tree)
    ted_score = max(0, 1 - d / size) if size > 0 else 0

    return cer_global, avg_cer_per_field, ted_score

def main(gt_file, pred_file, out_csv):
    # Caricamento GT con gestione fallback NaN
    try:
        with open(gt_file, "r", encoding="utf-8") as f:
            ground_truth = json.load(f)
    except json.JSONDecodeError:
        with open(gt_file, "r", encoding="utf-8") as f:
            content = f.read().replace('NaN', 'null')
            ground_truth = json.loads(content)

    with open(pred_file, "r", encoding="utf-8") as f:
        predictions = json.load(f)

    results = []
    totals = {"CER_Global": 0, "CER_Name": 0, "CER_Vorname": 0, "CER_Geb-Dat": 0, "TED": 0}
    count = 0
    fields_per_campo = ["CER_Name", "CER_Vorname", "CER_Geb-Dat"]

    for doc_id, pred_entries in predictions.items():
        
        # === LOGICA DI ALLINEAMENTO  ===
        # 1. Prova ID diretto
        if doc_id in ground_truth:
            gt_entries = ground_truth[doc_id]
        else:
            # 2. Prova ID + 1 (Modifica richiesta) 
            try:
                target_id = str(int(doc_id) + 1)
                gt_entries = ground_truth.get(target_id, [])
                

            except ValueError:
                gt_entries = []

        # Se pred_entries è vuoto o null, trattalo come lista vuota
        if not pred_entries: 
            pred_entries = []

        cer_global, avg_cer_dict, ted_score = compare_entries(gt_entries, pred_entries)
        
        row = [doc_id, round(cer_global, 2)]
        totals["CER_Global"] += cer_global
        
        for field in fields_per_campo:
            score = avg_cer_dict[field]
            row.append(round(score, 2))
            totals[field] += score 
            
        row.append(round(ted_score, 2))
        totals["TED"] += ted_score
        
        results.append(row)
        count += 1

    if count == 0:
        print("Nessun documento processato.")
        return

    # Scrittura CSV
    headers = ["ID", "CER_Global", "CER_Name", "CER_Vorname", "CER_Geb-Dat", "TED"]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(results)
        
        avg_row = ["AVG"]
        for header in headers[1:]:
            avg_row.append(round(totals[header] / count, 2))
        writer.writerow(avg_row)

    print(f"Risultati salvati in {out_csv}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python evaluate.py ground_truth.json predictions.json results.csv")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])