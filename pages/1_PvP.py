"""雙人對戰模式"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from game.game_state import GameState
from game.board import render_board
import chess

st.set_page_config(page_title="雙人對戰 - 西洋棋", page_icon="♔")

# 初始化遊戲狀態
if "game_state" not in st.session_state:
    st.session_state.game_state = GameState(mode=st.session_state.game_state.mode if "game_state" in st.session_state else None)
    if "game_state" not in st.session_state:
        st.session_state.game_state = GameState()
        st.session_state.game_state.mode = st.session_state.game_state.mode

# 標題
st.markdown("# 👥 雙人對戰")
st.markdown(f"**當前回合：** {'⚪ 白棋' if st.session_state.game_state.current_player else '⚫ 黑棋'}")

# 重置按鈕
if st.button("🔄 重新開始"):
    st.session_state.game_state.reset()
    st.rerun()

# 狀態訊息
if st.session_state.game_state.game_over:
    st.success(st.session_state.game_state.result)
elif st.session_state.game_state.board.is_check():
    st.warning("⚠️ 將軍！")

# 棋盤
def on_square_click(square):
    state = st.session_state.game_state
    
    # 如果需要升變，彈出選擇
    if state.needs_promotion() and state.selected_square is not None:
        # 檢查是否點擊了升變格子
        piece = state.board.piece_at(state.selected_square)
        to_rank = chess.square_rank(square)
        if piece and piece.color and to_rank == 7:  # 白兵到第8格
            st.session_state.promotion_square = square
            st.session_state.show_promotion = True
            return
        elif piece and not piece.color and to_rank == 0:  # 黑兵到第1格
            st.session_state.promotion_square = square
            st.session_state.show_promotion = True
            return
    
    # 正常選子/移動
    if state.selected_square is None:
        # 選子
        piece = state.board.piece_at(square)
        if piece and piece.color == state.current_player:
            state.selected_square = square
            state.legal_squares = [
                m.to_square for m in state.board.legal_moves
                if m.from_square == square
            ]
    else:
        # 移動
        if square in state.legal_squares:
            state.try_move(square)
        else:
            # 選另一個棋子
            piece = state.board.piece_at(square)
            if piece and piece.color == state.current_player:
                state.selected_square = square
                state.legal_squares = [
                    m.to_square for m in state.board.legal_moves
                    if m.from_square == square
                ]
            else:
                state.selected_square = None
                state.legal_squares = []

render_board(
    st.session_state.game_state.board,
    key_prefix="pvp",
    size=min(560, st.session_state.get("board_size", 560)),
    selected_square=st.session_state.game_state.selected_square,
    legal_squares=st.session_state.game_state.legal_squares,
    last_move=st.session_state.game_state.last_move,
    check_square=st.session_state.game_state.get_check_square(),
    on_square_click=on_square_click
)

# 升變選擇
if st.session_state.get("show_promotion", False):
    st.markdown("### ♕ 兵的升變：選擇升級棋子")
    cols = st.columns(4)
    pieces = [(chess.QUEEN, "♕ 后"), (chess.ROOK, "♖ 車"), (chess.BISHOP, "♗ 象"), (chess.KNIGHT, "♘ 馬")]
    for i, (p_type, label) in enumerate(pieces):
        with cols[i]:
            if st.button(label, key=f"promo_{p_type}"):
                state = st.session_state.game_state
                state.try_move(st.session_state.promotion_square, promotion=p_type)
                st.session_state.show_promotion = False
                del st.session_state.promotion_square
                st.rerun()

# 走法歷史
if st.session_state.game_state.move_history:
    st.markdown("### 📜 走法記錄")
    moves = st.session_state.game_state.move_history
    cols = st.columns(min(10, len(moves)))
    for i, move in enumerate(moves[-10:]):
        with cols[i % 10]:
            move_num = (i // 10) * 10 + i + 1
            if i % 2 == 0:
                st.caption(f"{move_num}. {move.uci()[:2]}→{move.uci()[2:]}")
            else:
                st.caption(f"{move.uci()[:2]}→{move.uci()[2:]}")