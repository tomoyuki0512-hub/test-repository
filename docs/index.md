---
title: ガイド一覧
---

# ガイド一覧

## GitHub・Git

- [Git コマンド一覧](git-commands.md)
- [GitHub 基本ガイド](github-guide.md)

## GitHub Pages・サイト公開

- [ローカルサーバーの起動方法](local-server-guide.md)
- [Jekyllテーマ一覧](jekyll-themes.md)
- [カスタムドメイン設定ガイド](custom-domain.md)
- [DNS・ドメイン完全ガイド](dns-guide.md)
- [自作サーバーでWebサイトを公開する方法](self-hosting-guide.md)
- [GitHub PagesでJavaScriptを使う](github-pages-js.md)

## Web開発基礎

- [WebフレームワークとはなにかまたExpress・Railsとは](framework-basics.md)
- [APIの種類・特徴・歴史 完全ガイド](api-guide.md)
- [データベースの種類まとめ](database-types-guide.md)
- [問い合わせページの作り方](contact-guide.md)

## Claude Codeを使ったアプリ開発

- [Claude Codeでアプリ開発する方法](claude-code-dev-guide.md)
- [Claude Codeアプリ開発 応用編（Docker・CI/CD・スタック選定）](claude-code-dev-guide-advanced.md)
- [Claude Codeで結果をすぐにプレビューする方法](preview-guide.md)

## Claude / AIモデル

- [Claude Opus 4.8 新機能まとめ](opus-4-8/README.md) ← 新機能と使い方の例
  - [概要・ベンチマーク・価格](opus-4-8/01-overview.md)
  - [Effort（労力）制御](opus-4-8/02-effort-control.md)
  - [Fast mode（高速モード）](opus-4-8/03-fast-mode.md)
  - [会話途中のシステムメッセージ](opus-4-8/04-mid-conversation-system-messages.md)
  - [プロンプトキャッシュ・その他](opus-4-8/05-prompt-caching-and-misc.md)
  - [Dynamic Workflows（Claude Code）](opus-4-8/06-dynamic-workflows.md)

## ネットワーク・通信のしくみ

- [光ファイバー ゼロからわかる完全ガイド](optical-fiber-guide.md)
- [光ファイバー ケーブル・コードと接続部材ガイド](optical-fiber-cable-types.md)
- [光ファイバー 大手各社の製品ラインナップまとめ](optical-fiber-vendors.md)
- [住友電工 光ファイバー製品 完全網羅ガイド（実務担当者向け）](sumitomo-electric-optical-fiber.md)

## システム設計・運用

- [低トラフィックサイト向けシステム構成ガイド](ando-piano-system-design.md)

## アプリストア公開（Apple / Google）

- [総合インデックス（はじめに・全体像・用語集）](store-publishing/README.md) ← まずはここから
- [① Apple App Store 公開フロー（ゼロから）](store-publishing/01-apple-app-store.md)
- [② Google Play 公開フロー（ゼロから）](store-publishing/02-google-play.md)
- [③ 収益化パターン（広告・サブスク・ハイブリッド）](store-publishing/03-monetization-ads-subscription.md) ← 広告収入・サブスク収益のモデル別シミュレーション
- [④ Apple vs Google 比較・公開前チェックリスト](store-publishing/04-comparison-checklist.md)
- [⑤ AWSでMacを起動してストア資材を準備する（EC2 Mac 署名ガイド）](store-publishing/05-aws-mac-signing.md) ← Macが無くても署名・ビルド・提出
- [⑥ macOS CIランナー料金とMac購入費の比較](store-publishing/06-macos-ci-and-buying-mac.md) ← GitHub Actions等の料金・物理Mac最低費用

## Flutterアプリ サブスクリプション（IAP）

- [総合インデックス（はじめに・用語集）](flutter-subscription-overview.md) ← まずはここから
- [事業視点ガイド（料金戦略・KPI）](flutter-subscription-business.md)
- [サブスクリプション要件定義資料](flutter-subscription-guide.md)
- [iOS / Android イベント・ステータス一覧](flutter-subscription-events.md)
- [解約・再加入 UX設計ガイド](flutter-subscription-ux.md)
- [解約・再加入 UXモック（HTML）](flutter-subscription-ux-mockup.html)
- [システム構成設計](flutter-subscription-system-design.md)
- [システム構成図（Mermaid / Python Diagrams）](flutter-subscription-architecture-diagram.md)
- [iOS サブスクリプション状態遷移図（SVG）](ios-subscription-lifecycle.md) ← AndroidのライフサイクルにないiOS版をSVGで作図
- [サブスクリプション & RevenueCat 総合ガイド](../revenuecat-subscription-guide.md) ← メリット/デメリット・費用・開発のし易さ・開発ステップ数とサーバー/保守の削減効果

