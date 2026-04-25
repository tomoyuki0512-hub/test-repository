---
title: Claude Codeでアプリ開発する方法
---

# Claude Codeでアプリ開発する方法

Claude CodeはCLIツールなので、**コマンドが動く環境であればほぼ何でも開発できる。**
ただしGUIを必要とする操作には制約がある。

---

## Claude Code全般でできること・できないこと

### ○ できること

| カテゴリ | 内容 |
|---|---|
| **プロジェクト生成** | CLI経由での雛形作成（`flutter create`、`rails new` 等） |
| **ファイル操作** | コード生成・編集・リファクタリング |
| **コマンド実行** | ビルド・テスト・サーバー起動・パッケージインストール |
| **デバッグ** | エラーメッセージの解析・修正 |
| **Git操作** | コミット・ブランチ・プッシュ |
| **設定ファイル** | 環境設定・CI/CD・Docker等 |
| **テスト作成** | ユニットテスト・統合テストの生成・実行 |

### ✗ できないこと

| カテゴリ | 内容 |
|---|---|
| **GUIの操作** | エミュレーター・シミュレーターの画面操作 |
| **ビジュアルプレビュー** | アプリ・UIの見た目の確認 |
| **ブラウザの操作** | 実際のブラウザでの動作確認 |
| **IDEのGUI機能** | Android Studio・Xcodeのデザイナー等 |
| **音声・カメラ等の実機確認** | デバイス依存の機能テスト |

> **補足：** ローカルサーバーを起動してブラウザで確認する作業は、Claude Codeがサーバーを立て、ユーザーがブラウザで確認するという分担で対応できる。

---

## フレームワーク別詳細

---

## Flutter（モバイル・Web・デスクトップ）

### 事前に必要なもの
- Flutter SDK（https://flutter.dev）
- Android Studio（Androidエミュレーター用）または Xcode（iOS用）
- VS Code（任意）

### 初期プロジェクト生成

```bash
# 新規プロジェクト作成
flutter create myapp

# テンプレート指定（アプリ種別）
flutter create --template=app myapp       # 通常アプリ
flutter create --template=plugin myapp   # プラグイン
flutter create --template=package myapp  # パッケージ

# 対象プラットフォームを指定
flutter create --platforms=android,ios,web myapp
```

### Claude Codeでできること

| 内容 | 詳細 |
|---|---|
| プロジェクト生成 | `flutter create` の実行 |
| Dartコード作成 | Widget・画面・ロジック・状態管理（Riverpod、BLoC等） |
| pubspec.yaml管理 | パッケージ追加・バージョン管理 |
| テスト実行 | `flutter test` |
| ビルド | `flutter build apk`、`flutter build web` 等 |
| 静的解析 | `flutter analyze`、`dart fix` |

### Claude Codeでできないこと

| 内容 | 理由・代替策 |
|---|---|
| エミュレーターの画面確認 | GUIのため不可。ユーザーが確認する必要あり |
| Hot Reload の視覚確認 | 同上 |
| Xcodeの証明書設定 | GUIのため不可 |

### 実際の開発フロー

```
Claude Codeがやる                    ユーザーがやる
─────────────────────────────────────────────────────
flutter create でプロジェクト生成
Dartコードを書く・修正する
flutter analyze でエラー確認
flutter test でテスト実行
                                     エミュレーターでUIを確認
                                     「このボタンが動かない」と伝える
エラーを修正する
```

---

## Spring Boot（Java / Kotlin・バックエンド）

### 事前に必要なもの
- JDK 17以上（https://adoptium.net）
- Maven または Gradle（Spring Initializrで自動生成される）

### 初期プロジェクト生成

**方法1：Spring Initializr（CLIで生成）**

```bash
# curlでzipを取得して展開
curl https://start.spring.io/starter.zip \
  -d type=maven-project \
  -d language=java \
  -d bootVersion=3.2.0 \
  -d groupId=com.example \
  -d artifactId=myapp \
  -d dependencies=web,data-jpa,h2 \
  -o myapp.zip
unzip myapp.zip -d myapp
```

**方法2：Spring Boot CLIがあれば**

```bash
spring init --dependencies=web,data-jpa myapp
```

### Claude Codeでできること

| 内容 | 詳細 |
|---|---|
| プロジェクト生成 | Initializr経由でのスキャフォールド |
| REST APIの実装 | Controller・Service・Repository層の作成 |
| DBの設定 | application.yml・JPA・Flyway等 |
| テスト作成・実行 | JUnit・Mockitoのテストコード生成と`./mvnw test` |
| ビルド・起動 | `./mvnw spring-boot:run` |
| Docker化 | Dockerfile・docker-compose.yml作成 |

