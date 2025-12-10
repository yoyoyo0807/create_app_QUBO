import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

def ensure_group_column(df: pd.DataFrame, n_groups: int = 6) -> pd.DataFrame:
    """
    group_id が無ければ SSS/CDS/SE から簡易クラスタリングで作る。
    """
    out = df.copy()
    if "group_id" in out.columns:
        return out

    features = []
    for c in ["SSS", "CDS", "SE"]:
        if c in out.columns:
            features.append(pd.to_numeric(out[c], errors="coerce").fillna(0.0))
        else:
            features.append(pd.Series(np.zeros(len(out))))

    X = np.vstack([f.values for f in features]).T
    if len(out) < n_groups:
        n_groups = max(1, len(out) // 2)

    if n_groups <= 1:
        out["group_id"] = 0
        return out

    km = KMeans(n_clusters=n_groups, random_state=42, n_init="auto")
    out["group_id"] = km.fit_predict(X)

    return out

def group_summary(df: pd.DataFrame) -> pd.DataFrame:
    cols = [c for c in ["SSS", "CDS", "SE", "total_cases", "stress_index"] if c in df.columns]
    agg = {c: "mean" for c in cols}
    agg["hospital_name"] = "count"

    g = df.groupby("group_id", dropna=False).agg(agg).rename(columns={"hospital_name": "n_hospitals"})
    g = g.reset_index().sort_values("n_hospitals", ascending=False)
    return g
