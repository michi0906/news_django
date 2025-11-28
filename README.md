# 📰 MyNewsApp

## 🧰 概要 (Overview)

MyNewsApp は、ニュース一覧を表示し、AI を使って「大喜利お題」を自動生成する Web アプリケーションです。  
ユーザーはログインして、気になるニュースカテゴリを選び、お題生成ボタンを押すだけで、お題の候補が得られます。  
主目的は、**ニュースを起点に「思考・遊び」を誘発する体験**を提供することです。  

---

## 🚀 主な機能 (Features)

- ニュース記事の一覧表示（カテゴリ別）  
- AI による「大喜利お題」の自動生成（ニュースタイトルを元にしたお題）  
- ユーザー認証／ログイン機能（ログインしないとお題生成できないよう制限）  
- シンプルで分かりやすい UI、ローカル環境でも起動可能  

---

## 🛠️ 開発環境とセットアップ (Setup / Installation)

### 前提条件 (Prerequisites)

- Python 3.10 以上  
- 仮想環境 (venv) を使うことを推奨  
- (オプション) API キーや機密情報は `.env` に設定  

### セットアップ手順 (Installation)

```bash
# リポジトリをクローン
git clone https://github.com/ユーザー名/リポジトリ名.git
cd リポジトリ名

# 仮想環境の作成と有効化
python -m venv .venv
# Windows（PowerShell）の場合
.\.venv\Scripts\Activate.ps1
# macOS / Linux の場合
source .venv/bin/activate

# 必要なパッケージのインストール
pip install -r requirements.txt

# (必要なら) .env ファイルをルートに作成し、API キーなどを設定

# データベースのマイグレーション
python manage.py migrate

# 開発用サーバー起動
python manage.py runserver
