---
title: Claude Codeアプリ開発 応用編（Docker・CI/CD・スタック選定）
---

# Claude Codeアプリ開発ガイド補強

---

## セクション1：Docker / コンテナとの組み合わせ

Claude Codeは`docker-compose.yml`の生成・編集・`docker compose up`の実行まで自動化できる。コンテナの起動確認（ログ確認）もCLIで完結するため、相性は非常に良い。

### Spring Boot + PostgreSQL

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      SPRING_DATASOURCE_URL: jdbc:postgresql://db:5432/myapp
      SPRING_DATASOURCE_USERNAME: user
      SPRING_DATASOURCE_PASSWORD: password
    depends_on:
      - db

volumes:
  postgres_data:
```

> Claude Codeへの指示例：「Spring Boot + PostgreSQLのdocker-compose.ymlを作って、Dockerfileも含めて起動まで確認して」

---

### FastAPI + PostgreSQL

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:password@db:5432/myapp
    depends_on:
      - db
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    volumes:
      - .:/app

volumes:
  postgres_data:
```

> Claude Codeへの指示例：「FastAPI + PostgreSQLをDockerで動かして。AlembicでDBマイグレーションも実行できるようにして」

---

### Rails + PostgreSQL

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_DB: myapp_development
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: postgresql://user:password@db:5432/myapp_development
      RAILS_ENV: development
    depends_on:
      - db
    volumes:
      - .:/app
    command: bash -c "bundle exec rails db:migrate && bundle exec rails server -b 0.0.0.0"

volumes:
  postgres_data:
```

> Claude Codeへの指示例：「Railsアプリ全体をDockerに対応させて。`docker compose up`一発で起動できるようにして」

---

### Claude Codeがコンテナ周りで自動化できること

| 作業 | 可否 | コメント |
|---|---|---|
| Dockerfile・docker-compose.yml生成 | ○ | ゼロから生成可能 |
| `docker compose up` 実行・ログ確認 | ○ | CLIで完結 |
| DB初期化・マイグレーション実行 | ○ | コマンド経由で可能 |
| コンテナ内でのデバッグ（exec） | ○ | `docker compose exec`で対応 |
| コンテナUIの画面確認 | ✗ | ブラウザでのUI確認はユーザーが担当 |

---

## セクション2：CI/CD（GitHub Actions）

### Python（FastAPI）用

```yaml
# .github/workflows/ci.yml
name: FastAPI CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: testdb
          POSTGRES_USER: user
          POSTGRES_PASSWORD: password
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        env:
          DATABASE_URL: postgresql://user:password@localhost:5432/testdb
        run: pytest --cov=. --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v4
```

---

### Java（Spring Boot）用

```yaml
# .github/workflows/ci.yml
name: Spring Boot CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 21
        uses: actions/setup-java@v4
        with:
          java-version: "21"
          distribution: "temurin"
          cache: maven

      - name: Build and test
        run: ./mvnw verify

      - name: Upload test report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: target/surefire-reports/
```

---

### Node.js（Next.js）用

```yaml
# .github/workflows/ci.yml
name: Next.js CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"

      - name: Install dependencies
        run: npm ci

      - name: Lint
        run: npm run lint

      - name: Type check
        run: npx tsc --noEmit

      - name: Run tests
        run: npm test -- --coverage

      - name: Build
        run: npm run build
```

> **Claude Codeへの指示例（共通）：** 「このリポジトリにGitHub ActionsでCI/CDを設定して。pushとPRで自動テストが走るようにして」

---

## セクション3：実際のプロジェクト技術スタック例

### 1. 飲食店の予約・問い合わせサイト

**推奨スタック**

| 項目 | 選択肢 |
|---|---|
| フロントエンド | Next.js（App Router）+ Tailwind CSS |
| バックエンド | Next.js API Routes（フルスタック構成） |
| データベース | PostgreSQL（Supabase利用で簡略化可） |
| ホスティング | Vercel |
| メール送信 | Resend または SendGrid |

**Claude Codeへの最初の指示例**

```
Next.jsで飲食店の予約・問い合わせサイトを作って。
機能：予約フォーム（日時・人数・氏名・電話番号）、問い合わせフォーム、
     予約一覧を確認できる管理ページ（/admin）。
