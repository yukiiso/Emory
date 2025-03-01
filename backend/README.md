## 📂 ディレクトリ構成
backend/
│── api/                # API関連
│   ├── __init__.py     # APIの初期化
│   ├── dynamo_api.py   # DynamoDB用API
│   ├── sql_api.py      # MySQL用API
│── tests/              # テストコード
│   ├── conftest.py     # pytest 設定
│   ├── __init__.py
│── app.py              # Flaskアプリのエントリーポイント
│── config.py           # 設定ファイル（環境変数の管理）
│── Dockerfile          # Docker用設定ファイル
│── dynamo.py           # DynamoDB関連の処理
│── models.py           # SQLAlchemyのデータモデル定義
│── routes.py           # ルーティング設定
│── run.py              # アプリの起動スクリプト
│── seed.py             # 初期データ投入用スクリプト
│── utils.py            # ユーティリティ関数
│── requirements.txt    # 依存ライブラリ一覧 (docker compose で呼ばれる)
│── README.md           # 本ファイル


## ヘルスチェックについて
大まかなヘルスチェックポイントは二箇所
[バックエンド全体のヘルスチェック](http://localhost:5001/health)
[API ヘルスチェック](http://localhost:5001/api/health)

## 実際のコーディングについて
### 全体の仕組み
docker composeした時に、run.pyが走る。  
run.pyがapp.pyを呼び出して、create_app()する。
その際、config.pyがconfig.envを参照して、今が開発環境なのか本番環境なのかと、それに対応するDBエンドポイントをとってくる。　　
また、create_app()の中で、まずmodels.pyを参照してRDSのスキーマを取得して、CREATE　TABLEする。　　
その後、seed_database(app)で、INSERTを行う。　　
現状はUserテーブルだけseed dataしてある。　　
フロントエンドへのレスポンスは基本的に全てJSON形式とする。　　
__init__.pyはディレクトリをモジュールとして認識させる役割があるから、何も書いてなくても消さないように。　　


### ルーティングについて
api/内の各APIファイルでBlueprintを作り、routes.pyでそれをルーティングすることで成立する。
Blueprintはchildをparentより先にregisterする必要があるから注意。　　
各Blueprintを用いた最終的なルーティングは各APIファイルに記述する。　
utils.pyはAPIではないが、ヘルスチェックやロゴの取得など一般的なルーティングを行う場所。　　

### dbアクセスについて
RDSのMySQLが2つ(mysql_db, mysql_test_db)と、NoSQLのDynamoDBU(dynamodb_local)がある。
それぞれアクセス用のエンドポイントはconfig.pyにある。(config)
また、DB確認用のAPIを作った。
[User](http://localhost:5001/api/db/sql/User)
[Question](http://localhost:5001/api/db/sql/Question)
[Record](http://localhost:5001/api/db/sql/Record)
[FaceAnalysis](http://localhost:5001/api/db/sql/FaceAnalysis)
[VoiceAnalysis](http://localhost:5001/api/db/sql/VoiceAnalysis)

Dynamo用の確認APIは明日作る


### テストについて
```pytest```で呼び出せる。
テスト内では、create_app()で新しくappを呼び出せる。開発用ではなく、自動的にテスト用のDBを使うため、開発用のDBが上書きされることはない。(dynamoは知らん)

