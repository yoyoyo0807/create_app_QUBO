import os
from dataclasses import dataclass
from typing import List, Optional, Tuple

import pandas as pd
import streamlit as st

from .ui import show_data_missing

DEFAULT_DIRS = [
    "data/processed",
    "data",
    "./data/processed",
    "./data",
]

@dataclass
class LoadResult:
    df: pd.DataFrame
    path: str
    tried: List[str]

def _find_file(filename: str, extra_dirs: Optional[List[str]] = None) -> Tuple[Optional[str], List[str]]:
    dirs = list(DEFAULT_DIRS)
    if extra_dirs:
        dirs = extra_dirs + dirs

    tried = []
    for d in dirs:
        p = os.path.join(d, filename)
        tried.append(os.path.abspath(p))
        if os.path.exists(p):
            return p, tried

    return None, tried

def _require_cols(df: pd.DataFrame, required: List[str], label: str):
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"[{label}] missing columns: {missing}")

@st.cache_data(show_spinner=False)
def load_csv(filename: str, required: Optional[List[str]] = None, label: str = "") -> LoadResult:
    path, tried = _find_file(filename)
    if not path:
        show_data_missing(
            f"❌ データファイルが見つかりませんでした: {filename}",
            tried_paths=tried
        )

    df = pd.read_csv(path)
    if required:
        _require_cols(df, required, label or filename)

    return LoadResult(df=df, path=path, tried=tried)

# ---- specific loaders ----

@st.cache_data(show_spinner=False)
def load_mesh_location() -> pd.DataFrame:
    res = load_csv(
        "mesh_location.csv",
        required=["mesh_id", "lon", "lat"],
        label="mesh_location"
    )
    return res.df

@st.cache_data(show_spinner=False)
def load_mesh_hospital_matrix() -> pd.DataFrame:
    # 推奨データ：無くてもページによっては動く設計にするため例外は呼び出し側で扱う
    res = load_csv(
        "mesh_hospital_case_matrix.csv",
        required=["mesh_id", "hospital_name", "n_cases"],
        label="mesh_hospital_case_matrix"
    )
    return res.df

@st.cache_data(show_spinner=False)
def load_hospital_scores() -> pd.DataFrame:
    res = load_csv(
        "hospital_stress_scores.csv",
        required=["hospital_name", "SSS", "CDS", "SE"],
        label="hospital_stress_scores"
    )
    return res.df

@st.cache_data(show_spinner=False)
def load_hospital_groups() -> pd.DataFrame:
    res = load_csv(
        "hospital_stress_with_groups.csv",
        required=["hospital_name", "group_id"],
        label="hospital_stress_with_groups"
    )
    return res.df
