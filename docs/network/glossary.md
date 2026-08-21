---
title: ネットワーク 用語集・チートシート
---

# 用語集・チートシート

[← 総合インデックスに戻る](README.md)

全章横断の用語辞典と、「困った時どの章？」の逆引き表、実務で引くための早見表をまとめています。

---

## 1. 用語集

### 基礎・階層

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **パケット** | 分割されたデータの小包。宛先情報が付く | [①](01-network-basics.md) |
| **カプセル化** | 層を降りるたびにヘッダを付けること | [①](01-network-basics.md) |
| **OSI 7階層** | ネットワークの役割を7層に分けた参照モデル | [①](01-network-basics.md) |
| **TCP/IP 4階層** | 実際のインターネットで使われる4層モデル | [①](01-network-basics.md) |
| **LAN / WAN** | 建物内 / 拠点間のネットワーク | [①](01-network-basics.md) |
| **DMZ** | 社内と外部の中間地帯。公開サーバを置く | [①](01-network-basics.md)・[⑥](06-security.md) |
| **RTT** | 往復遅延時間。**Web表示速度を支配する** | [①](01-network-basics.md) |
| **帯域 / 遅延 / ロス** | 速さの3指標。太さ / 長さ / 紛失率 | [①](01-network-basics.md) |
| **ブロードキャストドメイン** | ブロードキャストが届く範囲。**1つに詰め込みすぎない** | [①](01-network-basics.md) |

### L1・L2（物理・データリンク）

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **Cat5e / Cat6 / Cat6A** | LANケーブルの規格。**新規はCat6A** | [②](02-physical-datalink.md) |
| **PoE / PoE+ / PoE++** | LANケーブルでの給電。25.5W / 51W | [②](02-physical-datalink.md) |
| **PoEバジェット** | スイッチ全体の給電容量。**ポート単位で考えると事故る** | [②](02-physical-datalink.md) |
| **MACアドレス** | NICに焼かれた48ビットの固有番号 | [②](02-physical-datalink.md) |
| **MACアドレステーブル** | スイッチが学習する「どのポートにどのMAC」の表 | [②](02-physical-datalink.md) |
| **フラッディング** | 宛先未知のフレームを全ポートへ流すこと | [②](02-physical-datalink.md) |
| **VLAN** | 1台のスイッチを論理的に分割する仕組み | [②](02-physical-datalink.md) |
| **802.1Q / タグVLAN** | 複数VLANを1本のリンクで通す（トランク） | [②](02-physical-datalink.md) |
| **ネイティブVLAN** | トランク上のタグなしVLAN。**不一致が定番のミス** | [②](02-physical-datalink.md) |
| **STP / RSTP** | ループを防ぐ仕組み。**RSTPが現在の標準** | [②](02-physical-datalink.md) |
| **ブロードキャストストーム** | ループでブロードキャストが増殖し全停止する現象 | [②](02-physical-datalink.md) |
| **BPDUガード** | 誤って挿されたスイッチを自動遮断する保護機能 | [②](02-physical-datalink.md) |
| **LAG / LACP** | 複数リンクを束ねる。**1フローは1本しか使わない** | [②](02-physical-datalink.md) |
| **スタック / MLAG / VSS** | 複数スイッチを1台に見せる冗長化 | [②](02-physical-datalink.md) |
| **ランダムMAC** | 端末がSSIDごとに変えるMAC。**MAC認証が通らない原因** | [②](02-physical-datalink.md) |
| **802.1X** | ユーザー単位の認証。RADIUSと組み合わせる | [②](02-physical-datalink.md)・[⑥](06-security.md) |