### Claude Codeでできないこと

| 内容 | 代替策 |
|---|---|
| ブラウザでの動作確認 | `curl` や HTTPクライアント（httpie）でAPI確認は可能 |
| SwaggerUIの画面操作 | URLをユーザーがブラウザで開く |

> **ポイント：** Spring BootはバックエンドAPIがメインなので、Claude Codeとの相性は非常に良い。`curl`でAPIテストまで完結できる。

---

## Spring Framework（Spring Bootなし）

### Spring BootとSpring Frameworkの違い

| | Spring Boot | Spring Framework |
|---|---|---|
| 設定 | 自動設定（Convention over Configuration） | 手動設定が多い |
| 起動 | 組み込みTomcatで即起動 | 外部サーバー（Tomcat等）に別途デプロイ |
| 初心者向け | ○ | △（設定が複雑） |
| 現在の主流 | ○ | △（既存プロジェクトの保守が多い） |

**現在から新規開発するなら Spring Boot を選ぶのが一般的。**

Spring Framework単体での初期設定はXMLやJava Configを大量に書く必要があるが、Claude Codeは設定ファイルの生成・管理が得意なので対応可能。

---

## Ruby on Rails（Ruby・フルスタックWeb）

### 事前に必要なもの
- Ruby（rbenvやRVMで管理推奨）
- Bundler（`gem install bundler`）
- Node.js（アセットパイプライン用）
- データベース（SQLite・PostgreSQL・MySQL）

```bash
# Rubyのインストール確認
ruby -v

# Railsのインストール
gem install rails
```

### 初期プロジェクト生成

```bash
# 基本
rails new myapp

# DBを指定
rails new myapp --database=postgresql

# APIモード（フロントエンドと分離する場合）
rails new myapp --api

# テストフレームワーク指定
rails new myapp --skip-test --database=postgresql
```

### Claude Codeでできること

| 内容 | 詳細 |
|---|---|
| プロジェクト生成 | `rails new` の実行 |
| ジェネレーター | `rails generate model`・`controller`・`scaffold` |
| マイグレーション | `rails db:migrate`・スキーマ管理 |
| テスト | `rails test`・RSpec |
| サーバー起動 | `rails server`（ユーザーがブラウザで確認） |
| Gem管理 | Gemfile編集・`bundle install` |

### Claude Codeでできないこと

| 内容 | 代替策 |
|---|---|
| ブラウザでの画面確認 | `rails server` 後にユーザーがブラウザで確認 |
| Railsコンソールの対話操作 | スクリプトとして実行する形に変換 |

---

## React / Next.js（JavaScript・TypeScript・フロントエンド）

### 事前に必要なもの
- Node.js 18以上
- npm または yarn、pnpm

### 初期プロジェクト生成

```bash
# React（Vite使用・推奨）
npm create vite@latest myapp -- --template react-ts

# Next.js
npx create-next-app@latest myapp

# Next.jsオプション指定
npx create-next-app@latest myapp \
  --typescript \
  --tailwind \
  --eslint \
  --app   # App Router使用
```

### Claude Codeでできること

| 内容 | 詳細 |
|---|---|
| プロジェクト生成 | `create-vite`・`create-next-app` の実行 |
| コンポーネント作成 | JSX/TSXでのUI実装 |
| 状態管理 | useState・Zustand・Redux等 |
| APIルート | Next.jsのRoute Handlers |
| ビルド | `npm run build` |
| テスト | Jest・Vitest・React Testing Library |

> **ポイント：** フロントエンドはビジュアル確認がどうしても必要。`npm run dev` でサーバーを起動し、ユーザーがブラウザで確認しながらClaude Codeが修正するという流れが効果的。

---

## Django（Python・Webバックエンド）

### 事前に必要なもの
- Python 3.10以上
- pip・venv

### 初期プロジェクト生成

```bash
# 仮想環境の作成
python3 -m venv venv
source venv/bin/activate  # Windowsは venv\Scripts\activate

# Djangoインストール
pip install django

# プロジェクト生成
django-admin startproject myproject
cd myproject

# アプリ作成
python manage.py startapp myapp

# 開発サーバー起動
python manage.py runserver
```

### Claude Codeでできること

| 内容 | 詳細 |
|---|---|
| プロジェクト・アプリ生成 | `django-admin`・`startapp` |
| モデル・ビュー・URL設定 | MVTパターンの実装 |
| マイグレーション | `makemigrations`・`migrate` |
| Django管理画面 | models.pyの設定 |
| REST API | Django REST Framework |
| テスト | `python manage.py test` |

