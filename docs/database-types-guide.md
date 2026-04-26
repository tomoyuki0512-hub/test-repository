# データベースの種類まとめ

データベースは大きく「リレーショナル型」と「NoSQL型」に分類されます。それぞれの特徴と代表的な製品を解説します。

---

## 1. リレーショナルデータベース (RDB / RDBMS)

表（テーブル）形式でデータを管理し、SQL で操作する最も一般的なデータベースです。

| 特徴 | 内容 |
|------|------|
| データ形式 | 行と列からなるテーブル |
| クエリ言語 | SQL |
| 強み | トランザクション、整合性、結合クエリ |
| 弱み | 大量データのスケールアウトが難しい |

**代表的な製品**
- **MySQL** — Webアプリで最もよく使われるOSS
- **PostgreSQL** — 高機能・高拡張性のOSS
- **SQLite** — ファイル1つで動くシンプルなDB（組み込み用途に最適）
- **Oracle Database** — エンタープライズ向け商用DB
- **Microsoft SQL Server** — Windows環境でよく使われる商用DB

### インストール不要で使える組み込みRDB

SQLite のようにサーバーを別途インストールせず手軽に使える組み込みRDBが複数あります。

| DB | 主な言語 | 向いている用途 |
|----|---------|-------------|
| **SQLite** | Python / C / Ruby など幅広い | 汎用・軽量アプリ・モバイル |
| **DuckDB** | Python / R / Java など | データ分析・集計（列指向） |
| **H2** | Java | テスト・Spring Boot 開発 |
| **HSQLDB** | Java | テスト（レガシー系） |
| **Apache Derby** | Java | レガシー Java EE 環境 |

**DuckDB** は近年最も注目されている組み込みDB です。SQLite と同様にファイル1つで動きますが、分析・集計に特化した列指向のため大量データの SELECT が高速です。

```bash
pip install duckdb  # Python の場合これだけ
```

---

## Java 向け組み込みDB 詳細

### H2 Database（Java の定番）

Spring Boot がデフォルト対応しており、テスト環境では設定がほぼゼロです。

#### 動作モード

**組み込みモード（In-Memory）**

```
jdbc:h2:mem:mydb
```

- アプリと同じ JVM プロセス内で動く
- アプリ終了と同時にデータが消える
- Unit テスト向け（テストのたびにクリーンな状態から始められる）

**組み込みモード（ファイル）**

```
jdbc:h2:./data/mydb
```

- アプリと同じ JVM プロセス内で動く
- ファイルにデータが永続化される
- 接続できるのは1プロセスのみ（他のツールから同時接続できない）
- ローカル開発向け

**サーバーモード**

```
jdbc:h2:tcp://localhost:9092/~/mydb
```

- H2 が独立したプロセスとして起動
- 複数のアプリ・ツールから同時接続可能
- H2 Console（ブラウザUI）から中身を確認できる
- 「IntelliJ からも確認したい」場合に便利

| モード | データ永続化 | 同時接続 | 速度 | 向いている用途 |
|--------|------------|---------|------|-------------|
| In-Memory | なし | ✗ | 最速 | Unit テスト |
| ファイル組み込み | あり | ✗ | 速い | ローカル開発 |
| サーバー | あり | ◎ | 普通 | 複数ツールで確認したい |

---

### Apache Derby

Java で書かれた Apache Software Foundation 管理の組み込みRDB です。JDK 6〜7 時代に `Java DB` という名前で JDK に同梱されていましたが、JDK 8 以降は同梱されなくなりました。

H2 が登場してから Spring / Hibernate との連携が H2 の方が格段に楽になったため、**新規プロジェクトで Derby を選ぶ理由はほぼなく**、レガシーな Java EE プロジェクトや昔の教材で見かける程度です。

---

## ローカル開発・テスト・本番の DB 切り替え（Spring Boot）

本番では MySQL / PostgreSQL を使いながら、ローカル開発・テストでは H2 を使うのが一般的です。Spring Boot の **Profiles** で切り替えます。

### ファイル構成

```
src/main/resources/
├── application.properties          # 共通設定
├── application-local.properties    # ローカル開発（H2 ファイルモード）
├── application-test.properties     # テスト（H2 インメモリ）
└── application-prod.properties     # 本番（MySQL）
```

### application.properties（共通）

```properties
spring.jpa.hibernate.ddl-auto=update
```

### application-local.properties（ローカル開発）

```properties
spring.datasource.url=jdbc:h2:./data/mydb
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=

# ブラウザで DB を確認できるコンソールを有効化
spring.h2.console.enabled=true
spring.h2.console.path=/h2-console
```

