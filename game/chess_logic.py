"""西洋棋邏輯封裝 - 使用 python-chess"""
import chess
import streamlit as st
from typing import Optional, List, Tuple


class ChessLogic:
    def __init__(self):
        self.board = chess.Board()
    
    def reset(self):
        self.board = chess.Board()
    
    def get_legal_moves(self, square: Optional[int] = None) -> List[int]:
        """取得合法走法"""
        if square is not None:
            return [move.to_square for move in self.board.legal_moves 
                    if move.from_square == square]
        return [move.to_square for move in self.board.legal_moves]
    
    def make_move(self, from_sq: int, to_sq: int, promotion: Optional[int] = None) -> bool:
        """執行走法，成功返回 True"""
        move = chess.Move(from_sq, to_sq, promotion=promotion)
        if move in self.board.legal_moves:
            self.board.push(move)
            return True
        return False
    
    def is_check(self) -> bool:
        return self.board.is_check()
    
    def is_checkmate(self) -> bool:
        return self.board.is_checkmate()
    
    def is_stalemate(self) -> bool:
        return self.board.is_stalemate()
    
    def is_game_over(self) -> bool:
        return self.board.is_game_over()
    
    def get_turn(self) -> bool:
        """True = 白棋，False = 黑棋"""
        return self.board.turn
    
    def get_piece_at(self, square: int) -> Optional[chess.Piece]:
        return self.board.piece_at(square)
    
    def get_fen(self) -> str:
        return self.board.fen()
    
    def get_board_array(self) -> List[List[Tuple[int, Optional[chess.Piece]]]]:
        """取得 8x8 棋盤二維陣列"""
        board_array = []
        for rank in range(7, -1, -1):  # 從第8 rank 到第1 rank
            row = []
            for file in range(8):  # a-h
                square = rank * 8 + file
                piece = self.board.piece_at(square)
                row.append((square, piece))
            board_array.append(row)
        return board_array
    
    def get_king_square(self, white: bool) -> int:
        """取得國王位置"""
        return self.board.king(white)
    
    def is_square_attacked(self, square: int, by_white: bool) -> bool:
        return self.board.is_attacked_by(square, by_white)
    
    def get_captured_pieces(self) -> Tuple[List[chess.Piece], List[chess.Piece]]:
        """取得雙方被吃掉棋子"""
        white_captured = []
        black_captured = []
        for square in range(64):
            # 檢查雙方吃掉的棋子
            pass
        return white_captured, black_captured