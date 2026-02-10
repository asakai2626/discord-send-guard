# Discord Send Guard

Discordでの誤送信を防止するツール。Enterキーの挙動を変更し、うっかり送信を防ぎます。

## どう変わる？

| キー操作 | 変更前 | 変更後 |
|---------|--------|--------|
| Enter | メッセージ送信 | **改行**（送信しない） |
| Cmd+Enter (Mac) / Ctrl+Enter (Win) | 改行 | **メッセージ送信** |

> ⚠️ Discord がアクティブウィンドウのときだけ動作します。他のアプリには一切影響しません。

---

## ダウンロード＆インストール

### 必要なもの

- **Python 3.7以上**（[python.org](https://www.python.org/downloads/) からインストール）
- **Git**（[git-scm.com](https://git-scm.com/) からインストール）
- **macOS 10.13+** または **Windows 10+**

### Step 1: リポジトリをダウンロード

ターミナル（Mac）またはコマンドプロンプト（Windows）を開いて：

```bash
git clone https://github.com/asakai2626/discord-send-guard.git
cd discord-send-guard
```

> 💡 Gitがない場合は [GitHub のページ](https://github.com/asakai2626/discord-send-guard) から「Code → Download ZIP」でもOK

### Step 2: 仮想環境を作成（推奨）

```bash
# Mac / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: 依存関係をインストール

```bash
pip install -r requirements.txt
```

### Step 4: macOS のみ — アクセシビリティ権限の設定

macOSではキーボード操作に**アクセシビリティ権限**が必要です。

1. **システム設定** を開く
2. **プライバシーとセキュリティ** → **アクセシビリティ** を選択
3. 左下の鍵アイコンをクリックしてロック解除
4. **＋ボタン** で使用するターミナルアプリを追加：
   - 標準ターミナル: `/Applications/Utilities/Terminal.app`
   - iTerm2: `/Applications/iTerm.app`
   - VS Code のターミナル: `/Applications/Visual Studio Code.app`
5. チェックを入れて有効化

> ⚠️ 権限を追加した後、ターミナルを**再起動**してください。

---

## 使い方

### 起動

```bash
python run.py
```

起動すると以下のメッセージが表示されます：

```
Discord Send Guard v1.0.0
Discord Send Guard is running...
Press Ctrl+C to stop
```

### 動作確認

1. Discordを開いてメッセージ入力欄にカーソルを置く
2. **Enter** を押す → 改行される（送信されない！）
3. **Cmd+Enter** (Mac) / **Ctrl+Enter** (Win) を押す → メッセージが送信される
4. 他のアプリ（ブラウザなど）に切り替えてEnterを押す → 通常通り動作

### デバッグモード

問題があるときはデバッグモードで起動：

```bash
python run.py --debug
```

キー入力やウィンドウ検出のログがリアルタイムで表示されます。

### 停止

**Ctrl+C** で停止します。

---

## トラブルシューティング

### 「Operation not permitted」エラー（Mac）

→ アクセシビリティ権限が未設定です。上の「Step 4」を確認してください。

### 「AppKit not available」エラー（Mac）

```bash
pip install pyobjc-framework-Cocoa
```

### 「win32gui not available」エラー（Windows）

```bash
pip install pywin32
```

### Enterを押しても何も起きない

1. デバッグモードで起動: `python run.py --debug`
2. Discordがアクティブウィンドウとして検出されているかログを確認
3. ターミナルのアクセシビリティ権限を再確認

---

## テスト

```bash
python -m pytest tests/ -v
```

14件のテストが全てパスすればOKです。

---

## 技術仕様

- **キーフック**: `pynput` ライブラリ
- **ウィンドウ検出**: `AppKit.NSWorkspace`（Mac） / `win32gui`（Windows）
- **動作原理**: Enter単体 → ブロック＆Shift+Enter送信（改行）、修飾キー+Enter → パススルー（送信）
- **セキュリティ**: キーロギングなし。Discord以外のキー入力は改変しない

---

## ライセンス

MIT License

## 開発チーム

- **PO**: 浅野 海翔 (Asakai)
- **PM**: ideaccept-openclaw
- **Dev**: Claude Code