### application-test.properties（統合テスト）

```properties
spring.datasource.url=jdbc:h2:mem:testdb;MODE=MySQL
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=

# テストのたびにスキーマを再作成
spring.jpa.hibernate.ddl-auto=create-drop
```

`MODE=MySQL` を付けると H2 が MySQL の方言を模倣するため、本番との差異が減ります。

### application-prod.properties（本番）

```properties
spring.datasource.url=jdbc:mysql://your-host:3306/mydb
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.username=${DB_USER}
spring.datasource.password=${DB_PASSWORD}

spring.jpa.hibernate.ddl-auto=validate
```

### プロファイルの切り替え方法

```bash
# ローカル開発
./mvnw spring-boot:run -Dspring-boot.run.profiles=local

# 本番
java -jar app.jar --spring.profiles.active=prod
```

```java
// テストクラスに直接指定
@SpringBootTest
@ActiveProfiles("test")
class UserServiceTest { ... }
```

```bash
# 環境変数で指定（CI/CD 向け）
export SPRING_PROFILES_ACTIVE=prod
```

---

## 本番 DB パスワードの外出し方法

`application-prod.properties` に直接パスワードを書くとコードに機密情報が残ります。以下の方法で外出しします。

### 方法1: OS 環境変数（最もシンプル）

```bash
# サーバーの環境変数に設定
export DB_USER=myuser
export DB_PASSWORD=mysecretpassword
```

```properties
# application-prod.properties
spring.datasource.username=${DB_USER}
spring.datasource.password=${DB_PASSWORD}
```

Spring Boot は起動時に `${変数名}` を OS 環境変数から自動的に読み込みます。

---

### 方法2: .env ファイル（ローカル開発向け）

```bash
# .env ファイル（.gitignore に必ず追加する）
DB_USER=myuser
DB_PASSWORD=mysecretpassword
```

```bash
# .gitignore
.env
```

Docker Compose や dotenv ライブラリと組み合わせて使います。**.env は絶対に git にコミットしない**のが鉄則です。

---

### 方法3: クラウドのシークレット管理サービス

本番環境では OS 環境変数よりもシークレット管理サービスが推奨されます。

| サービス | 概要 |
|---------|------|
| **AWS Secrets Manager** | AWS 環境での定番。ローテーションも自動化可能 |
| **AWS Parameter Store** | 単純な KV 管理なら Secrets Manager より安価 |
| **HashiCorp Vault** | クラウド非依存のOSS秘密管理ツール |
| **GCP Secret Manager** | GCP 環境での定番 |

Spring Boot + AWS Secrets Manager の例（`spring-cloud-aws` 使用）：

```properties
# application-prod.properties
spring.config.import=aws-secretsmanager:/myapp/prod/db
```

```json
// AWS Secrets Manager に登録する値（JSON形式）
{
  "spring.datasource.username": "myuser",
  "spring.datasource.password": "mysecretpassword"
}
```

---

### 方法4: Spring Boot の暗号化（Jasypt）

設定ファイルに暗号化済みの値を書き、復号キーだけを環境変数で渡す方法です。

```xml
<!-- pom.xml -->
<dependency>
    <groupId>com.github.ulisesbocchio</groupId>
    <artifactId>jasypt-spring-boot-starter</artifactId>
    <version>3.0.5</version>
</dependency>
```

```properties
# application-prod.properties（ENC(...) が暗号化済みの値）
spring.datasource.password=ENC(base64encryptedvalue...)
jasypt.encryptor.password=${JASYPT_PASSWORD}
```

```bash
# 復号キーだけを環境変数で渡す
export JASYPT_PASSWORD=myencryptionkey
```

---

### 外出し方法の選び方

| 状況 | 推奨方法 |
|------|---------|
| ローカル開発 | `.env` ファイル（.gitignore 必須） |
| CI/CD（GitHub Actions など） | リポジトリの Secrets 機能 → 環境変数として注入 |
| AWS 本番環境 | AWS Secrets Manager |
| GCP 本番環境 | GCP Secret Manager |
| クラウド非依存の本番環境 | HashiCorp Vault |

---

### よくある落とし穴

| 問題 | 原因 | 対処 |
|------|------|------|
| H2 では動くが MySQL でエラー | SQL 方言の差異 | `MODE=MySQL` を付ける |
| テスト間でデータが残る | `ddl-auto=update` のまま | テストは `create-drop` にする |
| パスワードが git に混入 | `.env` や `prod.properties` をコミット | `.gitignore` に追加・`git-secrets` を導入 |

---

## 2. NoSQL データベース

