# Agent Development Kit (ADK) で作るさまざまな AI エージェントデザインパターン

## はじめに

このハンズオンでは、Agents CLI と Antigravity CLI を使い、さまざまな AI エージェントのデザインパターンを、実際に Agent Development Kit (ADK) 2.0 を使って構築しながら学びます。

### 目標

このハンズオンを通して、次のような事項を学習できます。

- ADK 2.0 の使い方
- Agents CLI の使い方
- Antigravity CLI の使い方
- さまざまな AI エージェントデザインパターンの理解

### 所要時間

<walkthrough-tutorial-duration duration="90"></walkthrough-tutorial-duration>

## Google Cloud Project のセットアップ

まずはじめに、コマンドで使用する Google Cloud Project の指定や使用するサービスの API の有効化を行います。

次のコマンドで、Google Cloud Project を設定します。

```sh
gcloud config set project $GOOGLE_CLOUD_PROJECT
```

次のコマンドで、使用するサービスの API の有効化を行います。

```sh
gcloud services enable aiplatform.googleapis.com weather.googleapis.com
```

## Antigravity CLI のインストール

AI エージェントのプロジェクトは Antigravity CLI を使って行うため、以下のコマンドでインストールします。

Antigravity CLI を使うことで、ターミナルからビルド、デバッグ、デプロイが可能です。タスクを自然言語で記述するだけで、あとは Antigravity がすべて処理します。

```sh
curl -fsSL https://antigravity.google/cli/install.sh | bash
```

次のコマンドが実行できれば、インストールが問題なく完了しています。

```sh
agy --version
```

## Antigravity CLI のセットアップ

Antigravity CLI のセットアップを始めます。次のコマンドを実行します。

```sh
agy
```

まずログイン方法を選択します。`Use a Google Cloud project` を選択します。

```
Welcome to the Antigravity CLI. You are currently not signed in.

 Select login method:
   1. Google OAuth
 > 2. Use a Google Cloud project

 [Use arrow keys to navigate, Enter to select]
```

認証用の URL が表示されます。URL をコピーし、ブラウザで新しいタブを開き、コピーした URL にアクセスします。

```
 Open the URL below in your browser:
 ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 https://accounts.google.com/o/oauth2/auth?...
 ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
```

認証を進めると、最後に認証コードが表示されるのでコピーします。Antigravity CLI の入力欄にペーストします。

```
After authenticating, copy the code displayed in the browser and paste it below:

 authorization code...
```

次に Google Cloud Project ID が求められるので <walkthrough-project-id/> を入力します。

```
 Enter Google Cloud Project ID:
 project id...
```

次にロケーションの選択が求められるので、デフォルトのまま `global` を選択します。

```
Select Google Cloud Location:
 > global
   us
   eu
```

次にカラースキームの選択が求められるので、好きなカラースキームを選択します。

```
Choose your color scheme:
  > terminal
    light
    solarized light
    colorblind-friendly light
    dark
    solarized dark
    colorblind-friendly dark
    tokyo night
```

次に利用規約の同意が求められるので、そのまま Enter を押下します。

```
Terms and Privacy:
  - Terms of Service: https://cloud.google.com/terms
  - Privacy Notice (excluding product analytics data): https://cloud.google.com/terms/cloud-privacy-notice
```

次に、Antigravity CLI へのディレクトリへのアクセス許可を与えます。`Yes, I trust this folder` を選択します。

```
Antigravity CLI requires permission to read, edit, and execute files here.
> Yes, I trust this folder
  No, exit
```

以上で Antigravity CLI の初期設定は終了です。簡単なプロンプトを入力し、返答が返ってくることを確認しましょう。

```
今日の東京の天気は？
```

Antigravity CLI を終了するには `Ctrl` + `D` を 2 回押します。

## Agents CLI のインストール

Agents CLI は Google Cloud 上で AI エージェントを構築、評価、デプロイするための CLI およびスキル パッケージです。

以下のコマンドでインストールします。

```sh
pip install google-agents-cli && agents-cli setup
```

Antigravity CLI で Agents CLI のスキルが使えるようになっているか確認しましょう。

次のコマンドで Antigravity CLI を起動します。

```sh
agy
```

スラッシュコマンドでスキル一覧が確認できます。

```sh
/skills
```

次のように、Agents CLI のスキルが表示されれば無事インストールが成功しています。

```
Workspace skills · Workspace config
  google-agents-cli-adk-code: This skill should be used when the user wants to "write agent code", "build an agent with ADK", "add a tool", "create a callback", "define an ...
  google-agents-cli-deploy: This skill should be used when the user wants to "deploy an agent", "deploy my ADK agent", "set up CI/CD", "configure secrets", "troubleshoot a ...
  google-agents-cli-eval: This skill should be used when the user wants to "run an evaluation", "evaluate my ADK agent", "write an evalset", "debug eval scores", "compare e...
  google-agents-cli-observability: This skill should be used when the user wants to "set up tracing", "monitor my ADK agent", "configure logging", "add observability", "deb...
  google-agents-cli-publish: This skill should be used when the user wants to "publish an agent", "publish my ADK agent", "register an agent with Gemini Enterprise", "publi...
  google-agents-cli-scaffold: This skill should be used when the user wants to "create an agent project", "start a new ADK project", "build me a new agent", "add CI/CD to m...
  google-agents-cli-workflow: This skill should be used when the user wants to "develop an agent", "build an agent using ADK", "run the agent locally", "debug agent code", ...
```

## お疲れ様でした！

以上で AI エージェントのデザインパターンを学ぶハンズオンは終了です。お疲れ様でした！

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>