"""Stockfish AI 玩家"""
import chess
import subprocess
import os
import platform
from pathlib import Path


class AIPlayer:
    def __init__(self, skill_level: int = 10):
        """
        初始化 AI 玩家
        
        Args:
            skill_level: 難度等級 0-20
                         0-3: 新手（容易失誤）
                         4-10: 一般
                         11-20: 困難
        """
        self.skill_level = max(0, min(20, skill_level))
        self.stockfish_path = self._find_stockfish()
        self.enabled = self.stockfish_path is not None
    
    def _find_stockfish(self) -> str | None:
        """找到 Stockfish 執行檔"""
        # 1. 檢查專案內的 stockfish
        base_dir = Path(__file__).parent.parent
        local_sf = base_dir / "stockfish"
        if local_sf.exists():
            return str(local_sf)
        
        # 2. 檢查系統 PATH
        system = platform.system()
        if system == "Windows":
            for name in ["stockfish.exe", "stockfish-windows.exe", "stockfish-windows-x86-64.exe"]:
                try:
                    result = subprocess.run(["where", name], capture_output=True, text=True)
                    if result.returncode == 0:
                        return result.stdout.strip().split("\n")[0]
                except:
                    pass
        else:
            for name in ["stockfish", "stockfish-ubuntu-x86-64"]:
                try:
                    result = subprocess.run(["which", name], capture_output=True, text=True)
                    if result.returncode == 0:
                        return result.stdout.strip()
                except:
                    pass
        
        return None
    
    def get_best_move(self, board: chess.Board, depth: int = None) -> chess.Move | None:
        """取得最佳走法"""
        if not self.enabled:
            return None
        
        if depth is None:
            # 根據難度設定深度
            depth = max(1, min(20, self.skill_level // 2 + 1))
        
        try:
            # 啟動 Stockfish 進程
            process = subprocess.Popen(
                [self.stockfish_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            # 設定難度
            process.stdin.write(f"setoption name Skill Level value {self.skill_level}\n")
            process.stdin.write(f"position fen {board.fen()}\n")
            process.stdin.write(f"go depth {depth}\n")
            process.stdin.flush()
            
            # 讀取結果
            best_move = None
            for line in iter(process.stdout.readline, ""):
                if line.startswith("bestmove"):
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        best_move = chess.Move.from_uci(parts[1])
                    break
            
            process.terminate()
            return best_move
            
        except Exception as e:
            print(f"Stockfish error: {e}")
            return None
    
    def get_move_quality(self, board: chess.Board, move: chess.Move) -> str:
        """評估走法品質"""
        if not self.enabled:
            return "AI未啟用"
        
        try:
            process = subprocess.Popen(
                [self.stockfish_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            process.stdin.write(f"setoption name Skill Level value {self.skill_level}\n")
            process.stdin.write(f"position fen {board.fen()}\n")
            process.stdin.write(f"go depth 10\n")
            process.stdin.flush()
            
            eval_score = None
            for line in iter(process.stdout.readline, ""):
                if "score cp" in line:
                    parts = line.strip().split()
                    for i, p in enumerate(parts):
                        if p == "cp" and i + 1 < len(parts):
                            eval_score = int(parts[i + 1]) / 100.0
                            break
                elif line.startswith("bestmove"):
                    break
            
            process.terminate()
            
            if eval_score is not None:
                return f"{eval_score:+.2f}"
            return "?"
            
        except:
            return "?"