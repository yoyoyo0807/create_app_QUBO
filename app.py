import streamlit as st

st.set_page_config(
    page_title="都市救急 システミックリスク Insight",
    layout="wide"
)

st.title("🚑 都市救急 システミックリスク Insight")
st.markdown("### “結果がひと目でわかる” を最優先にした Insight 중심ダッシュボード")

st.markdown("""
---
## このアプリの狙い

従来のような
- 120×120相関の“資料的な表示”
- QUBO vs Rankの表の羅列

ではなく、

**「このショックが起きると、どの地域と病院群が連鎖的に危ないのか」**  
を

1. 地図  
2. 病院ストレス  
3. 依存グルーピング  

の3視点で **意思決定に直結する形** で示します。

---

### 左のサイドバーからページを選んでください。
""")
