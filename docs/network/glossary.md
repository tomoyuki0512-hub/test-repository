---
title: 用語集・チートシート（ネットワーク）
---

# 用語集・チートシート（ネットワーク）

> 全章横断の用語辞典と、「困った時どの章？」の逆引き表・コマンド集・計算早見表をまとめています。

← [総合インデックスに戻る](README.md)

---

## 1. 「困った時どの章？」逆引き表

| やりたいこと・困っていること | 参照先 |
| --- | --- |
| そもそもネットワークの仕組みを知りたい | [① 基礎とOSI参照モデル](01-network-basics.md) |
| LANケーブルのカテゴリを選びたい | [② 1-1節](02-physical-datalink.md) |
| Wi-Fi APに給電したい／APが再起動を繰り返す | [② 1-4節 PoE](02-physical-datalink.md) |
| VLANを切りたい | [② 3節](02-physical-datalink.md) |
| **ネットワーク全体が突然止まった** | [② 4節 ループとSTP](02-physical-datalink.md)・[⑪ 2節](11-operations.md) |
| サブネットの計算をしたい | [③ 2節](03-ip-subnet.md) |
| **IPアドレス設計をゼロから引きたい** | [③ 3節](03-ip-subnet.md) |
| DHCPでIPが取れない | [③ 4節](03-ip-subnet.md) |
| IPv6を導入したい | [③ 7節](03-ip-subnet.md) |
| 経路が思った通りにならない | [④ 1節 経路表の読み方](04-routing.md) |
| OSPFの隣接が張れない | [④ 4-4節](04-routing.md) |
| クラウド専用線を引きたい（BGPが必要と言われた） | [④ 5節](04-routing.md)・[⑧ 6節](08-cloud-network.md) |
| ゲートウェイを冗長化したい | [④ 9節 VRRP/HSRP](04-routing.md) |
| ポート番号を調べたい | [⑤ 1-2節](05-transport-application.md) |
| **「遠い拠点とのファイル転送が遅い」** | [⑤ 2-5節 帯域遅延積](05-transport-application.md) |
| HTTPSの証明書エラーが出る | [⑤ 6-4節](05-transport-application.md) |
| 音声・ビデオ会議を優先したい | [⑤ 7節 QoS](05-transport-application.md) |
| ファイアウォールのルールを設計したい | [⑥ 1節](06-security.md) |
| DMZを作りたい | [⑥ 2-1節](06-security.md) |
| **拠点間VPNが繋がらない** | [⑥ 3-2節](06-security.md) |
| リモートワークのVPNが重い | [⑥ 3-3節 スプリットトンネル](06-security.md) |
| ゼロトラストを検討している | [⑥ 4節](06-security.md) |
| SASE / ZTNA を知りたい | [⑥ 5節](06-security.md) |
| Wi-Fiが遅い・不安定 | [⑦ 2節](07-wireless-wan.md) |
| 拠点間の回線を選びたい | [⑦ 3節](07-wireless-wan.md) |
| SD-WANを検討している | [⑦ 5節](07-wireless-wan.md) |
| VPCのCIDRを決めたい | [⑧ 1-2節](08-cloud-network.md) |
| **クラウドの通信費が高い** | [⑧ 2-2節・2-3節](08-cloud-network.md) |
| セキュリティグループとNACLの違い | [⑧ 3節](08-cloud-network.md) |
| Kubernetesのネットワーク設計 | [⑧ 8節](08-cloud-network.md) |
| **自社の規模に合う構成が知りたい** | [⑨ 規模別構成パターン](09-scale-patterns.md) |
| いつ構成を見直すべきか知りたい | [⑨ 6節 移行トリガー](09-scale-patterns.md) |
| **オンプレとクラウド、どちらにすべきか** | [⑩ 8節 判断チェックリスト](10-onprem-cloud-hybrid.md) |
| クラウド移行の進め方 | [⑩ 6節](10-onprem-cloud-hybrid.md) |
| 監視の仕組みを作りたい | [⑪ 1節](11-operations.md) |
| **障害の切り分け手順が知りたい** | [⑪ 2節](11-operations.md) |
| バックアップ・BCPを整えたい | [⑪ 4節](11-operations.md) |
| 設定変更で事故を減らしたい | [⑪ 6節 変更管理](11-operations.md) |

---

## 2. 症状別トラブル早見表（全章横断）