スキーマを柔軟にでき、水平スケールが得意なデータベースの総称です。用途に応じて4種類に分類されます。

### 2-1. ドキュメント型

JSON / BSON 形式のドキュメントをそのまま保存します。

| 特徴 | 内容 |
|------|------|
| データ形式 | JSON / BSON ドキュメント |
| 強み | スキーマレス、入れ子構造の表現が自然 |
| 向いている用途 | コンテンツ管理、カタログ、ユーザープロファイル |

**代表的な製品**
- **MongoDB** — 最も普及しているドキュメントDB
- **CouchDB** — HTTP API で操作できるOSS

---

### 2-2. キーバリュー型 (KVS)

キーと値のペアで高速にデータを読み書きします。

| 特徴 | 内容 |
|------|------|
| データ形式 | キー → 値 |
| 強み | 超高速な読み書き、シンプルな構造 |
| 向いている用途 | セッション管理、キャッシュ、リアルタイムランキング |

**代表的な製品**
- **Redis** — インメモリKVS。キャッシュや Pub/Sub にも使われる
- **Amazon DynamoDB** — AWSのフルマネージドKVS
- **Memcached** — シンプルな分散メモリキャッシュ

---

### 2-3. カラム型 (ワイドカラム型)

行ではなく列単位でデータを管理し、大量データへの集計クエリが高速です。

| 特徴 | 内容 |
|------|------|
| データ形式 | 列ファミリー（Column Family） |
| 強み | 大量データへの書き込み・集計が高速 |
| 向いている用途 | IoT、ログ分析、大規模SNS |

**代表的な製品**
- **Apache Cassandra** — 分散型・高可用性のOSS
- **Apache HBase** — Hadoop 上で動作する分散カラム型DB

---

### 2-4. グラフ型

ノード（頂点）とエッジ（辺）でデータの関係性を表現します。

| 特徴 | 内容 |
|------|------|
| データ形式 | ノード + エッジ + プロパティ |
| 強み | 複雑な関連性の探索が高速 |
| 向いている用途 | SNSのフォロー関係、レコメンド、不正検知 |

**代表的な製品**
- **Neo4j** — 最も普及しているグラフDB
- **Amazon Neptune** — AWSのフルマネージドグラフDB

---

## 3. 時系列データベース (TSDB)

タイムスタンプ付きのデータを効率的に保存・検索するために特化したデータベースです。

| 特徴 | 内容 |
|------|------|
| データ形式 | 時刻 + 指標値 |
| 強み | 時刻範囲での集計・ダウンサンプリングが高速 |
| 向いている用途 | サーバー監視、IoTセンサー、金融データ |

**代表的な製品**
- **InfluxDB** — 最もよく使われる時系列DB
- **TimescaleDB** — PostgreSQL 拡張の時系列DB
- **Prometheus** — Kubernetes 監視でよく使われるOSS

---

## 4. 全文検索エンジン

大量のテキストデータに対して高速な全文検索を提供します。

| 特徴 | 内容 |
|------|------|
| データ形式 | テキスト（転置インデックス） |
| 強み | キーワード検索、ランキング、ファセット検索 |
| 向いている用途 | サイト内検索、ログ検索、ECサイト |

**代表的な製品**
- **Elasticsearch** — 分散型の全文検索エンジン（ELKスタックの中心）
- **Apache Solr** — Lucene ベースのOSS検索エンジン
- **OpenSearch** — AWSが主導するElasticsearchのフォーク

---

## 5. NewSQL

RDB の ACID トランザクションを保ちながら、NoSQL のような水平スケールを実現します。

| 特徴 | 内容 |
|------|------|
| データ形式 | テーブル（SQL互換） |
| 強み | スケールアウト + トランザクション整合性 |
| 向いている用途 | グローバルサービス、金融系大規模システム |

**代表的な製品**
- **Google Spanner** — Google のグローバル分散RDB
- **CockroachDB** — OSSのNewSQL DB
- **TiDB** — MySQL 互換の分散DB

---

## 種類ごとの選び方まとめ

| やりたいこと | 向いている種類 |
|------------|-------------|
| 複雑な集計・結合クエリ | リレーショナル (RDB) |
| JSONをそのまま保存したい | ドキュメント型 |
| セッションやキャッシュを高速に扱いたい | キーバリュー型 |
| 時系列データ（センサー・監視）を扱いたい | 時系列DB |
| SNSやレコメンドなど関係性を扱いたい | グラフ型 |
| ログや大量データを分析したい | カラム型 / 全文検索エンジン |
| 大規模かつトランザクションが必要 | NewSQL |
