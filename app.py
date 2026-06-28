"""西洋棋遊戲 - 主頁面"""
import streamlit as st
import sys
from pathlib import Path

# 將遊戲模組加入路徑
sys.path.insert(0, str(Path(__file__).parent))

from game.game_state import GameMode, Difficulty

st.set_page_config(
    page_title="西洋棋 - Chess Game",
    page_icon="♔",
    layout="centered"
)

# 標題
st.markdown("""
<h1 style="text-align: center; font-size: 3em;">
    ♔ 西方棋 ♚
</h1>
<p style="text-align: center; color: #666; font-size: 1.2em;">
    Western Chess · 完整西洋棋遊戲
</p>
""", unsafe_allow_html=True)

st.divider()

# 模式選擇
st.markdown("## 🎮 選擇遊戲模式")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 👥 雙人對戰
    與朋友面對面對弈
    """)
    if st.button("開始 PvP", type="primary", use_container_width=True):
        st.switch_page("pages/1_PvP.py")

with col2:
    st.markdown("""
    ### 🤖 對戰電腦
    單人挑戰 AI（可選難度）
    """)
    if st.button("開始 vs AI", type="primary", use_container_width=True):
        st.switch_page("pages/2_PvAI.py")

with col3:
    st.markdown("""
    ### 📚 新手教學
    學習各棋種走法
    """)
    if st.button("開始學習", type="secondary", use_container_width=True):
        st.switch_page("pages/3_Tutorial.py")

st.divider()

# 說明
st.markdown("""
## 🎯 功能特色

| 功能 | 說明 |
|------|------|
| ♟️ **完整棋規** | 合法走法、將軍、將死、兵的升變 |
| 🎚️ **三種難度** | 新手 / 一般 / 困難 |
| 📖 **新手教學** | 各棋種走法詳解 |
| 🖥️ **跨平台** | 可部署到 Render.com 雲端 |

## ♟️ 棋子價值參考

| 棋子 | 價值 | 說明 |
|------|------|------|
| ♙ ♟ 兵 | 1 | 數量多，靈活但脆弱 |
| ♘ ♞ 馬 | 3 | 走法獨特，適合开局 |
| ♗ ♝ 象 | 3 | 斜向移動，遠距離火力 |
| ♖ ♜ 車 | 5 | 直線移動，強大主力 |
| ♕ ♛ 后 | 9 | 結合車+象，最強棋子 |
| ♔ ♚ 王 | ∞ | 生死之球，必須保護 |
""")

st.divider()
st.caption("Made with ♡ by 茶叔 · Powered by Streamlit + python-chess")