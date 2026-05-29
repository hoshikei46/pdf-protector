# 🔐 PDF パスワード保護ツール

PDFにAES-256パスワードを設定できるWebアプリです。  
URLを共有するだけで、Pythonなしの非エンジニアでも使えます。

## デモ

デプロイ後の URL をここに貼る  
例: `https://pdf-protector.vercel.app`

---

## デプロイ手順（初回のみ・約5分）

### 1. このリポジトリをフォーク or クローン

```bash
git clone https://github.com/あなたのID/pdf-protector.git
cd pdf-protector
```

### 2. Vercel にデプロイ

#### ブラウザから行う場合（推奨）

1. [vercel.com](https://vercel.com) にサインアップ（GitHub連携）
2. ダッシュボードの **"Add New → Project"** をクリック
3. このリポジトリを選択
4. そのまま **"Deploy"** を押す → 完了

#### CLIから行う場合

```bash
npm i -g vercel
vercel
```

---

## ファイル構成

```
pdf-protector/
├── api/
│   └── encrypt.py      # Vercel サーバーレス関数（pikepdf で AES-256 暗号化）
├── public/
│   └── index.html      # フロントエンド UI
├── requirements.txt    # Python 依存パッケージ
├── vercel.json         # Vercel ルーティング設定
└── README.md
```

---

## 技術仕様

| 項目 | 内容 |
|------|------|
| 暗号化方式 | AES-256（PDF規格 R6） |
| ライブラリ | [pikepdf](https://pikepdf.readthedocs.io/)（qpdf ベース） |
| バックエンド | Vercel Serverless Functions（Python） |
| フロントエンド | 純粋な HTML/CSS/JS（フレームワークなし） |
| 最大ファイルサイズ | 4.5MB（Vercel 無料枠の上限） |

---

## ローカルで動かす場合

```bash
pip install flask pikepdf
# api/encrypt.py の代わりに Flask 版を使う場合:
# （別途 Flask 版 app.py が必要）
```

---

## ライセンス

MIT
