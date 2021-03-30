## serverless-apiでspotifyのレコメンド検索強化版
- Spotifyのrelated_artistとかレコメンド検索が良いのだが、一度に表示される数が少なくローテーション周期も長いのですぐネタ切れになる
    - SpotifyAPIを叩いて自力で母数を増やしたい

### コンセプト
- DynamoDBとAPIGatewayを自分で使ってみる
- SpotifyAPIを使ってみる

## できること
- あらかじめ保存しておいた好きなアーティスト情報から、好きそうな曲をレコメンドする
    - 「あらかじめ保存」の保存先はDynamoDB、検索する主体はLambda
    - Spotipyのartist_related_artistsで関連アーティストを検索し、直近のアルバムを返す
        - レコメンド対象になったアーティストはDynamoDBに追加され、次回の検索の種になる
            - DynamoDBに入っているアーティストは検索対象にしない
            - DynamoDBのアーティスト数は一定数を超えないようにする(コストが無限に増えないように)
                - 現在は上限5000
- EventBridgeで半日(12時間)に1回実行する
- 1回の実行結果が気に入らなかった場合に、同時出力されるURLを叩くと再実行できる
    - 再実行用URLはLambda統合したAPIGatewayのURL

### 構成図
![](https://raw.githubusercontent.com/mini-hiori/spotify-search-newsong/master/docs/architecture.png)

### 使い方
1. [この記事](https://qiita.com/shirok/items/ba5c45511498b75aac27)などを参考にSpotifyAPIを利用可能にする
2. リポジトリをduplicate,cloneなどして自分のリポジトリにする
3. [この記事](https://dev.classmethod.jp/articles/github-action-ecr-push/)を参考にGithub ActionsでECRプッシュする設定を行う
    - [前回](https://github.com/mini-hiori/lambda-rss-reader-bot)と違って今回のActionsはmasterへのpushがトリガーにしています  
    developブランチからのプルリクマージをトリガーにデプロイが走るのでこの方がいい感じ
4. Lambdaを新規作成する。コンテナイメージ利用を選択し、↑のECRのURIを指定する
5. [この記事](https://dev.startialab.blog/etc/a105)を参考に、↑のLambdaにEventbridgeによるトリガーを設定する
    - 周期は半日に1回→rate(12 hours)
6. [この記事](https://dev.classmethod.jp/articles/secure-string-with-lambda-using-parameter-store/#%E4%BB%8A%E3%81%AEwebhook-url%E3%81%AE%E6%89%B1%E3%81%84)を参考に、以下2つをSystems Managerパラメータストアに配置する
    1. 送りたいDiscord-WebhookのURL
    2. SpotifyAPIのclient id
    3. SpotifyAPIのclient secret
        - 1,3は暗号化推奨
7. 3.LambdaのロールにSSM参照権限と暗号化パラメータの複合権限、DynamoDBの書き込み権限を付与する
    - SSM参照権限→SSMReadOnlyAccessでOK
    - 複合権限はkms:Decrypt。AWS管理ポリシーに該当するものがないので自力でポリシーを作成する必要がある
        - [参考](https://qiita.com/minamijoyo/items/c6c6770f04c24a695081)
    - DynamoDB書き込みの権限は最小のものがAWS管理ポリシーにないので自力で作った方がよい
        - 面倒ならDynamoDBFullAccessでも動作に支障はない
8. [この記事](https://qiita.com/blackcat5016/items/e41f7fb8b6b7a0c9b90b)などを参考にDynamoDBを作成する
    - 最初の検索の種として最低1レコードは好きなアーティストを入れておく
    - テーブル定義はとりあえず以下。今のところ実際にはspotify_uriしか使わない

|  spotify_uri(PK)  |  name  |  craeted_date  |  unixtime  |
| ---- | ---- | ---- | ---- |
|  アーティストのSpotifyURI |  アーティスト名  |  レコード作成日  |  レコード作成日のunixtime  |

9. [この記事](https://dev.classmethod.jp/articles/api-gateway-lambda-integration-fabu/)などを参考にAPIGatewayを作成し、3.Lambdaと統合する
    - Lambdaプロキシ統合を使いたい場合はLambdaの戻り値を厳密にjsonにしないとダメ ただ今回はAPIとしてLambdaが呼べれば良いだけなので、非プロキシLambda統合でも問題ない
        - https://qiita.com/polarbear08/items/3f5b8584154931f99f43

### TODO
- DynamoDBのメンテをAPI化したい
    - レコメンドがあまり好きでない方向に行き始めた場合はDynamoDB内のアーティストを消す必要があるが、今のところ手動でやるしかない
    - 削除用Lambda+APIGatewayを別途作る？

### よくわからんポイント