### L3（IP・ルーティング）

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **サブネットマスク / CIDR** | どこまでがネットワーク部かを示す | [③](03-ip-routing.md) |
| **ネットワークアドレス / ブロードキャストアドレス** | 各セグメントの先頭と末尾。**端末に割り当て不可** | [③](03-ip-routing.md) |
| **プライベートIP（RFC1918）** | 10 / 172.16-31 / 192.168 の範囲 | [③](03-ip-routing.md) |
| **APIPA（169.254.x.x）** | **DHCP失敗時に自動で付くアドレス** | [③](03-ip-routing.md) |
| **デフォルトゲートウェイ** | 自分のセグメント外へ出るときの出口 | [③](03-ip-routing.md) |
| **ARP** | IPアドレスからMACアドレスを解決する仕組み | [③](03-ip-routing.md) |
| **ロンゲストマッチ** | **より細かい経路が優先される**というルーティングの原則 | [③](03-ip-routing.md) |
| **デフォルトルート（0.0.0.0/0）** | 表に載っていない宛先の投げ先 | [③](03-ip-routing.md) |
| **OSPF** | リンクステート型。**社内・DC内の標準** | [③](03-ip-routing.md) |
| **BGP** | AS間ルーティング。**インターネットとクラウド接続の必須技術** | [③](03-ip-routing.md)・[⑩](10-hybrid-patterns.md) |
| **NAT / NAPT** | プライベートIPをグローバルIPに変換。ポートで多対1 | [③](03-ip-routing.md) |
| **ポートフォワード** | 外部からの特定ポートを内部サーバへ転送 | [③](03-ip-routing.md) |
| **MTU** | 1パケットの最大サイズ。通常1500 | [③](03-ip-routing.md) |
| **PMTUD** | 経路上の最小MTUを自動検出する仕組み。**ICMPを塞ぐと壊れる** | [③](03-ip-routing.md) |
| **MSSクランプ** | ルータがMSS値を書き換えてMTU問題を回避する設定 | [③](03-ip-routing.md) |
| **IPv6 / デュアルスタック** | 128ビットアドレス / v4とv6の併用 | [③](03-ip-routing.md) |
| **ICMP / traceroute** | 診断用プロトコル / 経路確認コマンド | [③](03-ip-routing.md) |

### L4（TCP・UDP）

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **ポート番号** | 機器の中のどのアプリか | [④](04-transport-tcp-udp.md) |
| **5タプル** | 送信元IP/ポート・宛先IP/ポート・プロトコル。**通信の識別単位** | [④](04-transport-tcp-udp.md) |
| **エフェメラルポート** | クライアントが一時的に使うポート（49152〜） | [④](04-transport-tcp-udp.md) |
| **3wayハンドシェイク** | SYN → SYN+ACK → ACK の接続確立 | [④](04-transport-tcp-udp.md) |
| **TIME_WAIT** | 切断後の待機状態。大量なら短時間接続の繰り返し | [④](04-transport-tcp-udp.md) |
| **CLOSE_WAIT** | **溜まったらアプリのclose漏れ** | [④](04-transport-tcp-udp.md) |
| **スライディングウィンドウ** | ACKを待たずに送れる量 | [④](04-transport-tcp-udp.md) |
| **BDP（帯域遅延積）** | 帯域×RTT。**太い回線でも遠いと速度が出ない理由** | [④](04-transport-tcp-udp.md) |
| **輻輳制御 / CUBIC / BBR** | 混雑時の送信量制御。**長距離・無線ならBBR** | [④](04-transport-tcp-udp.md) |
| **QUIC** | UDP上の新トランスポート。HTTP/3の土台 | [④](04-transport-tcp-udp.md) |
| **HoLブロッキング** | 先頭の詰まりで後続が待たされる現象 | [④](04-transport-tcp-udp.md) |
| **SYNフラッド / SYN Cookie** | 接続キューを埋める攻撃 / その対策 | [④](04-transport-tcp-udp.md) |

