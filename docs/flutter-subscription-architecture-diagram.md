# Flutterアプリ サブスクリプション システム構成図

## 構成概要

| 項目 | 選定 |
|---|---|
| クライアント | Flutter App（iOS / Android） |
| ロードバランサー | AWS ALB |
| APIサーバー | Java（EC2 / ECS） |
| DB | PostgreSQL（RDS） |
| キャッシュ | Redis（ElastiCache）※レート制限・通知UUID重複排除 |
| ストア通知（iOS） | Apple → ALB → Java API（直接HTTPS） |
| ストア通知（Android） | Google Play → **Google Cloud Pub/Sub** → Java API |

---

## 1. Mermaid 形式

```mermaid
graph LR

    subgraph CLIENT["クライアント"]
        Flutter["Flutter App\niOS / Android"]
    end

    subgraph APPLE_EXT["Apple"]
        Apple["App Store\nServer API"]
    end

    subgraph GCP["Google Cloud Platform"]
        GooglePlay["Google Play\nDeveloper API"]
        PubSubTopic["Pub/Sub\nトピック"]
        PubSubSub["Pub/Sub\nサブスクリプション\n（Push型）"]
    end

    subgraph AWS["AWS"]
        subgraph VPC["VPC"]
            subgraph PUBLIC["Public Subnet"]
                ALB["ALB\nロードバランサー"]
                JavaAPI["Java API\nサーバー"]
            end
            subgraph PRIVATE["Private Subnet"]
                RDS[("PostgreSQL\nRDS")]
                Redis[("Redis\nElastiCache")]
            end
        end
    end

    %% クライアント → API
    Flutter -->|"HTTPS"| ALB
    ALB -->|"HTTP"| JavaAPI

    %% API → 外部サービス（検証）
    JavaAPI -->|"レシート検証\nJWT認証"| Apple
    JavaAPI -->|"購入検証\nOAuth2"| GooglePlay

    %% API → DB / キャッシュ
    JavaAPI --- RDS
    JavaAPI --- Redis

    %% Apple Webhook（直接HTTPS）
    Apple -.->|"Webhook\nJWS署名"| ALB

    %% Google Play → Pub/Sub → API
    GooglePlay -.->|"通知発行"| PubSubTopic
    PubSubTopic -.-> PubSubSub
    PubSubSub -.->|"Push HTTPS"| ALB
```

---

## 2. Python Diagrams 形式

`diagrams` ライブラリ（`pip install diagrams`）で実行するとPNG画像を生成できます。

```python
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS, ElastiCache
from diagrams.aws.network import ALB
from diagrams.gcp.analytics import Pubsub
from diagrams.gcp.devtools import GCR  # Google Play の代替アイコン
from diagrams.generic.device import Mobile
from diagrams.generic.network import Firewall  # App Store Server API の代替

graph_attr = {
    "rankdir": "LR",
    "splines": "ortho",
}

with Diagram(
    "Flutter Subscription System",
    direction="LR",
    graph_attr=graph_attr,
    filename="flutter-subscription-architecture",
    show=False,
):
    flutter = Mobile("Flutter App\n(iOS/Android)")

    with Cluster("Apple"):
        apple = Firewall("App Store\nServer API")

    with Cluster("Google Cloud Platform"):
        google_play = GCR("Google Play\nDeveloper API")
        with Cluster("Pub/Sub"):
            pubsub_topic = Pubsub("トピック")
            pubsub_sub  = Pubsub("サブスクリプション\n(Push型)")

    with Cluster("AWS"):
        with Cluster("VPC"):
            with Cluster("Public Subnet"):
                alb = ALB("ALB")
                api = EC2("Java API\nサーバー")
            with Cluster("Private Subnet"):
                db    = RDS("PostgreSQL\n(RDS)")
                cache = ElastiCache("Redis\n(ElastiCache)")

    # クライアント → API
    flutter >> Edge(label="HTTPS") >> alb >> api

    # API → 外部サービス（検証）
    api >> Edge(label="レシート検証 (JWT)") >> apple
    api >> Edge(label="購入検証 (OAuth2)")  >> google_play

    # API → DB / キャッシュ
    api >> db
    api >> cache

    # Apple Webhook（直接 HTTPS）
    apple >> Edge(
        label="Webhook (JWS)",
        style="dashed",
        color="darkorange",
    ) >> alb

    # Google Play → Pub/Sub → API
    google_play >> Edge(style="dashed", color="royalblue") >> pubsub_topic
    pubsub_topic >> Edge(style="dashed", color="royalblue") >> pubsub_sub
    pubsub_sub >> Edge(
        label="Push HTTPS",
        style="dashed",
        color="royalblue",
    ) >> alb
```

### アイコン補足

| ノード | 使用クラス | 補足 |
|---|---|---|
| Flutter App | `generic.device.Mobile` | モバイル端末を表す汎用アイコン |
| App Store Server API | `generic.network.Firewall` | 外部APIの代替アイコン。`saas` 系に差し替え可 |
| Google Play Developer API | `gcp.devtools.GCR` | GCP系の代替アイコン |
| Pub/Sub トピック / サブスクリプション | `gcp.analytics.Pubsub` | GCP公式アイコン |
| ALB | `aws.network.ALB` | AWS公式アイコン |
| Java API サーバー | `aws.compute.EC2` | ECSを使う場合は `aws.compute.ECS` に変更 |
| PostgreSQL | `aws.database.RDS` | AWS公式アイコン |
| Redis | `aws.database.ElastiCache` | AWS公式アイコン |

---

## 3. データフローの凡例

| 線種 | 意味 |
|---|---|
| 実線 `───` | 通常のリクエスト／レスポンス |
| 破線 `- - -` | ストアからの非同期通知（Webhook / Pub/Sub Push） |
| オレンジ破線 | Apple Webhook（JWS署名付きHTTPS） |
| 青破線 | Android通知（Google Play → Pub/Sub → API）|
