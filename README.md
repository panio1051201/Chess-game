# ♔ 西洋棋遊戲 (Western Chess)

一個完整的西洋棋遊戲，使用 Python + Streamlit + Stockfish 開發，可直接在瀏覽器中遊玩。

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🎮 功能特色

| 功能 | 說明 |
|------|------|
| 👥 **雙人對戰** | 與朋友面對面對弈，共享螢幕 |
| 🤖 **對戰電腦** | 單人挑戰 AI，三種難度可選 |
| 📚 **新手教學** | 學習各棋種走法與規則 |
| ♟️ **完整棋規** | 合法走法、將軍、將死、升變、王車易位 |
| 🖥️ **跨平台** | 可部署到 Render.com 雲端 |

## 🕹️ 三種難度

| 難度 | 等級 | 說明 |
|------|------|------|
| 新人 | Level 3 | AI 會犯錯，適合初學者 |
| 一般 | Level 10 | 平衡挑戰 |
| 困難 | Level 18 | 需要認真思考 |

## 🚀 快速開始

### 本地運行

```bash
# 1. 克隆專案
git clone https://github.com/YOUR_USERNAME/chess-game.git
cd chess-game

# 2. 安裝依賴
pip install -r requirements.txt

# 3. 下載 Stockfish（可選，需要 AI 對戰）
# Windows:
# 從 https://stockfishchess.org/download/ 下載並放到專案根目錄
# Linux/Mac:
# sudo apt-get install stockfish  # 或 brew install stockfish

# 4. 啟動
streamlit run app.py
```

### 部署到 Render.com

1. Fork 此專案到你的 GitHub
2. 到 [Render.com](https://render.com) 創建 Web Service
3. 連接你的 GitHub 專案
4. 設定：
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port $PORT`
5. 點擊 Deploy

## 📁 專案結構

```
chess_game/
├── app.py                  # 主頁面
├── requirements.txt        # 依賴
├── README.md               # 本文件
├── game/
│   ├── __init__.py
│   ├── board.py            # 棋盤渲染
│   ├── chess_logic.py      # 棋盤邏輯
│   ├── ai_player.py        # Stockfish AI
│   └── game_state.py       # 遊戲狀態
├── pages/
│   ├── 1_PvP.py            # 雙人對戰
│   ├── 2_PvAI.py           # 對戰電腦
│   └── 3_Tutorial.py       # 新手教學
└── .streamlit/
    └── config.toml         # Streamlit 設定
```

## ♟️ 棋子價值

| 棋子 | 符號 | 價值 |
|------|------|------|
| 兵 | ♙ ♟ | 1 |
| 馬 | ♘ ♞ | 3 |
| 象 | ♗ ♝ | 3 |
| 車 | ♖ ♜ | 5 |
| 后 | ♕ ♛ | 9 |
| 王 | ♔ ♚ | ∞ |

## 🎯 特殊規則

- **兵的升變**：兵走到對方底線時，可升變為后/車/象/馬
- **王車易位**：滿足條件時，國王和車可一次交換位置
- **吃過路兵**：特殊吃法，針對第一步走兩格的兵

## 🛠️ 技術棧

- **Python 3.9+** - 程式語言
- **Streamlit** - 網頁 UI 框架
- **python-chess** - 棋盤邏輯
- **Stockfish** - AI 棋引擎

## 📝 License

MIT License - 自由使用、修改、發布。

---

Made with ♡ by 茶叔