## 年金・社会保障

- [遺族年金・遺族厚生年金 完全ガイド](survivors-pension-guide.md) ← 受給条件と男性・女性・子のパターン別金額例
- [障害年金 完全ガイド](disability-pension-guide.md) ← 受給条件・等級・パターン別金額例
- [国からもらえる保障 まとめ](government-support-guide.md) ← 医療・仕事・子育て・障害・生活の社会保障早見
- [年金 繰上げ・繰下げ 図解ガイド（SVG）](pension-deferral-svg-guide.md) ← 年齢による損益分岐点をSVGで可視化
- [年金と収入の関係（在職老齢年金・収入要件）](pension-income-test-guide.md) ← 働くと止まる？収入が多いともらえない？

## 進学・教育費

- [大学進学のための奨学金・教育ローン 完全ガイド](daigaku-shogakukin-guide.md) ← 給付/無利子/有利子・金利（固定/変動）・借りられる金額を網羅。大学無償化・母子家庭の補助も収録
- [奨学金「代理返還（返還支援）制度」導入企業ガイド](dairihenkan-kigyo-list.md) ← 入社すると会社が奨学金を肩代わり。約4,800社の公式検索リンク・企業例

## 投資・資産形成

- [投資指標と資産シミュレーション まとめ](investment-indicators-simulation.md) ← リターン・標準偏差・シャープレシオ・相関係数の意味と計算、一括・積立投資の成長シミュレーション
- [投資指標・資産シミュレーター（HTML）](investment-simulator.html) ← 指標の計算と複利・積立の成長グラフをブラウザで描画

## 認証・セキュリティ

- [SSO（シングルサインオン）完全ガイド](sso-guide.md) ← 仕組み・SAML/OAuth/OIDCの違い・導入手順を誰でもわかるように

## デザイン・画像

- [画像フォーマットの特徴とWeb・アプリでの使用用途](../image-formats-guide.md)

## 就職・キャリア

- [ケース面接 学習ポータル（HTML）](case-interview-portal.html) ← まずはここから。全教材のフェーズ別ナビ＋練習進捗ダッシュボード
- [ケース面接 完全ガイド（内容と対策）](case-interview-guide.md) ← 出題内容・ファーム別形式・解き方の型・例題と模範解答・3ヶ月対策スケジュール
- [ケース面接で覚えておくべき数値まとめ](case-interview-key-numbers.md) ← 人口・GDP・市場規模・店舗数に加え、世界人口・主要国GDP・日本の代表企業の売上規模も収録
- [ケース面接 頻出お題集（練習問題バンク50問）](case-interview-question-bank.md) ← フェルミ25問＋ビジネスケース20問＋政策系5問を難易度・ヒント付きで
- [業界別ビジネスモデル・KPIガイド](industry-business-models.md) ← コンビニ・外食・航空・ホテル・SaaS・ジム等8業界の収益構造とKPI相場観
- [ケース面接 模擬面接フル対話スクリプト](case-interview-mock-script.md) ← 候補者リード型30分の面接官とのやり取りを再現・💡解説付き
- [ケース面接 練習トレーナー（HTML）](case-practice-trainer.html) ← お題50問をランダム出題。タイマー・ヒント・自己採点の進捗保存つき
- [模擬面接シミュレーター（HTML）](case-mock-simulator.html) ← 面接官の台詞→自分で答える→模範回答と解説を開く、のステップ練習
- [ケース面接 数値暗記フラッシュカード（HTML）](case-numbers-flashcards.html) ← 約60枚をクイズ形式で暗記。カテゴリ別・「覚えた」進捗保存つき
- [暗算・概算ドリル（HTML）](case-math-drill.html) ← 2桁掛け算・%・大数の桁感覚を4択×20秒で特訓。正答率を記録
- [模擬面接 採点ルーブリック（印刷用HTML）](case-interview-rubric.html) ← ペア練習の面接官役用。11項目×5段階の行動アンカー付き採点表
- [直前チートシート（印刷用HTML）](case-interview-cheatsheet.html) ← 型・分解式・最重要数値をA4×2枚に凝縮。面接前日の見直し用
- [行動面接（フィット面接）対策ガイド](fit-interview-guide.md) ← STAR法・頻出質問20・エピソード棚卸し・逆質問集
- [離職率の適正値 完全ガイド](turnover-rate-guide.md) ← 計算方法・全国平均・業界別の目安・適正レンジ・判断基準・改善策

## 学習ツール

- [英単語帳](english-words.html)
