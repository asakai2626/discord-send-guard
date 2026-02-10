# Discord Send Guard

Discordでメッセージを送信する際、Enterキーの誤送信を防止するツール。

## 概要

Discord Send Guardは、Discordがアクティブウィンドウのときだけ、キー操作を以下のように変更します:

- **Enterキー単体** → 改行（送信しない）
- **Cmd+Enter (Mac) / Ctrl+Enter (Windows)** → 送信

これにより、長文を書いている途中での誤送信を防止できます。

## 特徴

- Discord限定の動作（他のアプリには影響なし）
- クロスプラットフォーム対応（macOS、Windows）
- 軽量・バックグラウンド常駐
- CLI操作のみ（GUIなし）
- セキュアな設計（Discord以外のキー入力はキャプチャしない）

## 動作環境

- Python 3.7以上
- macOS 10.13以上 または Windows 10以上

## インストール

### 1. リポジトリのクローン

```bash
cd code/discord-send-guard
```

### 2. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### macOS固有の設定

macOSでは**アクセシビリティ権限**が必要です。

1. システム設定を開く
2. 「プライバシーとセキュリティ」→「アクセシビリティ」に移動
3. 実行するターミナルアプリ（ターミナル、iTerm2など）に権限を付与

### Windows固有の設定

Windowsでは管理者権限が必要な場合があります。必要に応じて管理者としてコマンドプロンプトやPowerShellを実行してください。

## 使用方法

### 基本的な使い方

```bash
python run.py
```

または

```bash
python discord_send_guard.py
```

### デバッグモード

```bash
python run.py --debug
```

デバッグモードでは、以下の情報がログに出力されます:

- アクティブなアプリケーション名
- 押されたキー（修飾キー、Enterキー）
- キーイベントの処理内容

### 停止方法

**Ctrl+C** で停止します。

## 動作確認

1. Discord Send Guardを起動
2. Discordを開く
3. メッセージ入力欄で以下を試す:
   - **Enterキー単体** → 改行される
   - **Cmd+Enter (Mac) / Ctrl+Enter (Windows)** → メッセージが送信される
4. 他のアプリ（ブラウザ、メモ帳など）を開く
5. Enterキーが通常通り動作することを確認

## テスト

ユニットテストを実行:

```bash
python -m pytest tests/ -v
```

または

```bash
cd tests
python test_discord_send_guard.py
```

## トラブルシューティング

### macOS: "Operation not permitted" エラー

アクセシビリティ権限が付与されていません。上記の「macOS固有の設定」を参照してください。

### macOS: "AppKit not available" エラー

以下をインストール:

```bash
pip install pyobjc-framework-Cocoa
```

### Windows: "win32gui not available" エラー

以下をインストール:

```bash
pip install pywin32
```

### Enterキーが反応しない

1. デバッグモードで起動: `python run.py --debug`
2. ログを確認し、Discordが正しく検出されているか確認
3. Discordのウィンドウ名に"discord"が含まれているか確認

### 他のアプリでもEnterキーの挙動が変わる

バグの可能性があります。以下の情報を添えてIssueを報告してください:

- OS名とバージョン
- 影響を受けるアプリケーション名
- デバッグログ

## 技術詳細

### アーキテクチャ

- **キーフック**: `pynput`ライブラリを使用
- **アクティブウィンドウ検出**:
  - macOS: `AppKit.NSWorkspace`
  - Windows: `win32gui`

### キーイベントの処理フロー

1. キー押下イベントをキャプチャ
2. 修飾キー（Cmd/Ctrl）の状態を記録
3. Enterキーが押された場合:
   - Discordがアクティブでない → 通常動作
   - Discordがアクティブ:
     - 修飾キーあり → 送信を許可
     - 修飾キーなし → Shift+Enterに変換（改行）

### セキュリティ考慮事項

- Discord以外のアプリでは、キー入力を監視するのみで改変しない
- キーロギングは行わない（ログにキー内容は記録しない）
- 最小権限の原則に基づき、必要な権限のみ要求

## ライセンス

MIT License

## 貢献

バグ報告、機能リクエスト、プルリクエストを歓迎します。

## 開発者

- PO: 浅野 海翔 (Asakai)
- PM: ideaccept-openclaw
- Dev: Claude Code

## バージョン履歴

### v1.0.0 (2026-02-11)

- 初回リリース
- macOS、Windows対応
- Enterキー/Cmd+Enter/Ctrl+Enterの挙動変更機能
- Discord検出機能
- CLI操作
- ユニットテスト

## 関連ドキュメント

- [要件定義書](../../docs/discord-send-guard/REQUIREMENTS.md)