### L7（アプリケーション）

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **DHCP / DHCPリレー** | IP等の自動配布 / VLANを越えて中継する設定 | [⑤](05-application-dns-http.md) |
| **DHCPスヌーピング** | 不正なDHCPサーバを遮断する機能 | [⑤](05-application-dns-http.md)・[⑥](06-security.md) |
| **TTL（DNS）** | キャッシュ保持時間。**移行前に下げる** | [⑤](05-application-dns-http.md) |
| **スプリットDNS** | 社内と社外で異なるIPを返す構成 | [⑤](05-application-dns-http.md) |
| **条件付きフォワーダ** | 特定ドメインだけ別のDNSへ転送。**ハイブリッドの要** | [⑤](05-application-dns-http.md)・[⑩](10-hybrid-patterns.md) |
| **HTTP/2 / HTTP/3** | 多重化 / QUIC上のHTTP（**UDP 443**） | [⑤](05-application-dns-http.md) |
| **TLS 1.3** | 現在の暗号化標準。1-RTT・0-RTT | [⑤](05-application-dns-http.md) |
| **中間証明書** | サーバ証明書とルートCAをつなぐ証明書。**設定漏れが定番** | [⑤](05-application-dns-http.md) |
| **ACME / Let's Encrypt** | 証明書の自動発行・更新の仕組み | [⑤](05-application-dns-http.md) |
| **L4 LB / L7 LB** | ポートで振り分け / URL・ヘッダで振り分け | [⑤](05-application-dns-http.md) |
| **ヘルスチェック** | 死んだサーバを切り離す仕組み。**LBの本質** | [⑤](05-application-dns-http.md) |
| **スティッキーセッション** | 同じサーバに固定する仕組み。**外部化のほうが望ましい** | [⑤](05-application-dns-http.md) |
| **リバースプロキシ** | サーバ側に立つ代理。TLS終端・負荷分散 | [⑤](05-application-dns-http.md) |
| **X-Forwarded-For** | 元の送信元IPを伝えるヘッダ | [⑤](05-application-dns-http.md) |
| **CDN** | エッジから配信して遅延を縮める | [⑤](05-application-dns-http.md) |
| **NTP** | 時刻同期。**ずれると認証・証明書・ログが壊れる** | [⑤](05-application-dns-http.md) |

### セキュリティ

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **ステートフルインスペクション** | 通信の状態を覚えて戻りを自動許可するFW | [⑥](06-security.md) |
| **NGFW** | アプリ種別・ユーザーまで判断する次世代FW | [⑥](06-security.md) |
| **デフォルト拒否** | 明示的に許可した以外は全拒否。**FW設計の原則** | [⑥](06-security.md) |
| **IDS / IPS** | 侵入検知 / 侵入防御 | [⑥](06-security.md) |
| **WAF** | Webアプリへの攻撃を遮断。**FWとは守る層が違う** | [⑥](06-security.md) |
| **IPsec / SSL-VPN / WireGuard** | VPNの主な方式 | [⑥](06-security.md) |
| **ゼロトラスト** | 場所で信頼せず毎回検証する考え方 | [⑥](06-security.md) |
| **ZTNA** | アプリ単位のアクセス仲介。**VPNの置き換え** | [⑥](06-security.md) |
| **SASE / SSE** | セキュリティ機能をクラウドに集約 / そのセキュリティ部分 | [⑥](06-security.md) |
| **SWG / CASB** | Webアクセス制御 / SaaS利用の可視化と制御 | [⑥](06-security.md) |
| **マイクロセグメンテーション** | サーバ単位で通信を制限 | [⑥](06-security.md) |
| **ラテラルムーブメント** | 侵入後の横展開。**セグメント分離で封じる** | [⑥](06-security.md) |
| **ARPスプーフィング / DAI** | 偽ARPによる盗聴 / その対策 | [⑥](06-security.md) |
| **DDoS（帯域枯渇型）** | 大量通信で回線を埋める。**上流で止めるしかない** | [⑥](06-security.md) |

### 設計・構成

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **SPOF** | 単一障害点。**人も含まれる** | [⑦](07-design-basics.md) |
| **Active-Standby / Active-Active** | 待機型 / 両系稼働型の冗長化 | [⑦](07-design-basics.md) |
| **RTO / RPO** | 復旧目標時間 / 許容データ損失。**DR設計の出発点** | [⑦](07-design-basics.md)・[⑨](09-cloud-patterns.md) |
| **オーバーサブスクリプション** | 上位リンクの収容率。アクセス層で20:1〜4:1 | [⑦](07-design-basics.md) |
| **QoS** | 優先制御。**帯域は増えない** | [⑦](07-design-basics.md) |
| **3層モデル / コラプストコア** | コア・ディストリ・アクセス / 上2層の統合 | [⑦](07-design-basics.md)・[⑧](08-onpremise-patterns.md) |
| **Spine-Leaf** | DCの標準トポロジ。**どのサーバ間も2ホップ** | [⑧](08-onpremise-patterns.md) |
| **VXLAN / EVPN** | L3網の上にL2を作るトンネル技術 | [⑧](08-onpremise-patterns.md) |
| **East-West / North-South** | サーバ間通信 / 外部との通信 | [⑧](08-onpremise-patterns.md) |
| **EOL / EOSL** | 販売終了 / 保守終了。**計画的な更改が必要** | [⑧](08-onpremise-patterns.md) |
| **SD-WAN** | 複数回線をポリシーで一元管理する仕組み | [⑧](08-onpremise-patterns.md)・[⑩](10-hybrid-patterns.md) |