| 症状 | 最有力の原因 | 参照 |
| --- | --- | --- |
| `169.254.x.x` が付いている | DHCPに到達できていない | [③ 1-2](03-ip-subnet.md) |
| 全社が突然停止 | **L2ループ** | [② 4](02-physical-datalink.md) |
| pingは通るがアプリが繋がらない | ポートがFWで塞がれている | [⑤ 8](05-transport-application.md) |
| `ping 8.8.8.8` はOK、名前解決NG | **DNS** | [⑤ 4](05-transport-application.md) |
| 大きいファイルだけ失敗 | **MTU / PMTUD** | [① 4-3](01-network-basics.md) |
| VPN越しだけ不調 | MTU・MSSクランプ | [⑥ 3-2](06-security.md) |
| 疎通はするが異常に遅い | デュプレックスミスマッチ | [② 1-5](02-physical-datalink.md) |
| 片方向だけ通信できる | **戻りの経路がない** | [④ 10](04-routing.md) |
| 突然Wi-Fiが全員切れる（数十秒） | **DFS**（レーダー検知） | [⑦ 1-3](07-wireless-wan.md) |
| APが再起動を繰り返す | **PoE電力不足** | [② 1-4](02-physical-datalink.md) |
| 新VLANでIPが取れない | `ip helper-address` 設定漏れ | [③ 4-3](03-ip-subnet.md) |
| OSPFが ExStart で止まる | **MTU不一致** | [④ 4-4](04-routing.md) |
| PCではOK、スマホで証明書エラー | **中間証明書の設定漏れ** | [⑤ 6-4](05-transport-application.md) |
| クラウドで通信できない | SG/NACL/ルートテーブル | [⑧ 9](08-cloud-network.md) |
| クラウド請求が急増 | NAT GW・Egress・AZ間通信 | [⑧ 2-2](08-cloud-network.md) |
| 会議室が満員だとWi-Fiが不安定 | 人体減衰＋端末密度 | [⑦ 2-4](07-wireless-wan.md) |

---

## 3. コマンド集

### 3-1. 基本の疎通確認

| 目的 | Linux / macOS | Windows |
| --- | --- | --- |
| IP確認 | `ip addr` | `ipconfig /all` |
| 疎通 | `ping 8.8.8.8` | `ping 8.8.8.8` |
| 経路追跡 | `traceroute example.com` | `tracert example.com` |
| 経路表 | `ip route` | `route print` |
| ARPテーブル | `ip neigh` | `arp -a` |
| DNS確認 | `dig example.com` | `nslookup example.com` |
| 接続状態 | `ss -tunap` | `netstat -ano` |
| ポート疎通 | `nc -zv host 443` | `Test-NetConnection host -Port 443` |
| MTU確認 | `ping -M do -s 1472 host` | `ping -f -l 1472 host` |
| DNSキャッシュ削除 | `resolvectl flush-caches` | `ipconfig /flushdns` |
| IP再取得 | `dhclient -r && dhclient` | `ipconfig /release && ipconfig /renew` |

### 3-2. Cisco IOS 系（確認コマンド）

```
show ip interface brief          インタフェース一覧とIP・状態
show interface Gi0/1             詳細（速度・二重・エラーカウンタ）
show interface status            ポート状態・VLAN・速度の一覧
show mac address-table           MACアドレステーブル
show vlan brief                  VLAN一覧
show spanning-tree               STPの状態・ルートブリッジ
show ip route                    経路表
show ip ospf neighbor            OSPF隣接状態（FULL/2WAYならOK）
show ip bgp summary              BGPセッション状態
show etherchannel summary        LAG（EtherChannel）の状態
show cdp neighbors detail        隣接機器の情報
show logging                     ログ
show processes cpu sorted        CPU使用率（ループ検知に有用）
show power inline                PoE給電状況とバジェット
```

### 3-3. 作業時の安全策

```
reload in 10          10分後に再起動を予約（締め出し対策）
reload cancel         正常に接続できたら取り消す
copy run start        設定を保存（これを忘れると再起動で消える）
show archive config differences   設定差分の確認
```

### 3-4. Linux サーバー側

```
ss -tlnp                          LISTENしているポートとプロセス
ss -tan state syn-sent            SYN_SENT の滞留を確認
tcpdump -i eth0 -nn port 443      パケットキャプチャ
iftop / nload                     リアルタイムの帯域使用
mtr example.com                   ping + traceroute の統合（継続測定）
curl -v https://example.com       HTTP/TLSの詳細な挙動
openssl s_client -connect host:443 -servername host   証明書チェーンの確認
```

---

## 4. 計算・設計の早見表

### 4-1. サブネット早見表

