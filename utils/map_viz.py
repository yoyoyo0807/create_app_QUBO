import pandas as pd
import folium

def base_map(center_lat=38.2682, center_lon=140.8694, zoom=11):
    return folium.Map(location=[center_lat, center_lon], zoom_start=zoom, tiles="cartodbpositron")

def add_mesh_points(m, df_mesh: pd.DataFrame, value_col: str = "risk_score"):
    """
    メッシュ点を描画。 value_col が NaNでも動く。
    """
    df = df_mesh.copy()
    if value_col not in df.columns:
        value_col = None

    for _, r in df.iterrows():
        lat, lon = r.get("lat"), r.get("lon")
        if pd.isna(lat) or pd.isna(lon):
            continue

        val = None if value_col is None else r.get(value_col)
        # 色はシンプルに3段階
        if val is None or pd.isna(val):
            color = "#111111"  # NaNは黒
        else:
            try:
                v = float(val)
            except Exception:
                v = None
            if v is None:
                color = "#111111"
            elif v >= 0.7:
                color = "#d00000"
            elif v >= 0.6:
                color = "#ff7b00"
            else:
                color = "#ffffff"

        folium.CircleMarker(
            location=[lat, lon],
            radius=4,
            color=color,
            fill=True,
            fill_opacity=0.85,
            weight=0.5,
            tooltip=f"{r.get('mesh_id','')}"
        ).add_to(m)

    return m

def add_hospital_points(m, df_h: pd.DataFrame, label_col="hospital_name", value_col="stress_index"):
    df = df_h.copy()
    if value_col not in df.columns:
        value_col = None

    for _, r in df.iterrows():
        lat, lon = r.get("lat"), r.get("lon")
        if pd.isna(lat) or pd.isna(lon):
            continue

        val = None if value_col is None else r.get(value_col)
        if val is None or pd.isna(val):
            color = "#333333"
            radius = 5
        else:
            try:
                v = float(val)
            except Exception:
                v = 0.0
            # 0〜1想定
            radius = 5 + 10 * max(0.0, min(1.0, v))
            # 赤〜白の簡易表現
            color = "#d00000" if v >= 0.7 else ("#ff7b00" if v >= 0.5 else "#ffffff")

        folium.CircleMarker(
            location=[lat, lon],
            radius=radius,
            color=color,
            fill=True,
            fill_opacity=0.85,
            weight=0.8,
            tooltip=f"{r.get(label_col,'')}"
        ).add_to(m)

    return m