### クラウド・ハイブリッド

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **VPC / VNet** | クラウド上の自社専用ネットワーク | [⑨](09-cloud-patterns.md) |
| **AZ（アベイラビリティゾーン）** | 物理的に分離されたDC群 | [⑨](09-cloud-patterns.md) |
| **パブリック / プライベートサブネット** | **違いはルートテーブルの中身だけ** | [⑨](09-cloud-patterns.md) |
| **セキュリティグループ（SG）** | インスタンス単位のステートフルFW。**SG参照が強力** | [⑨](09-cloud-patterns.md) |
| **ネットワークACL** | サブネット単位のステートレスFW | [⑨](09-cloud-patterns.md) |
| **NAT Gateway** | プライベートサブネットからの外向き通信。**処理データ量課金に注意** | [⑨](09-cloud-patterns.md) |
| **VPCエンドポイント / PrivateLink** | AWSサービスへの閉域接続。**NAT料金の削減にも効く** | [⑨](09-cloud-patterns.md) |
| **VPCピアリング** | VPC間の1対1接続。**推移的ルーティング不可** | [⑨](09-cloud-patterns.md) |
| **Transit Gateway** | VPC・拠点を束ねるハブ。**VPC 4つ以上ならこちら** | [⑨](09-cloud-patterns.md) |
| **IPAM** | CIDRの一元管理・自動払い出し | [⑨](09-cloud-patterns.md) |
| **検査VPC** | 全通信を集中検査するVPC | [⑩](10-hybrid-patterns.md) |
| **Direct Connect / ExpressRoute / Interconnect** | 各クラウドへの専用線サービス。**BGP必須** | [⑩](10-hybrid-patterns.md) |
| **ローカルブレイクアウト** | SaaS通信をVPNに通さず直接出す | [⑩](10-hybrid-patterns.md) |
| **非対称ルーティング** | 行きと帰りの経路が違う。**ステートフルFWが落とす** | [⑩](10-hybrid-patterns.md) |
| **リフト&シフト** | そのままクラウドへ移す。**最大のアンチパターン** | [⑪](11-scale-comparison.md) |
| **TCO** | 総保有コスト。**人件費が30〜40%** | [⑪](11-scale-comparison.md) |

### 運用

| 用語 | 意味 | 章 |
| --- | --- | --- |
| **SNMP / SNMPトラップ** | 機器メトリクス取得 / 機器からの能動通知 | [⑫](12-operations-troubleshooting.md) |
| **Syslog** | ログの集約プロトコル | [⑫](12-operations-troubleshooting.md) |
| **NetFlow / sFlow** | **誰がどこと何バイト通信したかの可視化** | [⑫](12-operations-troubleshooting.md) |
| **合成監視（外形監視）** | 実ユーザーの体験を模擬する監視 | [⑫](12-operations-troubleshooting.md) |
| **アラート疲れ** | 通知が多すぎて無視される状態 | [⑫](12-operations-troubleshooting.md) |
| **IaC** | 設定をコードで管理・適用 | [⑫](12-operations-troubleshooting.md) |
| **ドリフト** | コードと実機の設定のズレ | [⑨](09-cloud-patterns.md)・[⑫](12-operations-troubleshooting.md) |
| **アウトオブバンド管理** | 通常経路と別の管理経路。**自爆対策** | [⑫](12-operations-troubleshooting.md) |
| **ポストモーテム** | 障害の振り返り。**人ではなく仕組みを責める** | [⑫](12-operations-troubleshooting.md) |

