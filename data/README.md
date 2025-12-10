# Data specification (processed)

このアプリは **巨大な生データを使いません**。  
Colab で軽量化・集計したCSVを `data/processed/` に置くことで動きます。

---

## 1. mesh_location.csv (必須)

### 用途
- Insight Map のベース地図（メッシュ単位の地理+リスク）

### 必須カラム
- mesh_id (str)
- lon (float)
- lat (float)

### 推奨カラム
- n_cases (int)
- risk_score (float)  
  ※ NaNが多い場合、地図の解釈性が落ちます。  
  risk_score が無い/NaNでも動作はします。

---

## 2. mesh_hospital_case_matrix.csv (推奨)

### 用途
- 病院依存構造の計算や説明に使用

### 必須カラム
- mesh_id (str)
- hospital_name (str)
- n_cases (int)

### 推奨カラム
- share (float)  # 同メッシュ内の病院シェア
- risk_score (float)

---

## 3. hospital_stress_scores.csv (必須)

### 用途
- Hospital Stress Explorer のランキング/比較

### 必須カラム
- hospital_name (str)
- SSS (float)
- CDS (float)
- SE  (float)

### 推奨カラム
- total_cases (int)
- mean_risk (float)
- lon (float)
- lat (float)

---

## 4. hospital_stress_with_groups.csv (推奨)

### 用途
- Dependency Groups ページのクラスター表示

### 必須カラム
- hospital_name (str)
- group_id (int or str)

### 推奨カラム
- SSS, CDS, SE
- total_cases
- lon, lat

---

## 置き場所
