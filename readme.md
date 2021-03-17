## serverless-apiでspotifyのレコメンド検索強化版(自分用)
- Spotifyのレコメンド検索が良いのだが、一度に表示される数が少なくローテーション周期も長いのですぐネタ切れになる
    - SpotifyAPIを叩いて自力で母数を増やしたい

### コンセプト
- DynamoDBとAPIGatewayを自分で使ってみる
- SpotifyAPIを使ってみる

## やりたいこと
- あらかじめ保存しておいた好きな曲やアーティスト情報からSpotifyAPIで関連する曲やアーティストを検索する
    - 「あらかじめ保存」の保存先はSystems Manager、検索する主体はLambda
    - Spotipyのartist_related_artistsで関連アーティストを検索する
        - 曲をレコメンドするときはtop trackか直近のアルバムを返す
- 同じ結果を検索しないように、直近の検索結果をDynamoDBに保存する
    - TTL機能を利用してしばらくしたら消す
- 定期実行も行うが、APIを叩いて任意実行できるようにもする
    - LambdaをAPIGatewayと統合することで実現
    - 検索対象がアーティストか曲かでエンドポイントを分ける？

### 構成図
![](https://raw.githubusercontent.com/mini-hiori/spotify-search-newsong/master/docs/architecture.png)
### 使い方

### TODO

### よくわからんポイント