| CIDR | マスク | ホスト数 | ブロック幅（第4オクテット） |
| --- | --- | --- | --- |
| /30 | 255.255.255.252 | 2 | 4 |
| /29 | 255.255.255.248 | 6 | 8 |
| /28 | 255.255.255.240 | 14 | 16 |
| /27 | 255.255.255.224 | 30 | 32 |
| /26 | 255.255.255.192 | 62 | 64 |
| /25 | 255.255.255.128 | 126 | 128 |
| **/24** | **255.255.255.0** | **254** | 256 |
| /23 | 255.255.254.0 | 510 | — |
| /22 | 255.255.252.0 | 1022 | — |
| /16 | 255.255.0.0 | 65534 | — |

**暗算のコツ**：`256 − マスクの最終値 = ブロック幅`。ホスト数 = `2^(32−プレフィックス) − 2`

### 4-2. 設計の数値目標

| 項目 | 目安 |
| --- | --- |
| 1セグメントの端末数 | **250台以内**（/24 の範囲） |
| 端末台数の見積もり | **人数 × 2〜3** |
| Wi-Fi RSSI（業務） | **−65dBm 以上** |
| Wi-Fi SNR | 25dB 以上 |
| AP 1台あたり | **20〜30台** |
| Wi-Fi チャネル幅（高密度） | 20〜40MHz |
| 回線帯域の増強検討 | **ピーク使用率 70%** |
| DHCPプールの拡張検討 | 使用率 80% |
| PoEバジェットの余裕 | 使用率 80%以下 |
| 音声（VoIP）の品質要件 | **遅延<150ms、ジッタ<30ms、ロス<1%** |
| 機器の更改サイクル | **5年** |
| ログの保管期間 | **最低3ヶ月、可能なら1年** |
| バックアップ復元テスト | **年2回以上** |
| 冗長系の切替テスト | 年1回 |

### 4-3. LANケーブル選定

| 用途 | 推奨 |
| --- | --- |
| オフィス新規配線 | **CAT6A（UTP）** |
| 既存が1Gで十分 | CAT5e で可（新規なら CAT6以上） |
| フロア間・建物間 | **光ファイバ（SMF）** |
| DC内の短距離 | MMF（OM4）または DAC |
| ノイズが多い工場 | STP（**両端アース必須**）または光 |

### 4-4. MTU の目安

| 環境 | MTU |
| --- | --- |
| 標準 Ethernet | 1500 |
| PPPoE | 1454 / 1492 |
| IPsec VPN | 1400前後 |
| ジャンボフレーム（DC内） | 9000 |

---

## 5. 用語辞典（五十音・アルファベット順）

### アルファベット