---

## 2. 「困った時どの章？」逆引き表

| やりたいこと・困っていること | 章 |
| --- | --- |
| ネットワークの仕組みを一から知りたい | [①](01-network-basics.md) |
| スイッチとルータの違いが分からない | [① 6章](01-network-basics.md) |
| LANケーブルの規格を選びたい | [② 1章](02-physical-datalink.md) |
| **APが起動しない・PoEが足りない** | [② 1章](02-physical-datalink.md) |
| 部署ごとにネットワークを分けたい | [② 4章 VLAN](02-physical-datalink.md) |
| **ネットワークが突然全停止した** | [② 5章 ループ](02-physical-datalink.md)・[⑫ 4章](12-operations-troubleshooting.md) |
| Wi-Fiが遅い・切れる | [② 7章](02-physical-datalink.md) |
| **サブネットの計算がしたい** | [③ 2章](03-ip-routing.md)・[本ページ 5章](#5-サブネット早見表) |
| IPアドレスの範囲を決めたい | [③ 3章](03-ip-routing.md)・[⑦ 5章](07-design-basics.md) |
| **169.254.x.x が付いている** | [③ 3章](03-ip-routing.md) |
| 通信が意図しない経路を通る | [③ 5章 ロンゲストマッチ](03-ip-routing.md) |
| **pingは通るのにページが開かない** | [③ 8章 MTU](03-ip-routing.md) |
| ポート番号を調べたい | [④ 1章](04-transport-tcp-udp.md)・[本ページ 3章](#3-ポート番号一覧) |
| **回線を増速したのに速くならない** | [④ 4章 BDP](04-transport-tcp-udp.md) |
| **「address already in use」が出る** | [④ 7章 ポート枯渇](04-transport-tcp-udp.md) |
| **接続がたまに切れる** | [④ 7章 タイムアウト](04-transport-tcp-udp.md) |
| DHCPで配るIPが足りない | [⑤ 1章](05-application-dns-http.md) |
| 社内と社外で違うIPを返したい | [⑤ 2章 スプリットDNS](05-application-dns-http.md) |
| **証明書が期限切れした** | [⑤ 4章](05-application-dns-http.md) |
| ロードバランサを導入したい | [⑤ 5章](05-application-dns-http.md) |
| サイトを速くしたい | [⑤ 7章 CDN](05-application-dns-http.md)・[① 9章](01-network-basics.md) |
| ファイアウォールのルールを設計したい | [⑥ 2章](06-security.md) |
| **WAFは必要か知りたい** | [⑥ 3章](06-security.md) |
| リモートワークの接続方式を決めたい | [⑥ 4章・5章](06-security.md) |
| **ランサムウェア対策をしたい** | [⑥ 6章・9章](06-security.md) |
| ゲストWi-Fiを安全に提供したい | [⑥ 6章](06-security.md)・[② 4章](02-physical-datalink.md) |
| **可用性99.9%が何を意味するか知りたい** | [⑦ 3章](07-design-basics.md) |
| 冗長化の方式を選びたい | [⑦ 4章](07-design-basics.md) |
| 必要な回線帯域を見積もりたい | [⑦ 6章](07-design-basics.md) |
| **オフィスのネットワークを構築したい** | [⑧](08-onpremise-patterns.md) |
| データセンターを設計したい | [⑧ 3章 Spine-Leaf](08-onpremise-patterns.md) |
| **AWSのネットワークを設計したい** | [⑨](09-cloud-patterns.md) |
| **クラウドの料金が高い** | [⑨ 1章 NAT GW](09-cloud-patterns.md) |
| VPCが増えてきた | [⑨ 2章 TGW](09-cloud-patterns.md) |
| DR構成を作りたい | [⑨ 3章](09-cloud-patterns.md) |
| **オンプレとクラウドを繋ぎたい** | [⑩](10-hybrid-patterns.md) |
| **VPNは繋がるのに名前解決できない** | [⑩ 3-2章 ハイブリッドDNS](10-hybrid-patterns.md) |
| 専用線かVPNか決めたい | [⑩ 1章](10-hybrid-patterns.md) |
| **オンプレとクラウドどちらにすべきか** | [⑪ 2章](11-scale-comparison.md) |
| コストを比較したい | [⑪ 4章 TCO](11-scale-comparison.md) |
| クラウド移行の進め方を知りたい | [⑪ 6章・7章](11-scale-comparison.md) |
| 監視項目を決めたい | [⑫ 1章](12-operations-troubleshooting.md) |
| **障害の切り分け方が分からない** | [⑫ 2章](12-operations-troubleshooting.md) |
| **どの通信が帯域を食っているか知りたい** | [⑫ 1章 NetFlow](12-operations-troubleshooting.md) |
| 設定変更で事故を減らしたい | [⑫ 5章](12-operations-troubleshooting.md) |

---

## 3. ポート番号一覧

| ポート | プロトコル | サービス | 公開可否の目安 |
| --- | --- | --- | --- |
| 20 / 21 | TCP | FTP | ⚠️ 平文。SFTPへ |
| **22** | TCP | **SSH / SFTP** | ❌ **インターネットへ公開しない** |
| 23 | TCP | Telnet | ❌ 平文。使用しない |
| 25 | TCP | SMTP | メールサーバのみ |
| **53** | **UDP / TCP** | **DNS** | 権威DNSのみ。**TCPも塞がない** |
| 67 / 68 | UDP | DHCP | 社内のみ |
| **80** | TCP | HTTP | ✅（443へリダイレクト） |
| 88 | TCP/UDP | Kerberos | 社内のみ |
| 110 / 995 | TCP | POP3 / POP3S | |
| 123 | UDP | **NTP** | 社内のみ |
| 143 / 993 | TCP | IMAP / IMAPS | |
| 161 / 162 | UDP | SNMP / トラップ | ❌ 管理セグメントのみ |
| 389 / 636 | TCP | LDAP / LDAPS | ❌ 社内のみ |
| **443** | TCP / **UDP（HTTP/3）** | **HTTPS** | ✅ |
| **445** | TCP | **SMB** | ❌ **絶対に公開しない** |
| 514 | UDP | Syslog | 社内のみ |
| 587 | TCP | SMTP Submission | ✅ |
| 1812 / 1813 | UDP | RADIUS | 社内のみ |
| **3306** | TCP | **MySQL** | ❌ 公開しない |
| **3389** | TCP | **RDP** | ❌ **絶対に公開しない** |
| **5432** | TCP | **PostgreSQL** | ❌ 公開しない |
| 5060 / 5061 | UDP/TCP | SIP（VoIP） | |
| **6379** | TCP | **Redis** | ❌ **絶対に公開しない**（認証なし既定） |
| 8080 / 8443 | TCP | HTTP代替 / HTTPS代替 | LB配下のみ |
| 9200 | TCP | Elasticsearch | ❌ 公開しない |
| 27017 | TCP | MongoDB | ❌ 公開しない |

---

## 4. コマンドチートシート

```bash
# ─── 到達性・経路 ───────────────────────────────
ping -c 5 8.8.8.8                       # 到達確認・RTT・ロス
ping -s 1472 -M do 8.8.8.8              # MTU検証（1472+28=1500）
traceroute 8.8.8.8                      # 経路確認（Win: tracert）
mtr -rwbzc 100 8.8.8.8                  # 経路＋ロス率。切り分けの主力
ip route                                # ルーティングテーブル（Win: route print）
ip neigh                                # ARPテーブル（Win/Mac: arp -a）
ip -br addr                             # IPアドレス一覧（簡潔表示）

# ─── ポート・コネクション ─────────────────────────
ss -tlnp                                # LISTEN中のポートとプロセス
ss -ant                                 # 全TCPコネクション
ss -ant | awk '{print $1}' | sort | uniq -c   # 状態別集計
nc -zv example.com 443                  # ポート疎通確認
Test-NetConnection example.com -Port 443      # 同上（PowerShell）

# ─── DNS ──────────────────────────────────────
dig example.com                         # 名前解決
dig @8.8.8.8 example.com                # 外部リゾルバで確認（比較用）
dig +trace example.com                  # ルートから追跡
dig example.com MX                      # レコード種別を指定
resolvectl status                       # 使用中のDNSサーバ確認（systemd）

# ─── HTTP・TLS ────────────────────────────────
curl -v https://example.com                              # 詳細表示
curl -o /dev/null -s -w "%{time_total}\n" https://...    # 応答時間
curl --resolve example.com:443:1.2.3.4 https://example.com  # DNSを迂回
openssl s_client -connect example.com:443 -servername example.com
echo | openssl s_client -connect example.com:443 2>/dev/null \
  | openssl x509 -noout -dates                           # 証明書の期限

# ─── キャプチャ ────────────────────────────────
tcpdump -i any port 443 -nn             # 443番の通信
tcpdump -i any host 10.0.0.5 -nn -c 100 # 特定ホスト・100個
tcpdump -i any -w capture.pcap          # 保存（Wiresharkで解析）
tcpdump -i any 'tcp[tcpflags] & tcp-syn != 0'   # SYNのみ抽出

# ─── 帯域測定 ──────────────────────────────────
iperf3 -s                               # サーバ側
iperf3 -c <server>                      # クライアント側
iperf3 -c <server> -P 8                 # 8並列（BDPの影響を確認）
iperf3 -c <server> -u -b 100M           # UDP（ジッタ・ロス）
```

---

## 5. サブネット早見表

| CIDR | サブネットマスク | ホスト数 | ブロックサイズ | 用途 |
| --- | --- | --- | --- | --- |
| /30 | 255.255.255.252 | 2 | 4 | ルータ間P2P |
| /29 | 255.255.255.248 | 6 | 8 | 小さなDMZ |
| /28 | 255.255.255.240 | 14 | 16 | TGWアタッチメント・小規模サーバ群 |
| /27 | 255.255.255.224 | 30 | 32 | 小部署 |
| /26 | 255.255.255.192 | 62 | 64 | 中規模サブネット |
| /25 | 255.255.255.128 | 126 | 128 | |
| **/24** | **255.255.255.0** | **254** | **256** | **標準。1部署・1フロア** |
| /23 | 255.255.254.0 | 510 | 512 | 無線など台数が多い場合 |
| /22 | 255.255.252.0 | 1,022 | 1,024 | 拠点枠の予約 |
| /20 | 255.255.240.0 | 4,094 | 4,096 | |
| **/16** | **255.255.0.0** | **65,534** | **65,536** | **VPC全体・拠点全体の枠** |
| /8 | 255.0.0.0 | 16,777,214 | — | 全社の枠（10.0.0.0/8） |

**計算のコツ**
- ホスト数 = **2^(32−CIDR) − 2**
- /24 を分割：/25 は2個、/26 は4個、/27 は8個、/28 は16個
- **/26 の境界**：`.0` `.64` `.128` `.192`
- **/28 の境界**：`.0` `.16` `.32` `.48` `.64` …

---

## 6. 頻出エラー・症状 早見表

| 症状・エラー | 原因 | 対処 | 章 |
| --- | --- | --- | --- |
| **IPが 169.254.x.x** | DHCP応答なし | ケーブル → スイッチ → DHCPプール枯渇の順に確認 | [③](03-ip-routing.md) |
| **ネットワーク全体が停止** | ループ | 余分なケーブルを抜く。BPDUガード設定 | [②](02-physical-datalink.md) |
| **リンク速度が100Mbps** | オートネゴ失敗・ケーブル内断線 | ケーブル交換 | [②](02-physical-datalink.md) |
| **pingは通るがWebが開かない** | MTU / PMTUD失敗 | MSSクランプ・ICMP Type3 Code4を許可 | [③](03-ip-routing.md) |
| `Connection refused` | サービス未起動・ポート違い | `ss -tlnp` で確認 | [④](04-transport-tcp-udp.md) |
| `Connection timed out` | **FW/SGで遮断**・経路なし | `tcpdump` でSYN/SYN+ACKを確認 | [④](04-transport-tcp-udp.md) |
| `address already in use` | **エフェメラルポート枯渇** | コネクション再利用・プール化 | [④](04-transport-tcp-udp.md) |
| `CLOSE_WAIT` が大量 | **アプリのclose漏れ** | アプリを修正 | [④](04-transport-tcp-udp.md) |
| `NXDOMAIN` | レコード不在・タイポ | `dig @8.8.8.8` と比較 | [⑤](05-application-dns-http.md) |
| `SERVFAIL` | DNSサーバ側の障害・DNSSEC不整合 | 別リゾルバで確認 | [⑤](05-application-dns-http.md) |
| `certificate has expired` | **証明書期限切れ** | 更新。ACME自動化＋期限監視 | [⑤](05-application-dns-http.md) |
| `unable to get local issuer certificate` | **中間証明書の設定漏れ** | サーバ側でチェーンを配信 | [⑤](05-application-dns-http.md) |
| `502 Bad Gateway` | バックエンド停止・タイムアウト | アプリの死活・プロキシのタイムアウト値 | [⑤](05-application-dns-http.md) |
| `504 Gateway Timeout` | バックエンドが遅い | 処理時間・DB・タイムアウト階層 | [⑤](05-application-dns-http.md) |
| 認証だけ失敗する | **時刻ずれ**（Kerberos） | NTP同期を確認 | [⑤](05-application-dns-http.md) |
| **VPNは繋がるが名前解決できない** | DNS転送設定の漏れ | 条件付きフォワーダ / Resolverルール | [⑩](10-hybrid-patterns.md) |
| クラウドのサーバに繋がらない | **SGの設定漏れ**・ルートテーブル | SGのインバウンド・`tcpdump` | [⑨](09-cloud-patterns.md) |
| クラウド料金が急増 | **NAT Gateway・データ転送** | VPCエンドポイント・CloudFront経由へ | [⑨](09-cloud-patterns.md) |

---

## 7. 設計・構築チェックリスト（統合版）

### 設計時
- [ ] IPアドレスが**将来つなぐ相手と重複していない**（→[⑦](07-design-basics.md)）
- [ ] 現在の**2〜3倍の余裕**がある
- [ ] SPOFがない（回線・機器・電源・配線・**人**）
- [ ] **ゲストWi-Fi・IoT・管理系が分離**されている（→[⑥](06-security.md)）
- [ ] FWは**デフォルト拒否**。Any-Anyルールがない
- [ ] 上位リンクの**収容率**が妥当
- [ ] 命名規則が決まっている

### 構築・移行時
- [ ] **フェイルオーバー試験**を実施した
- [ ] MSSクランプを設定した（VPN/トンネル利用時）
- [ ] **DNSの相互解決**を確認した（ハイブリッド時）
- [ ] **NTPを全機器に設定**した
- [ ] ログの集約先と保管期間を設定した
- [ ] **設定バックアップの自動取得**を設定した
- [ ] **切り戻し手順と判断基準**（時間）を用意した

### 運用開始後
- [ ] 監視項目とアラート通知先が設定されている
- [ ] **証明書・ライセンス・保守の期限**が監視されている
- [ ] 構成図・台帳が最新
- [ ] **半期の切替試験・年次のDR訓練**が予定に入っている
- [ ] FWルールの棚卸しが定期実施されている
- [ ] **設定できる人が2人以上いる**

---

## 8. 関連ガイド

| ガイド | 内容 |
| --- | --- |
| [DNS・ドメイン完全ガイド](../dns-guide.md) | DNSの詳細版（レコード種別・移管手順） |
| [光ファイバー・光通信 完全ガイド](../optical-fiber-overview.md) | 物理層の詳細版（FTTH・PON・海底ケーブル） |
| [自作サーバーでWebサイトを公開する方法](../self-hosting-guide.md) | 家庭・SOHO規模の実践 |
| [APIの種類・特徴・歴史 完全ガイド](../api-guide.md) | HTTPより上のレイヤ |
| [SSO（シングルサインオン）完全ガイド](../sso/README.md) | ゼロトラストの認証基盤 |
| [低トラフィックサイト向けシステム構成ガイド](../ando-piano-system-design.md) | 小規模クラウド構成の実例 |
| [Git コマンド一覧](../git-commands.md) | 構成管理（IaC）で使う |

---

[← 総合インデックスに戻る](README.md)
