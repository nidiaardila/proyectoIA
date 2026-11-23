import json

with open("registros_latencia_costo.jsonl", encoding="utf-8") as f:
    for linea in f:
        r = json.loads(linea)
        tokens_entrada = r["tokens"]["input_tokens"] if r["tokens"] else None
        tokens_salida = r["tokens"]["output_tokens"] if r["tokens"] else None
        t_busqueda = r["tiempos_ms"].get("embed_y_busqueda")
        t_gen = r["tiempos_ms"].get("generacion")
        print(
            f"k={r['k']} | in={tokens_entrada} out={tokens_salida} | "
            f"busq={t_busqueda} ms gen={t_gen} ms total={r['tiempo_total_ms']} ms | "
            f"{r['pregunta'][:40]}"
        )