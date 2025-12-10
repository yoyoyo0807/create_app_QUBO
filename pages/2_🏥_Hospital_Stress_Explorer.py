import streamlit as st
import pandas as pd

from utils.data_loader import load_hospital_scores
from utils.metrics import compute_composite_stress, safe_fill_scores
from utils.ui import section

st.title("🏥 Hospital Stress Explorer")

section("目的", "🎯")
st.markdown("""
**病院単体の脆弱性**と**優先支援の候補**を  
ランキング形式で把握するページです。

- SSS / CDS / SE を統合した **stress_index** を採用
- 問い合わせ数が少ない病院で率が歪む問題を避けるため  
  `total_cases` があればフィルタで制御できます
""")

df = load_hospital_scores()
df = compute_composite_stress(df)

section("フィルタ", "🧪")
min_cases = 0
if "total_cases" in df.columns:
    max_cases = int(pd.to_numeric(df["total_cases"], errors="coerce").fillna(0).max())
    min_cases = st.slider("最小 total_cases", 0, max_cases, 0, step=max(1, max_cases // 20))
else:
    st.info("total_cases が無いので件数フィルタは無効です。")

if "total_cases" in df.columns:
    df["total_cases"] = pd.to_numeric(df["total_cases"], errors="coerce").fillna(0).astype(int)
    df_f = df[df["total_cases"] >= min_cases].copy()
else:
    df_f = df.copy()

section("ランキング", "📈")
top_n = st.slider("Top-N", 10, 200, 50, step=10)

df_f = safe_fill_scores(df_f)
df_f = df_f.sort_values("stress_index", ascending=False).head(top_n)

st.dataframe(
    df_f[ [c for c in ["hospital_name", "stress_index", "SSS", "CDS", "SE", "total_cases", "mean_risk"] if c in df_f.columns] ],
    width="stretch"
)

section("解釈ガイド", "🧠")
st.markdown("""
- **SSS**：病院のストレス蓄積（構造上の重さ）
- **CDS**：クラスター依存の強さ（連鎖の危うさ）
- **SE** ：ショックへの弾性の低さ（耐性が低いほど高い想定）

このページは**“病院単体の危険度と支援優先度”**にフォーカスします。
""")
