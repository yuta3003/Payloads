# Fuzzing
- [Shats's Fuzzing](#what's-fuzzing)
    - [Observation target](#observation-target)

## What's Fuzzing.
ファジングとはテスト対象に不具合が起きそうなデータを次々と送りつけその応答を観察することでバグや脆弱性を発見すること。  

ファジングの特徴は以下の3点
1. テスト対象の内部構造を知る必要がない
1. 応用範囲が広い
1. 段階的な攻撃を検出できない

### Observation target
#### 終了ステータスの番号とその説明

|番号|説明|
|---|---|
|1|一般的なエラー|
|2|コマンドの誤用|
|126|コマンドを実行できなかった|
|127|コマンドが見つからなかった|
|128|シグナルによって終了した|

#### シグナル番号とその説明

|シグナル名|番号|説明|
|---|:-:|---|
|SIGILL|4|不正な命令|
|SIGBUS|7|パスエラー(不正なメモリアクセス)|
|SIGFPE|8|不正な浮動小数点の演算|
|SIGSEGV|11|不正なメモリの参照|
|SIGSYS|31|不正なルーチンへの引数|
