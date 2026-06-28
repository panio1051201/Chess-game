"""新手教學頁面"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from game.board import PIECE_NAMES, PIECE_NAMES_CN
import chess

st.set_page_config(page_title="新手教學 - 西洋棋", page_icon="♔")

st.markdown("# 📚 西洋棋新手教學")
st.markdown("學習每種棋子的獨特走法，成為棋盤大師！")

# 棋子教學數據
PIECES = [
    {
        "type": chess.KING,
        "symbol": "♔ ♚",
        "name": "國王 (King)",
        "value": "∞",
        "color": "white" if False else "black",
        "desc": "國王是棋盤上最重要的棋子，保護國王是遊戲的最高目標！",
        "moves": "國王可以向任何方向（橫、直、斜）移動**一步**。",
        "special": "王車易位（Castling）：當國王和車都未移動過，且中間無棋子時，可一次移動兩格，同時車跳到國王另一側。",
        "example": "殘局時國王可以主動出擊，幫助兵的推進。",
        "emoji": "👑"
    },
    {
        "type": chess.QUEEN,
        "symbol": "♕ ♛",
        "name": "后 (Queen)",
        "value": "9",
        "desc": "后是棋盤上最強大的棋子，結合了車和象的功能。",
        "moves": "后可以向任何方向（橫、直、斜）移動**任意格數**，不能跳過其他棋子。",
        "special": "后通常在開局和中局後期發揮最大威力。",
        "example": "用后直接攻擊對方國王往往很有效。",
        "emoji": "👸"
    },
    {
        "type": chess.ROOK,
        "symbol": "♖ ♜",
        "name": "車 (Rook)",
        "value": "5",
        "desc": "車走直線，是強大的攻擊和防守棋子。",
        "moves": "車只能走橫向或縱向，任意格數，不能跳過其他棋子。",
        "special": "車在開放線（有空格的白話或黑格）上特別強大。",
        "example": "車進入第七排（對方底線）往往能造成巨大壓力。",
        "emoji": "🏰"
    },
    {
        "type": chess.BISHOP,
        "symbol": "♗ ♝",
        "name": "象 (Bishop)",
        "value": "3",
        "desc": "象走斜線，在長距離對角線攻擊中很強。",
        "moves": "象只能走斜向，任意格數，不能跳過其他棋子。每個象固定在一種顏色的格子上。",
        "special": "異色格象（不同顏色的兩隻象）比雙象更強，因為它們可以控制兩種顏色。",
        "example": "象適合攻擊對方王周围的弱點，特別是f7/f2 和 c7/c2 的原始兵形。",
        "emoji": "🏥"
    },
    {
        "type": chess.KNIGHT,
        "symbol": "♘ ♞",
        "name": "馬 (Knight)",
        "value": "3",
        "desc": "馬走獨特的L形，是唯一可以跳過其他棋子的棋子。",
        "moves": "馬走L形：先水平或垂直走兩格，再垂直或水平走一格（2+1=3格）。可以跳過其他棋子。",
        "special": "馬是近距離戰鬥專家，在棋盤中心時可以控制最多8個格子。",
        "example": "馬在中心可以同時威脅多個敵方棋子，讓對手難以防禦。",
        "emoji": "🐴"
    },
    {
        "type": chess.PAWN,
        "symbol": "♙ ♟",
        "name": "兵 (Pawn)",
        "value": "1",
        "desc": "兵是數量最多的棋子，也是西洋棋獨特魅力所在。",
        "moves": "兵只能向前走（白棋向上，黑棋向下），每步一格。**第一步**可以走兩格。",
        "special": """兵的吃法獨特：只能吃斜前方一格的敵方棋子（不能吃正前方）。
        
**兵的升變 (Promotion)**：兵走到對方底線時，可以升變為后、車、象、馬之一。

**吃過路兵 (En Passant)**：當對方兵第一步走兩格，且經過你的兵攻擊範圍時，可以立刻吃下對方的兵。""",
        "example": "連接兵（相鄰兩列並排的兵）可以互相保護，形成強大的兵鍊。",
        "emoji": "🎖️"
    },
]

# 選擇顯示哪個棋子
st.markdown("## 🎯 選擇要學習的棋子")

cols = st.columns(6)
selected_idx = 0

for i, piece in enumerate(PIECES):
    with cols[i]:
        emoji = piece["emoji"]
        if st.button(f"{emoji}\n{piece['name'].split()[0]}", use_container_width=True):
            selected_idx = i

piece = PIECES[selected_idx]

# 詳細說明
st.divider()
st.markdown(f"## {piece['emoji']} {piece['name']}")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"### 棋子的價值：{piece['value']}")
    st.markdown(f"**棋子符號：** {piece['symbol']}")
    st.markdown(f"**英文：** {piece['name'].split('(')[1].replace(')', '')}")
    st.markdown(f"**中文：** {piece['name'].split('(')[0].strip()}")

with col2:
    st.markdown(f"### 📝 描述")
    st.info(piece["desc"])

st.divider()

# 走法
st.markdown("### ♟️ 走法")
st.markdown(piece["moves"])

# 特殊能力
if piece.get("special"):
    st.markdown("### ⭐ 特殊能力")
    st.markdown(piece["special"])

# 實例
if piece.get("example"):
    st.markdown("### 💡 實戰建議")
    st.success(piece["example"])

# 棋盤視覺化
st.divider()
st.markdown("### �棋盤視覺化")

# 顯示棋盤格子的顏色說明
st.markdown("""
<style>
.tutorial-board {{
    display: grid;
    grid-template-columns: repeat(8, 50px);
    grid-template-rows: repeat(8, 50px);
    border: 2px solid #333;
    width: 400px;
}}
.t-cell {{
    width: 50px;
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 35px;
}}
.t-white {{ background-color: #f0d9b5; }}
.t-black {{ background-color: #b58863; }}
</style>
""", unsafe_allow_html=True)

html = '<div class="tutorial-board">'
for rank in range(7, -1, -1):
    for file in range(8):
        is_white = (rank + file) % 2 == 1
        html += f'<div class="t-cell t-{"white" if is_white else "black"}"></div>'
html += '</div>'
st.markdown(html, unsafe_allow_html=True)

# 基礎規則
st.divider()
st.markdown("## 📋 遊戲基本規則")

rules = [
    ("♔ 國王被將死", "保護你的國王！當國王被將軍（下一步會被吃）時，必須解除。"),
    ("🎯 將死 (Checkmate)", "國王被將軍且無法解除時，遊戲結束，攻擊方獲勝。"),
    ("🤝 僵局 (Stalemate)", "輪到走棋的一方沒有合法走法但未被將軍，判為和局。"),
    ("♟️ 兵的升變", "兵到達對方底線時，必須升變為后、車、象或馬。"),
    ("🔄 王車易位", "滿足條件時，國王和車可以一次交換位置。"),
    ("👻 吃過路兵", "特殊吃法，用兵的斜向吃子權利。"),
]

for title, desc in rules:
    st.markdown(f"**{title}**：{desc}")

# 練習提示
st.divider()
st.markdown("## 🎮 實踐練習")

st.markdown("""
現在去 **雙人對戰** 或 **對戰電腦** 模式實際演練吧！

1. 先用 **雙人對戰** 熟悉基本走法
2. 再用 **對戰電腦 - 新手難度** 練習思考
3. 嘗試使用 **兵的升變** 和 **王車易位**
""")

st.caption("💡 提示：按左側選單可以切換到其他模式")