"""對戰電腦模式"""
import streamlit as st
import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from game.game_state import GameState, Difficulty
from game.board import render_board
from game.ai_player import AIPlayer
import chess

st.set_page_config(page_title="對戰電腦 - 西洋棋", page_icon="♔")

# 初始化
if "ai_game_state" not in st.session_state:
    st.session_state.ai_game_state = GameState()
    st.session_state.ai_game_state.mode = st.session_state.ai_game_state.mode

# 側邊欄設定
with st.sidebar:
    st.markdown("## ⚙️ 遊戲設定")
    
    # 難度選擇
    diff = st.selectbox(
        "難度",
        [Difficulty.BEGINNER, Difficulty.NORMAL, Difficulty.HARD],
        format_func=lambda x: f"{x.label} (Level {x.skill_level})",
        index=1
    )
    
    # 玩家顏色
    player_white = st.radio("你扮演", ["⚪ 白棋", "⚫ 黑棋"], index=0) == "⚪ 白棋"
    
    if st.button("🔄 重新開始"):
        st.session_state.ai_game_state.reset()
        st.session_state.ai_player = AIPlayer(diff.skill_level)
        st.rerun()
    
    st.divider()
    st.markdown("""
    ### 💡 難度說明
    - **新人**：AI 會犯錯，適合初學者
    - **一般**：平衡挑戰
    - **困難**：需要認真思考
    """)

# 初始化 AI
if "ai_player" not in st.session_state:
    st.session_state.ai_player = AIPlayer(diff.skill_level)

# 同步難度
st.session_state.ai_game_state.difficulty = diff
st.session_state.ai_game_state.player_color = player_white

state = st.session_state.ai_game_state

# 標題
st.markdown("# 🤖 對戰電腦")
st.markdown(f"**難度：** {diff.label} | **你：** {'⚪ 白棋' if player_white else '⚫ 黑棋'}")

# 狀態
if state.game_over:
    st.success(state.result)
elif state.board.is_check():
    st.warning("⚠️ 將軍！")

# 判斷是否輪到 AI
ai_turn = (state.current_player == False) if player_white else (state.current_player == True)
waiting_for_ai = ai_turn and not state.game_over

# 棋盤點擊處理
def on_square_click(square):
    if waiting_for_ai:
        return  # AI 回合時不處理點擊
    
    s = st.session_state.ai_game_state
    
    # 升變
    if s.needs_promotion() and s.selected_square is not None:
        piece = s.board.piece_at(s.selected_square)
        to_rank = chess.square_rank(square)
        if piece and piece.color and to_rank == 7:
            st.session_state.promotion_square = square
            st.session_state.show_promotion = True
            return
        elif piece and not piece.color and to_rank == 0:
            st.session_state.promotion_square = square
            st.session_state.show_promotion = True
            return
    
    # 選子/移動
    if s.selected_square is None:
        piece = s.board.piece_at(square)
        if piece and piece.color == s.current_player:
            s.selected_square = square
            s.legal_squares = [m.to_square for m in s.board.legal_moves if m.from_square == square]
    else:
        if square in s.legal_squares:
            s.try_move(square)
            st.rerun()
        else:
            piece = s.board.piece_at(square)
            if piece and piece.color == s.current_player:
                s.selected_square = square
                s.legal_squares = [m.to_square for m in s.board.legal_moves if m.from_square == square]
            else:
                s.selected_square = None
                s.legal_squares = []

# 渲染棋盤
render_board(
    state.board,
    key_prefix="ai",
    size=min(560, st.session_state.get("board_size", 560)),
    selected_square=state.selected_square,
    legal_squares=state.legal_squares,
    last_move=state.last_move,
    check_square=state.get_check_square(),
    on_square_click=on_square_click if not waiting_for_ai else lambda x: None
)

# AI 回合
if waiting_for_ai:
    with st.spinner("🤖 AI 思考中..."):
        ai_move = st.session_state.ai_player.get_best_move(state.board)
        if ai_move:
            state.board.push(ai_move)
            state.move_history.append(ai_move)
            state.last_move = ai_move
            state.current_player = not state.current_player
            
            if state.board.is_checkmate():
                state.game_over = True
                state.result = "🤖 AI 將死！你輸了。"
            elif state.board.is_stalemate():
                state.game_over = True
                state.result = "僵局（和局）"
            
            st.rerun()

# 升變選擇
if st.session_state.get("show_promotion", False):
    st.markdown("### ♕ 兵的升變：選擇升級棋子")
    cols = st.columns(4)
    pieces = [(chess.QUEEN, "♕ 后"), (chess.ROOK, "♖ 車"), (chess.BISHOP, "♗ 象"), (chess.KNIGHT, "♘ 馬")]
    for i, (p_type, label) in enumerate(pieces):
        with cols[i]:
            if st.button(label, key=f"ai_promo_{p_type}"):
                state.try_move(st.session_state.promotion_square, promotion=p_type)
                st.session_state.show_promotion = False
                del st.session_state.promotion_square
                st.rerun()

# 資訊
if state.game_over:
    st.info("按左側「重新開始」再來一局！")

st.caption(f"Stockfish AI 等級：{diff.skill_level}")