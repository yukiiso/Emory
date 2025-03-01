## 依存関係のインストール
```
cd frontend
npm install
```

## 📂 ディレクトリ構成
frontend/
│── public/             # 静的ファイル（index.html など）
│── src/                # フロントエンドのソースコード
│   ├── components/     # UIコンポーネント（Navbar など）
│   ├── pages/          # 画面ごとのコンポーネント
│   ├── routes/         # ルーティング設定
│   ├── App.js          # メインコンポーネント
│   ├── config.js       # 環境変数の設定
│── .gitignore          
│── Dockerfile          
│── package.json        # npm の依存関係
│── package-lock.json   # インストール済みのパッケージ情報
│── README.md           # 本ファイル


## 実際のコーディングについて
### 全体の仕組み
src/index.jsの上にApp.jsが呼ばれていて、その中にcomponents/とかpages/が呼ばれている。  
ルーティングはsrc/routes/index.jsで管理している。

### バックエンドAPIの使用について
src/config.jsにバックエンドAPIのエンドポイントが変数としておいてある。(これもconfig.envから取ってきてる)
pages/SampleApiData.jsでやってるように、
```
import { API_URL } from "../config";
```
してから、
```
fetch(`${API_URL}/api/health`)
```
ってすることで、共通のAPIルートを使うことができる。(こうすることでデプロイ時に楽になる)

### cssについて
各ページ(ex: pages/Home.js)に書いてしまってOK!
他のcssに影響を与えないような書き方もあるから、調べてみてくれ！

### テストについて
時間がないから後回しでOK!