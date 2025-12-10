import streamlit as st
import pandas as pd
from streamlit_folium import st_folium

from utils.data_loader import load_mesh_location
from utils.ui import section
from utils.map_viz import base_map, add_mesh_points

st.title("🗺 Insight Map — 地域ショックの見える化")

section("目的", "🎯")
st.markdown("""
**ショックや負荷の増大が“どの地域に集中しうるか”** を  
まず最初に地図上で直感的に把握するページです。

- risk_score が無い/NaNでも描画できます
- NaNが多い場合は黒点が増えるので  
  **データ整備の必要性自体がInsight**になります
""")

df_mesh = load_mesh_location()

section("表示設定", "⚙️")
value_candidates = ["risk_score", "n_cases"]
value_candidates = [c for c in value_candidates if c in df_mesh.columns]
value_col = st.selectbox(
    "色判定に使う指標",
    options=value_candidates if value_candidates else ["(none)"]
)

if value_col == "(none)":
    value_col = "risk_score"  # fallback

max_points = st.slider("表示メッシュ数（上位から）", 50, 500, 200, step=50)

# ソートロジック：risk_score優先 → 無ければn_cases
df_plot = df_mesh.copy()
sort_key = "risk_score" if "risk_score" in df_plot.columns else ("n_cases" if "n_cases" in df_plot.columns else None)

if sort_key:
    df_plot[sort_key] = pd.to_numeric(df_plot[sort_key], errors="coerce")
    df_plot = df_plot.sort_values(sort_key, ascending=False)

df_plot = df_plot.head(max_points)

section("地図", "🧭")
m = base_map()
m = add_mesh_points(m, df_plot, value_col=value_col)

st.caption("色の目安：白=低 / 橙=中 / 赤=高 / 黒=NaN")
st_folium(m, width="stretch", height=650)

section("データ確認", "🧾")
st.dataframe(df_plot, width="stretch")
