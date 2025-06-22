import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN
from typing import List, Dict, Any
from codex_alchemy.vault import restore
import datetime

# --- EWMA Helper ---
def ewma(series, alpha=0.3):
    return series.ewm(alpha=alpha).mean()

# --- Main Drift Detection ---
def detect_drift(sigil: str = "default") -> Dict[str, Any]:
    glyphs = restore(sigil)
    if not glyphs:
        return {"status": "empty", "drifted": [], "details": []}

    # Extract features
    names = []
    vectors = []
    timestamps = []
    lineage_depths = []
    for g in glyphs:
        names.append(getattr(g, "name", "unknown"))
        vectors.append(np.array(getattr(g, "vector", [0]*10)))
        timestamps.append(getattr(g, "timestamp", datetime.datetime.now().timestamp()))
        lineage_depths.append(getattr(g, "lineage_depth", 0))
    X = np.stack(vectors)
    df = pd.DataFrame({
        "name": names,
        "timestamp": timestamps,
        "lineage_depth": lineage_depths
    })

    # DBSCAN for cluster anomaly
    db = DBSCAN(eps=1.5, min_samples=2).fit(X)
    df["cluster"] = db.labels_
    df["anomaly"] = df["cluster"] == -1

    # EWMA for drift (on each vector dim)
    drift_scores = np.abs(X - ewma(pd.DataFrame(X)).values)
    drift_magnitude = drift_scores.mean(axis=1)
    df["drift"] = drift_magnitude

    # Categorize
    drifted = []
    for i, row in df.iterrows():
        cat = []
        if row["anomaly"]:
            cat.append("Drifting")
        if row["drift"] > 0.8:
            cat.append("Rapid Drift")
        if row["lineage_depth"] == 0:
            cat.append("Unlinked")
        if (datetime.datetime.now().timestamp() - row["timestamp"]) > 7*24*3600:
            cat.append("Stale")
        if cat:
            drifted.append({
                "name": row["name"],
                "categories": cat,
                "drift_score": float(row["drift"]),
                "cluster": int(row["cluster"]),
            })
    return {
        "status": "ok",
        "drifted": drifted,
        "total": len(glyphs),
        "details": drifted,
    } 