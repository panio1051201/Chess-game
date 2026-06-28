"""遊戲狀態管理"""
import chess
from typing import Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class GameMode(Enum):
    PVP = "pvp"
    PVAI = "pvai"
    TUTORIAL = "tutorial"


class Difficulty(Enum):
    BEGINNER = ("新人", 3)
    NORMAL = ("一般", 10)
    HARD = ("困難", 18)
    
    def __init__(self, label: str, skill_level: int):
        self.label = label
        self.skill_level = skill_level


@dataclass
class GameState:
    board: chess.Board = field(default_factory=chess.Board)
    mode: GameMode = GameMode.PVP
    difficulty: Difficulty = Difficulty.NORMAL
    
    # 當前玩家（True = 白棋）
    current_player: bool = True
    
    # 選中狀態
    selected_square: Optional[int] = None
    legal_squares: list = field(default_factory=list)
    
    # 歷史
    move_history: list = field(default_factory=list)
    last_move: Optional[chess.Move] = None
    
    # 遊戲狀態
    game_over: bool = False
    result: Optional[str] = None
    
    # 玩家顏色（PvAI 模式）
    player_color: bool = True  # True = 白棋
    
    def reset(self):
        self.board = chess.Board()
        self.current_player = True
        self.selected_square = None
        self.legal_squares = []
        self.move_history = []
        self.last_move = None
        self.game_over = False
        self.result = None
    
    def select_square(self, square: int) -> bool:
        """選擇格子，返回是否選中了己方棋子"""
        piece = self.board.piece_at(square)
        
        # 如果選中的是己方棋子，切換選中狀態
        if piece and piece.color == self.current_player:
            self.selected_square = square
            self.legal_squares = [
                move.to_square for move in self.board.legal_moves
                if move.from_square == square
            ]
            return True
        
        # 如果已經選中，嘗試移動
        if self.selected_square is not None:
            return self.try_move(square)
        
        return False
    
    def try_move(self, to_square: int, promotion: int = None) -> bool:
        """嘗試移動"""
        if self.selected_square is None:
            return False
        
        move = chess.Move(self.selected_square, to_square, promotion=promotion)
        
        if move in self.board.legal_moves:
            self.board.push(move)
            self.move_history.append(move)
            self.last_move = move
            self.selected_square = None
            self.legal_squares = []
            self.current_player = not self.current_player
            
            # 檢查遊戲結束
            if self.board.is_checkmate():
                self.game_over = True
                winner = "白棋" if not self.current_player else "黑棋"
                self.result = f"{winner} 將死！"
            elif self.board.is_stalemate():
                self.game_over = True
                self.result = "僵局（和局）"
            elif self.board.is_insufficient_material():
                self.game_over = True
                self.result = "局面不足以取勝（和局）"
            
            return True
        
        # 無效走法，取消選中
        self.selected_square = None
        self.legal_squares = []
        return False
    
    def needs_promotion(self) -> bool:
        """是否需要兵的升變"""
        if self.selected_square is None:
            return False
        
        piece = self.board.piece_at(self.selected_square)
        if piece and piece.piece_type == chess.PAWN:
            to_square = self.selected_square
            # 兵的升變：白兵走到第8 rank，黑兵走到第1 rank
            if piece.color and chess.square_rank(to_square) == 6:
                return True
            if not piece.color and chess.square_rank(to_square) == 1:
                return True
        return False
    
    def get_check_square(self) -> Optional[int]:
        """取得將軍的國王位置"""
        if self.board.is_check():
            return self.board.king(self.board.turn)
        return None
    
    def get_all_legal_moves_for_current_player(self) -> list:
        """取得所有合法走法"""
        moves = []
        for move in self.board.legal_moves:
            if self.board.piece_at(move.from_square).color == self.current_player:
                moves.append(move)
        return moves