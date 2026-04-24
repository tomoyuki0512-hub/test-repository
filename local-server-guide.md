# ローカルサーバーの起動方法

FigmaにHTMLデザインを取り込む際などに使うローカルサーバーの起動方法まとめ。

---

## どこのフォルダで実行する？

**HTMLファイルがあるフォルダ**で実行する。

```
例：C:\Users\yourname\Desktop\mysite\
    ├── index.html
    ├── style.css
    └── script.js
```

```bash
cd C:\Users\yourname\Desktop\mysite
```

---

## 起動コマンド

### Node.js を使う場合

```bash
npx serve .
```

- Node.js が必要（https://nodejs.org）
- デフォルトで `http://localhost:3000` で起動

### Python3 を使う場合

```bash
python3 -m http.server 8080
```

- Python3 が必要（https://www.python.org）
- `http://localhost:8080` で起動

どちらもHTMLファイルがあるフォルダで実行するだけでOK。インストールされている方を使えばよい。

---

## フォルダ構成

特に決まりはないが、`index.html` があると自動的にトップページとして認識される。

```
mysite/
├── index.html   ← http://localhost:3000 でアクセスできる
├── other.html   ← http://localhost:3000/other.html でアクセス
├── style.css
└── script.js
```

---

## そもそも何をしているのか？

HTMLファイルをダブルクリックで開くと `file://` プロトコルで開く。これだと：

- 外部からアクセスできない
- 一部のJavaScriptや拡張機能が動かない（例：Builder.ioのChrome拡張）

ローカルサーバーを起動すると `http://localhost:XXXX` というURLでアクセスできるようになり、本物のWebサーバーと同じ環境になる。

---

## スマホからアクセスする場合

PCとスマホが同じWi-Fiに接続されていれば、スマホのブラウザからもアクセスできる。

1. PCのIPアドレスを確認する
   - Windows: `ipconfig` コマンド → IPv4アドレスを確認
   - Mac/Linux: `ifconfig` または `ip a` コマンド
2. スマホのブラウザで以下にアクセス：
   ```
   http://192.168.1.10:3000   ← PCのIPアドレスに置き換える
   ```

---

## Figmaへの取り込みに使う場合

Builder.io の Chrome拡張 + Figmaプラグインを使う際、`file://` では動作しない場合があるため、このローカルサーバー経由でアクセスする必要がある。