| 用語 | 読み・正式名称 | 意味 | 章 |
| --- | --- | --- | --- |
| **ACL** | Access Control List | 通信の許可/拒否のルール一覧 | ⑥ |
| **AD値** | Administrative Distance | 経路情報の信頼度。小さいほど優先 | ④ |
| **APIPA** | — | DHCP失敗時に自動で付く `169.254.x.x` | ③ |
| **ARP** | Address Resolution Protocol | IPアドレスからMACアドレスを調べる | ③ |
| **AS** | Autonomous System | BGPにおける組織単位。AS番号で識別 | ④ |
| **AZ** | Availability Zone | クラウドの独立した設備区画 | ⑧ |
| **BGP** | Border Gateway Protocol | AS間の経路交換。インターネットの基盤 | ④ |
| **BPDU** | Bridge Protocol Data Unit | STPが交換する制御フレーム | ② |
| **CASB** | Cloud Access Security Broker | SaaS利用の可視化・制御 | ⑥ |
| **CDN** | Content Delivery Network | エッジでキャッシュ配信 | ⑧ |
| **CIDR** | Classless Inter-Domain Routing | `/24` のようなプレフィックス表記 | ③ |
| **DFS** | Dynamic Frequency Selection | 5GHz帯でレーダーを検知しチャネル変更 | ⑦ |
| **DHCP** | — | IPアドレスの自動配布 | ③ |
| **DMZ** | DeMilitarized Zone | 公開サーバーを置く隔離区画 | ⑥ |
| **DNS** | Domain Name System | 名前とIPアドレスの変換 | ⑤ |
| **DoH / DoT** | DNS over HTTPS / TLS | DNS通信の暗号化 | ⑤ |
| **DSCP** | Differentiated Services Code Point | QoSの優先度マーキング | ⑤ |
| **ECMP** | Equal Cost Multi-Path | 等コストの複数経路で負荷分散 | ④ |
| **EDR** | Endpoint Detection and Response | 端末側の脅威検知・対処 | ⑥ |
| **EOL / EOS** | End of Life / Support | 製品の販売終了／保守終了 | ⑨⑪ |
| **EVPN** | Ethernet VPN | VXLANの制御プレーン。BGP拡張 | ⑨ |
| **FCS** | Frame Check Sequence | フレームの誤り検出符号 | ① |
| **GARP** | Gratuitous ARP | 自分から一方的に送るARP。切替通知等 | ③ |
| **HSRP** | Hot Standby Router Protocol | ゲートウェイ冗長（Cisco独自） | ④ |
| **IGP / EGP** | Interior / Exterior Gateway Protocol | 組織内／組織間のルーティングプロトコル | ④ |
| **IPsec** | — | IPレベルの暗号化。サイト間VPNの定番 | ⑥ |
| **IX** | Internet eXchange | ISP同士の相互接続点 | ⑧ |
| **LACP** | Link Aggregation Control Protocol | リンク束ね（LAG）の標準プロトコル | ② |
| **LAG** | Link Aggregation | 複数リンクを1本に束ねる | ② |
| **MAC アドレス** | Media Access Control | 機器に焼き付けられた48ビットの識別子 | ② |
| **MLAG / vPC / VSS** | — | 2台のスイッチを1台に見せる技術 | ⑨ |
| **MLO** | Multi-Link Operation | Wi-Fi 7の複数帯域同時利用 | ⑦ |
| **MTU** | Maximum Transmission Unit | 1フレームで運べる最大データ長 | ① |
| **NACL** | Network ACL | クラウドのサブネット単位フィルタ（**ステートレス**） | ⑧ |
| **NAT / NAPT** | Network Address (Port) Translation | プライベートIP↔グローバルIPの変換 | ③ |
| **NDR** | Network Detection and Response | 通信から異常を検知 | ⑥ |
| **NetFlow / sFlow** | — | 通信フローの記録・可視化 | ⑪ |
| **NGFW** | Next Generation Firewall | アプリ識別・ユーザー識別ができるFW | ⑥ |
| **NTP** | Network Time Protocol | 時刻同期。**運用の前提条件** | ⑪ |
| **OFDMA** | — | Wi-Fi 6の多台数効率化技術 | ⑦ |
| **OSPF** | Open Shortest Path First | 企業内で最も使われる動的ルーティング | ④ |
| **OT** | Operational Technology | 工場の制御系。IT系と分離すべき領域 | ⑥⑨ |
| **OUI** | Organizationally Unique Identifier | MACアドレス前半24bit。メーカー識別 | ② |
| **PBR** | Policy Based Routing | 宛先以外の条件で経路を変える | ④ |
| **PMTUD** | Path MTU Discovery | 経路上の最小MTUを自動検出 | ①⑤ |
| **PoE** | Power over Ethernet | LANケーブルで給電 | ② |
| **PON** | Passive Optical Network | 1本の光を分岐して共有（FTTHの方式） | ⑦ |
| **QUIC** | — | UDP上の信頼性プロトコル。HTTP/3の土台 | ⑤ |
| **RADIUS** | — | 認証サーバーのプロトコル。802.1Xで使用 | ⑥ |
| **RPO / RTO** | Recovery Point / Time Objective | 目標復旧時点／目標復旧時間 | ⑪ |
| **RSSI** | Received Signal Strength Indicator | 受信信号強度（dBm） | ⑦ |
| **RSTP** | Rapid STP（802.1w） | 高速収束版STP。**現在の標準** | ② |
| **RTT** | Round Trip Time | 往復遅延時間 | ⑤ |
| **SASE** | Secure Access Service Edge | SD-WAN＋クラウド型セキュリティ | ⑥ |
| **SD-WAN** | Software Defined WAN | WANをソフトウェアで一元制御 | ⑦ |
| **SG** | Security Group | クラウドのインスタンス単位FW（**ステートフル**） | ⑧ |
| **SIEM** | Security Information and Event Management | ログ集約と相関分析 | ⑥ |
| **SLA** | Service Level Agreement | 品質保証の契約 | ⑦ |
| **SLAAC** | Stateless Address Autoconfiguration | IPv6のアドレス自動構成 | ③ |
| **SNMP** | Simple Network Management Protocol | 機器監視の標準プロトコル | ⑪ |
| **SPOF** | Single Point of Failure | 単一障害点 | ⑪ |
| **SSE** | Security Service Edge | SASEからSD-WANを除いた部分 | ⑥ |
| **STP** | Spanning Tree Protocol | L2ループを防ぐ | ② |
| **SWG** | Secure Web Gateway | クラウド型のWebフィルタ | ⑥ |
| **TCO** | Total Cost of Ownership | 総保有コスト（初期＋運用） | ⑩ |
| **TLS** | Transport Layer Security | 暗号化・完全性・認証 | ⑤ |
| **TTL** | Time To Live | パケットの生存ホップ数／DNSのキャッシュ時間 | ①⑤ |
| **TWT** | Target Wake Time | Wi-Fi 6の省電力機能 | ⑦ |
| **UTM** | Unified Threat Management | 多機能を1台に統合したセキュリティ機器 | ⑥ |
| **VLAN** | Virtual LAN | スイッチを論理的に分割 | ② |
| **VPC / VNet** | Virtual Private Cloud / Network | クラウド上の自社ネットワーク空間 | ⑧ |
| **VRF** | Virtual Routing and Forwarding | 経路表を複数持つ。**L3版のVLAN** | ④ |
| **VRRP** | Virtual Router Redundancy Protocol | ゲートウェイ冗長（標準規格） | ④ |
| **VXLAN** | Virtual eXtensible LAN | L3上にL2をオーバーレイ。VLAN上限を突破 | ⑨ |
| **WAF** | Web Application Firewall | Webアプリ特有の攻撃を防ぐ | ⑥ |
| **ZTNA** | Zero Trust Network Access | VPNの代替。アプリ単位のアクセス制御 | ⑥ |
| **802.1Q** | — | VLANタグの規格 | ② |
| **802.1X** | — | ネットワーク接続時の認証 | ⑥ |
| **3-2-1ルール** | — | バックアップの原則（3コピー・2媒体・1遠隔） | ⑪ |