---

## FastAPI（Python・API開発）

### 事前に必要なもの
- Python 3.10以上
- pip・venv

### 初期プロジェクト生成

```bash
pip install fastapi uvicorn

# 雛形は自分で作る（CLIジェネレーターなし）
# Claude Codeが構成ごと生成してくれる
```

### Claude Codeでできること

FastAPIは設定ファイルよりコードで定義するスタイルのため、Claude Codeとの相性が非常に良い。

| 内容 | 詳細 |
|---|---|
| プロジェクト構成の生成 | ディレクトリ構造・`main.py`・`requirements.txt`一式 |
| エンドポイント実装 | Pydanticモデル・パスオペレーション |
| DB連携 | SQLAlchemy・Alembic |
| 認証 | JWT・OAuth2 |
| テスト | pytest・`TestClient` |
| 起動 | `uvicorn main:app --reload` |

> **ポイント：** `http://localhost:8000/docs` でSwagger UIが自動生成されるが画面確認はユーザーが行う。`curl` でのAPIテストはClaude Codeが実行できる。

---

## Express.js / Node.js（バックエンド）

### 事前に必要なもの
- Node.js 18以上

### 初期プロジェクト生成

```bash
# 基本（Claude Codeが一式生成）
mkdir myapp && cd myapp
npm init -y
npm install express

# TypeScript構成
npm install express typescript ts-node @types/express
npx tsc --init
```

### Claude Codeでできること

Node.jsはシンプルな構成のため、Claude Codeがゼロから一式生成しやすい。

| 内容 | 詳細 |
|---|---|
| プロジェクト一式の生成 | package.json・index.ts・ルーター構成 |
| REST API | ルーター・ミドルウェア・バリデーション |
| DB連携 | Prisma・Mongoose・Knex等 |
| 認証 | JWT・Passport.js |
| テスト | Jest・Supertest |
| 起動 | `node index.js`・`npx ts-node index.ts` |

---

## フレームワーク比較まとめ

| フレームワーク | 言語 | Claude Codeとの相性 | GUI確認の必要度 | 初心者向け |
|---|---|---|---|---|
| **Flutter** | Dart | ★★★★☆ | 高（UIアプリ） | △ |
| **Spring Boot** | Java/Kotlin | ★★★★★ | 低（API中心） | △ |
| **Spring** | Java/Kotlin | ★★★☆☆ | 低 | ✗ |
| **Ruby on Rails** | Ruby | ★★★★☆ | 中（Web画面あり） | ○ |
| **React/Next.js** | JS/TS | ★★★★☆ | 高（UIフレームワーク） | ○ |
| **Django** | Python | ★★★★★ | 低〜中 | ○ |
| **FastAPI** | Python | ★★★★★ | 低（API中心） | ○ |
| **Express.js** | JavaScript | ★★★★★ | 低（API中心） | ○ |

---

## 効果的な使い方のコツ

### 1. 「何を作りたいか」を最初に伝える

```
悪い例：「Flutterのコードを書いて」
良い例：「FlutterでログインとTODOリスト機能を持つアプリを作って。
         状態管理はRiverpodを使い、バックエンドはFirebaseを想定。」
```

### 2. GUIが必要な確認はユーザーが担当

```
Claude Codeがやる  → コードの生成・修正・テスト実行
ユーザーがやる    → ブラウザ・エミュレーターでの見た目確認
                    「このボタンの色がおかしい」など具体的にフィードバック
```

### 3. エラーはそのままコピペ

エラーメッセージをそのまま貼り付けると、Claude Codeが原因と修正方法を提示してくれる。

### 4. テストを先に書く（TDD）との相性が良い

Claude Codeはテストコードの生成が得意。テストを先に書いて、それをパスするコードを生成させると品質が上がりやすい。

---

## 何を作りたいか → フレームワーク逆引き表

| 作りたいもの | 推奨フレームワーク | 言語 | 難易度 |
|---|---|---|---|
| 飲食店・企業の紹介サイト | Rails / Next.js | Ruby / JS | ★★☆ |
| ブログ・ECサイト | Next.js | TypeScript | ★★☆ |
| スマホアプリ（iOS/Android両対応） | Flutter | Dart | ★★★ |
| データ処理・機械学習API | FastAPI | Python | ★★☆ |
| シンプルなREST API | Express.js | JavaScript | ★☆☆ |
| 管理画面付きWebサービス | Django | Python | ★★☆ |
| リアルタイム通信（チャット等） | NestJS + Socket.io | TypeScript | ★★★ |
| データ可視化ダッシュボード | Streamlit | Python | ★☆☆ |
| 個人ポートフォリオ | Next.js（静的生成） | TypeScript | ★☆☆ |