DBはPostgreSQL（Prisma経由）、フォーム送信時にメール通知（Resend）。
UIはTailwind CSSでシンプルに。
```

---

### 2. 習い事教室の生徒管理アプリ（スマホ）

**推奨スタック**

| 項目 | 選択肢 |
|---|---|
| フロントエンド | Flutter（iOS / Android対応） |
| バックエンド | FastAPI または Firebase |
| データベース | PostgreSQL または Firestore |
| 認証 | Firebase Auth |
| ホスティング | Fly.io（API）/ Firebase Hosting |

**Claude Codeへの最初の指示例**

```
Flutterで習い事教室の生徒管理アプリを作って。
機能：生徒一覧・登録・編集・削除、出欠管理（日付ごとに○×記録）、
     月謝の支払い状況管理。
状態管理はRiverpod、バックエンドはFastAPI + PostgreSQL（Docker）。
まずFlutterプロジェクト生成とFastAPIのプロジェクト構成から始めて。
```

---

### 3. 社内ダッシュボード（データ集計・グラフ表示）

**推奨スタック**

| 項目 | 選択肢 |
|---|---|
| フロントエンド | React（Vite + TypeScript）+ Recharts または Chart.js |
| バックエンド | FastAPI または Express.js |
| データベース | PostgreSQL |
| 認証 | 社内SSO または シンプルなJWT認証 |
| ホスティング | 社内サーバー または AWS/GCP |

**Claude Codeへの最初の指示例**

```
Reactで社内の売上データを表示するダッシュボードを作って。
機能：月次売上の折れ線グラフ、部門別売上の棒グラフ、KPI数値カード。
バックエンドはFastAPI + PostgreSQL。
グラフはRechartsを使って。認証はJWTでシンプルに。
Vite + TypeScriptでプロジェクトを生成して、まずAPIから作って。
```

---

### 4. 個人ポートフォリオ・ブログ

**推奨スタック**

| 項目 | 選択肢 |
|---|---|
| フレームワーク | Next.js（静的生成 / SSG） |
| コンテンツ管理 | Markdown（MDX）または Contentlayer |
| スタイリング | Tailwind CSS |
| ホスティング | Vercel（無料枠で可） |
| バックエンド | 不要（静的サイト） |

**Claude Codeへの最初の指示例**

```
Next.js + Tailwind CSSでエンジニアの個人ポートフォリオサイトを作って。
ページ：トップ（自己紹介・スキル一覧）、制作物一覧、ブログ一覧・詳細。
ブログはMarkdown（MDX）で管理。デザインはシンプルかつモダンに。
Vercelにデプロイできる構成で。`npx create-next-app`から始めて。
```

---

## セクション4：フロントエンドとバックエンドの組み合わせパターン

| フロントエンド | バックエンド | DB | 難易度 | 主な用途 |
|---|---|---|---|---|
| Next.js（フルスタック） | Next.js API Routes | PostgreSQL / SQLite | ★★☆☆☆ | Webサービス全般・SaaS |
| React（Vite） | FastAPI | PostgreSQL | ★★★☆☆ | 管理画面・ダッシュボード |
| React（Vite） | Express.js | MongoDB | ★★☆☆☆ | プロトタイプ・小規模API |
| React（Vite） | Spring Boot | PostgreSQL / MySQL | ★★★★☆ | 業務システム・企業向け |
| Flutter | FastAPI | PostgreSQL | ★★★☆☆ | モバイルアプリ（iOS/Android） |
| Flutter | Firebase | Firestore | ★★☆☆☆ | モバイルアプリ（リアルタイム） |
| Vue.js（Nuxt） | Laravel | MySQL | ★★★☆☆ | WebアプリのPHP構成 |
| Rails（フルスタック） | Rails（内蔵） | PostgreSQL | ★★☆☆☆ | 小〜中規模Webアプリ |
| 静的HTML / Next.js SSG | なし（静的） | なし | ★☆☆☆☆ | ポートフォリオ・ランディングページ |
| React Native | Node.js（Express） | PostgreSQL | ★★★★☆ | クロスプラットフォームモバイル |

> **難易度の基準：** ★☆☆☆☆＝入門、★★☆☆☆＝初級、★★★☆☆＝中級、★★★★☆＝上級、★★★★★＝エキスパート

> **選び方のポイント：**
> - 最速でリリースしたい → Next.js フルスタック（フロント・バック・DB一体で管理できる）
> - モバイルアプリ → Flutter + Firebase（認証・DBをFirebaseに任せると開発量が減る）
> - 業務システム → Spring Boot + PostgreSQL（堅牢・型安全）
> - 学習コストを下げたい → Rails または Next.js フルスタック

---

← [基本編に戻る](claude-code-dev-guide)