### 日本語

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **アクセスポート** | 端末を接続するポート。1VLANに所属 | ② |
| **カプセル化** | 層を下るたびにヘッダを付けること | ① |
| **輻輳（ふくそう）** | 通信が混雑して詰まること | ⑤ |
| **ブロードキャストストーム** | ループでブロードキャストが増殖し停止する現象 | ② |
| **フルトンネル / スプリットトンネル** | VPNで全通信を通すか、社内宛てのみ通すか | ⑥ |
| **ヘアピン（バックホール）** | 拠点の通信を本社経由にすること | ⑥⑦ |
| **ローカルブレイクアウト** | 拠点から直接インターネットへ出すこと | ⑦ |
| **ロンゲストマッチ** | 最も詳しい（プレフィックスが長い）経路を選ぶ規則 | ④ |
| **トランクポート** | 複数VLANをタグ付きで通すポート | ② |
| **責任共有モデル** | クラウドで基盤は事業者、設定とデータは利用者の責任 | ⑩ |
| **ラテラルムーブメント** | 侵入後に内部で横展開すること | ⑥ |
| **リパトリエーション** | クラウドからオンプレへ戻すこと | ⑩ |
| **デュプレックスミスマッチ** | 全二重/半二重の不一致。遅さの古典的原因 | ② |
| **フローティングスタティック** | AD値を大きくした予備経路 | ④ |
| **サイトサーベイ** | 無線LANの電波調査 | ⑦ |

---

## 6. 章別 最重要ポイント総まとめ

| 章 | 一番大事なこと |
| --- | --- |
| ① 基礎 | **IPは最終目的地、MACは次の1ホップ**。切り分けは下の層から |
| ② L1/L2 | **トラブルの過半数はここ**。ループは全社を止める。PoEバジェットを検算する |
| ③ IP/サブネット | **IPアドレス設計はやり直せない**。将来の3倍で、クラウドと重複させない |
| ④ ルーティング | **ロンゲストマッチ → AD → メトリック**。**往復で設計する** |
| ⑤ L4/L7 | **遠距離が遅いのはRTTの問題**。増速しても直らない |
| ⑥ セキュリティ | **境界防御だけでは足りない**。まずMFA。VPN機器のパッチが最優先 |
| ⑦ 無線/WAN | **APを増やす前にチャネル設計**。「2社契約」でも物理経路が同じことがある |
| ⑧ クラウド | **CIDRは縮小できない**。SGはステートフル、NACLはステートレス |
| ⑨ 規模別 | 判断は**人数ではなく損害額**。**配線とIP設計だけは将来規模で作る** |
| ⑩ 配置 | **5年TCO＋人件費で比較**。ハイブリッドは運用コストが最も高くなり得る |
| ⑪ 運用 | **冗長化と監視はセット**。「取れている」と「戻せる」は別 |

---

← [総合インデックスに戻る](README.md)
