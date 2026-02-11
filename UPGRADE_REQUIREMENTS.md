# Discord Send Guard v2.0 - GUI App Upgrade Requirements

## 概要
現在のCLIツールを、macOS向けのGUIアプリケーションに大幅アップグレードする。

## 現状の問題
- ターミナルから毎回起動する必要がある → めんどくさい
- GUIがない → 分かりにくい
- 自動起動しない → 毎回手動
- 権限設定のガイドがない → ユーザーが迷う

## 要件

### 1. メニューバーアプリ化
- macOSメニューバーに常駐するアプリにする
- `rumps` ライブラリを使用（Python macOSメニューバーアプリ用）
- メニューバーアイコン（シールド/ガードのアイコン）
- メニュー項目：
  - ステータス表示（有効/無効）
  - 有効/無効の切り替え
  - 設定
  - ログ表示
  - 終了

### 2. GUIウィンドウ（設定・セットアップ）
- `tkinter` を使用（Python標準ライブラリ、追加インストール不要）
- 初回起動時にセットアップウィザードを表示
- セットアップウィザードの内容：
  1. Welcome画面（アプリの説明）
  2. アクセシビリティ権限の設定ガイド（ステップバイステップ、画像付き）
  3. 自動起動の設定確認
  4. 完了画面

### 3. アクセシビリティ権限チュートリアル（アプリ内GUI）
- 画像付きのステップバイステップガイド
- 各ステップ：
  1. 「システム設定を開く」ボタン（クリックで自動的にシステム設定を開く）
  2. 「プライバシーとセキュリティ → アクセシビリティ」への案内
  3. アプリを追加する手順
  4. 権限チェック機能（権限が付与されたか自動確認）
- ガイド画像は `assets/` フォルダに配置
- 画像はプレースホルダーとして簡易的に作成（テキスト付きの説明画像）

### 4. macOS起動時の自動スタート
- LaunchAgent plist を `~/Library/LaunchAgents/` に配置
- セットアップウィザードで有効/無効を選択可能
- 設定画面からも切り替え可能
- plist名: `com.ideaccept.discord-send-guard.plist`

### 5. py2appでの.appバンドル化
- `py2app` を使用してmacOS .appバンドルを作成
- ダブルクリックで起動可能
- setup.pyにpy2app設定を追加
- ビルドコマンド: `python setup.py py2app`

### 6. プロジェクト構造
```
discord-send-guard/
├── app.py                    # メインアプリ（メニューバー + GUI統合）
├── discord_send_guard.py     # コアロジック（既存、変更最小限）
├── gui/
│   ├── __init__.py
│   ├── setup_wizard.py       # 初回セットアップウィザード
│   ├── settings_window.py    # 設定画面
│   └── permission_guide.py   # 権限設定ガイド
├── utils/
│   ├── __init__.py
│   ├── autostart.py          # LaunchAgent管理
│   ├── permissions.py        # 権限チェック
│   └── config.py             # 設定ファイル管理（JSON）
├── assets/
│   ├── icon.png              # メニューバーアイコン
│   ├── app_icon.icns         # アプリアイコン
│   └── guide/                # ガイド用画像
│       ├── step1_system_settings.png
│       ├── step2_privacy.png
│       ├── step3_accessibility.png
│       └── step4_add_app.png
├── tests/
│   └── ...
├── setup.py                  # py2app対応
├── requirements.txt          # 依存関係更新
├── run.py                    # CLIエントリーポイント（後方互換）
├── README.md
└── UPGRADE_REQUIREMENTS.md
```

### 7. 設定ファイル
- `~/.discord-send-guard/config.json` に保存
- 設定項目：
  - `enabled`: bool（ガード有効/無効）
  - `autostart`: bool（自動起動）
  - `debug`: bool（デバッグモード）
  - `first_run`: bool（初回起動フラグ）

### 8. 依存関係
- `rumps` - macOSメニューバーアプリ
- `pynput` - キーボードフック（既存）
- `pyobjc-framework-Cocoa` - macOS API（既存）
- `Pillow` - 画像処理（ガイド画像生成用）
- `py2app` - .appバンドル化（ビルド時のみ）

## 制約
- **macOS優先**（Windowsは後回し）
- **Python + tkinter** でGUI（追加フレームワーク不要）
- ガイド画像はPillowでプログラム的に生成（スクリーンショットは使わない）
- 既存のコアロジック（discord_send_guard.py）は可能な限り維持

## 成果物
- 動作するGUIアプリ
- `python setup.py py2app` でビルド可能
- 全テストがパス
- README更新
