import streamlit as st
import pandas as pd
from streamlit_folium import st_folium

from utils.data_loader import load_hospital_groups, load_hospital_scores
from utils.metrics import compute_composite_stress
from utils.clustering import ensure_group_column, group_summary
from utils.map_viz import base_map, add_hospital_points
from utils.ui import section

st.title("🧩 Hospital Dependency Groups — 連鎖崩壊グループ")

section("目的", "🎯")
st.markdown("""
**“どの病院が同じ運命共同体か”** を作り、  
**連鎖的に崩壊しうる病院群**を可視化するページです。

- `hospital_stress_with_groups.csv` があればそれを使用
- 無ければ `hospital_stress_scores.csv` から簡易クラスタで作成
""")

try:
    df_g = load_hospital_groups()
    source = "hospital_stress_with_groups.csv"
except Exception:
    df_g = load_hospital_scores()
    source = "hospital_stress_scores.csv (fallback)"

df_g = compute_composite_stress(df_g)
df_g = ensure_group_column(df_g, n_groups=6)

section("グループ概要", "📊")
st.caption(f"データソース: {source}")

summ = group_summary(df_g)
st.dataframe(summ, width="stretch")

section("グループ選択", "🧪")
group_ids = list(summ["group_id"].astype(str).unique())
sel = st.multiselect("表示する group_id", options=group_ids, default=group_ids[: min(3, len(group_ids))])

df_show = df_g[df_g["group_id"].astype(str).isin(sel)].copy()

section("地図（病院）", "🗺")
if not {"lon", "lat"}.issubset(df_show.columns):
    st.warning("この地図には hospital の lon/lat が必要です。CSVに lon, lat を追加してください。")
else:
    # map_viz expects lat/lon columns named lat/lon
    df_show = df_show.rename(columns={"lon": "lon", "lat": "lat"})
    m = base_map()
    m = add_hospital_points(m, df_show, value_col="stress_index")
    st_folium(m, width="stretch", height=650)

section("病院リスト", "🏥")
st.dataframe(
    df_show[[c for c in ["hospital_name", "group_id", "stress_index", "SSS", "CDS", "SE", "total_cases"] if c in df_show.columns]],
    width="stretch"
)

section("解釈ガイド", "🧠")
st.markdown("""
**このページが示したいInsightは1つだけです：**

> “個別最適ではなく、グループ単位で支援/代替受入れ/搬送戦略を考えるべき病院群が存在する”

ここが見えると、政策は
- **支援対象を“点”から“面”へ**
- **同時停止の回避**
- **代替先の事前合意**
に進められます。
""")