**初心者の最短コース：**
- バックエンド → **FastAPI**（自動ドキュメント生成・エラーが分かりやすい）
- フロントエンド → **Next.js**（ファイルを置くだけでルーティングが決まる）

---

## Claude Codeへの効果的な指示の出し方

### 悪い例・良い例の対比

| # | 悪い例 | 良い例 |
|---|---|---|
| 1 | `ログイン機能を作って` | `FastAPIでJWT認証のログインAPIを作って。POST /auth/login、リクエストは{email, password}、レスポンスは{access_token}の形式で` |
| 2 | `エラーが出て動かない` | エラー全文＋実行コマンド＋関連コードをそのまま貼る |
| 3 | `ボタンをいい感じにして` | `送信ボタンを背景色#3B82F6・白文字・角丸8px・ホバー時は少し暗くする・幅いっぱい（w-full）にして` |
| 4 | `ユーザー管理システムを全部作って` | `今回はまずユーザー一覧取得API（GET /users）だけ作って。ページネーション付きで` |
| 5 | `さっきのコードを修正して` | `routers/users.pyのget_users関数に、削除済み（is_deleted=True）を除外するフィルターを追加して。既存のページネーション処理は変えないで` |

### 要件定義テンプレート

新機能を依頼するときはこの形式で伝えると精度が上がる。

```
【目的】何を実現したいか
【技術スタック】バックエンド/フロントエンド/DB
【仕様】エンドポイント名・リクエスト・レスポンス形式
【制約】変えてほしくない部分・前提条件
【今回の範囲】ここだけ作ってほしいという絞り込み
```

### 段階的に積み上げる順番

```
Step1: DBモデル設計だけ作る
Step2: 基本CRUDのAPIを作る（バリデーションなし）
Step3: バリデーション・エラー処理を追加
Step4: 認証・権限チェックを追加
Step5: フロントエンドと接続
Step6: テストを書く
```

各ステップで動作確認してから次へ進む。

---

## よくある質問（FAQ）

### Q. どこまで任せられる？

| 任せられること | 人間がやること |
|---|---|
| コード生成・修正・リファクタリング | 要件・仕様の決定 |
| テストコード生成・実行 | ブラウザ・エミュレーターでの動作確認 |
| Dockerの設定・起動 | 本番環境へのデプロイ判断 |
| Git操作・CI/CD設定 | セキュリティ要件の最終確認 |

---

### Q. コードが長くなってきたら？

200〜300行を超えたらファイル分割を依頼する。

```
main.pyが400行を超えてきました。以下の基準で分割してください：
- DB接続関連 → database.py
- ユーザー関連エンドポイント → routers/users.py
- 共通スキーマ → schemas.py
```

---

### Q. セキュリティは大丈夫？

**貼り付けてはいけないもの：** 本番の `.env`・実際のAPIキー・個人情報が入った実データ

**確認を依頼できること：**
```
以下のコードのセキュリティ上の問題点を指摘してください。
特にSQLインジェクション・パスワードの扱い・認証の実装を確認してください。
```

---

### Q. 複数ファイルにまたがる修正は？

関連ファイルをまとめて貼り付けて依頼する。

```
以下の3ファイルを確認して、Userモデルにphone_numberフィールドを追加してください。
関連する箇所をすべて修正してください。

【models.py】（コードを貼り付け）
【schemas.py】（コードを貼り付け）
【routers/users.py】（コードを貼り付け）
```

---

## まとめ

```
Claude Codeで完結できること
    ├─ プロジェクトの雛形生成（全フレームワーク対応）
    ├─ コード生成・修正・リファクタリング
    ├─ ビルド・テスト・サーバー起動
    └─ Git操作・Docker設定

ユーザーとの分担が必要なこと
    ├─ ブラウザ・エミュレーターでのUI確認
    ├─ デバイス実機でのテスト
    └─ GUIを使う設定（Xcode証明書等）
```

**バックエンドAPI（Spring Boot・FastAPI・Express等）はClaude Codeだけでほぼ完結できる。**
**フロントエンド・モバイル（Flutter・React等）はビジュアル確認をユーザーが担当する分担が必要。**

---

## 関連ガイド

- [Docker・CI/CD・スタック選定の詳細](claude-code-dev-guide-advanced) — 実際のプロジェクト構成例・GitHub Actions・docker-compose
