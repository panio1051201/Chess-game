"""棋盤渲染組件"""
import streamlit as st
import chess


# Unicode 棋子字符
PIECE_SYMBOLS = {
    (chess.PAWN, True): "♙",
    (chess.PAWN, False): "♟",
    (chess.ROOK, True): "♖",
    (chess.ROOK, False): "♜",
    (chess.KNIGHT, True): "♘",
    (chess.KNIGHT, False): "♞",
    (chess.BISHOP, True): "♗",
    (chess.BISHOP, False): "♝",
    (chess.QUEEN, True): "♕",
    (chess.QUEEN, False): "♛",
    (chess.KING, True): "♔",
    (chess.KING, False): "♚",
}

# 棋子名稱（英文）
PIECE_NAMES = {
    chess.PAWN: "Pawn",
    chess.ROOK: "Rook",
    chess.KNIGHT: "Knight",
    chess.BISHOP: "Bishop",
    chess.QUEEN: "Queen",
    chess.KING: "King",
}

# 棋種中文字
PIECE_NAMES_CN = {
    chess.PAWN: "兵",
    chess.ROOK: "車",
    chess.KNIGHT: "馬",
    chess.BISHOP: "象",
    chess.QUEEN: "后",
    chess.KING: "王",
}


def render_board(board, key_prefix="board", size=560, 
                 selected_square=None, legal_squares=None,
                 last_move=None, check_square=None,
                 on_square_click=None):
    """
    渲染棋盤
    
    Args:
        board: chess.Board 物件
        key_prefix: Streamlit widget key 前綴
        size: 棋盤大小（像素）
        selected_square: 當前選中的格子
        legal_squares: 合法移動目標格子列表
        last_move: 最後一步走法
        check_square: 將軍的國王位置
        on_square_click: 回調函數，參數為點擊的格子索引
    """
    cell_size = size // 8
    
    # CSS
    st.markdown(f"""
    <style>
    .chess-board {{
        display: grid;
        grid-template-columns: repeat(8, {cell_size}px);
        grid-template-rows: repeat(8, {cell_size}px);
        border: 3px solid #333;
        width: {size}px;
    }}
    .chess-cell {{
        width: {cell_size}px;
        height: {cell_size}px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: {cell_size * 0.75}px;
        cursor: pointer;
        user-select: none;
        position: relative;
    }}
    .chess-cell.white {{
        background-color: #f0d9b5;
    }}
    .chess-cell.black {{
        background-color: #b58863;
    }}
    .chess-cell.selected {{
        background-color: #829769 !important;
    }}
    .chess-cell.legal-move {{
        position: relative;
    }}
    .chess-cell.legal-move::after {{
        content: "";
        position: absolute;
        width: {cell_size * 0.3}px;
        height: {cell_size * 0.3}px;
        background-color: rgba(0, 0, 0, 0.15);
        border-radius: 50%;
    }}
    .chess-cell.last-move {{
        background-color: #cdd26a !important;
    }}
    .chess-cell.check {{
        background-color: #e74c3c !important;
    }}
    .piece-white {{
        color: #fff;
        text-shadow: 0 0 2px #000, 0 0 2px #000;
    }}
    .piece-black {{
        color: #000;
    }}
    .coord {{
        position: absolute;
        font-size: 10px;
        font-weight: bold;
    }}
    .coord-file {{
        bottom: 1px;
        right: 3px;
    }}
    .coord-rank {{
        top: 1px;
        left: 3px;
    }}
    </style>
    """, unsafe_allow_html=True)
    
    # 建立格子 HTML
    html = '<div class="chess-board">'
    
    for rank in range(7, -1, -1):  # 第8 rank 到第1 rank
        for file in range(8):
            square = rank * 8 + file
            is_white = (rank + file) % 2 == 1
            
            # 取得棋子
            piece = board.piece_at(square)
            
            # 組合 class
            classes = ["chess-cell"]
            classes.append("white" if is_white else "black")
            
            if square == selected_square:
                classes.append("selected")
            elif square in (legal_squares or []):
                classes.append("legal-move")
            elif last_move and square in (last_move.from_square, last_move.to_square):
                classes.append("last-move")
            elif square == check_square:
                classes.append("check")
            
            # 棋子字符
            piece_html = ""
            if piece:
                symbol = PIECE_SYMBOLS.get((piece.piece_type, piece.color), "?")
                color_class = "piece-white" if piece.color else "piece-black"
                piece_html = f'<span class="{color_class}">{symbol}</span>'
            
            # 座標
            coord_html = ""
            if file == 0:  # 左側座標
                coord_html += f'<span class="coord coord-rank">{rank + 1}</span>'
            if rank == 0:  # 底部座標
                coord_html += f'<span class="coord coord-file">{chr(97 + file)}</span>'
            
            html += f'<div class="{" ".join(classes)}">{piece_html}{coord_html}</div>'
    
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)
    
    # 隱藏的點擊區域（用於互動）
    cols = st.columns(8)
    for file in range(8):
        with cols[file]:
            for rank in range(8):
                square = (7 - rank) * 8 + file
                if st.button("", key=f"{key_prefix}_{square}", help=f"{chr(97+file)}{rank+1}"):
                    if on_square_click:
                        on_square_click(square)


def render_captured_pieces(pieces: list, is_white: bool) -> str:
    """渲染被吃掉棋子"""
    if not pieces:
        return ""
    symbols = [PIECE_SYMBOLS.get((p.piece_type, p.color), "?") for p in pieces]
    return f'<span class="{"piece-white" if is_white else "piece-black"}">{"".join(symbols)}</span>'


def get_piece_info(piece_type: int) -> dict:
    """取得棋子資訊"""
    return {
        "name": PIECE_NAMES.get(piece_type, "Unknown"),
        "name_cn": PIECE_NAMES_CN.get(piece_type, "未知"),
        "symbol": PIECE_SYMBOLS.get((piece_type, True), "?"),
    }