import pandas as pd
import numpy as np

def safe_fill_scores(df: pd.DataFrame, cols=None):
    if cols is None:
        cols = ["SSS", "CDS", "SE"]
    out = df.copy()
    for c in cols:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce").fillna(0.0)
    return out

def normalize_series(s: pd.Series):
    s = pd.to_numeric(s, errors="coerce")
    if s.isna().all():
        return s.fillna(0.0)
    mn, mx = s.min(), s.max()
    if mx == mn:
        return s.fillna(0.0) * 0
    return (s - mn) / (mx - mn)

def compute_composite_stress(df: pd.DataFrame, w_sss=0.5, w_cds=0.3, w_se=0.2):
    out = safe_fill_scores(df)
    for c in ["SSS", "CDS", "SE"]:
        if c not in out.columns:
            out[c] = 0.0

    s1 = normalize_series(out["SSS"])
    s2 = normalize_series(out["CDS"])
    s3 = normalize_series(out["SE"])

    out["stress_index"] = w_sss * s1 + w_cds * s2 + w_se * s3
    return out
