# Agent Development Kit (ADK) と Gemini Enterprise Agent Runtime で作るシングルエージェント

### 所要時間

<walkthrough-tutorial-duration duration="90"></walkthrough-tutorial-duration>

## はじめに

このハンズオンでは、Agents CLI と Antigravity CLI を使い、Agent Development Kit (ADK) 2.0 でシングルエージェントを開発する方法を学びます。また、Gemini Enterprise Agent Runtime へのデプロイも行います。

### 目標

このハンズオンを通して、次の機能の使い方を学習できます。

- ADK 2.0 の使い方
- Gemini Enterprise Agent Runtime へのデプロイ方法
- Agents CLI の使い方
- Antigravity CLI の使い方

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

ハンズオンではスムーズに実装を進めるため、パーミッション設定をデフォルトの「レビューが必要な設定」から「自動許可の設定」に変更します。パーミッション設定は `/permission` スラッシュコマンドを実行します。

```
/permission
```

設定を `always-proceed` に変更します。

```
Active Permissions

  request-review Prompt for write, bash, and web tools
  proceed-in-sandbox  Auto-approve terminal commands in sandbox
> always-proceed (current)  Auto-approve all tools
  strict              Prompt for all non-read tools
```

以上で Antigravity CLI の初期設定は終了です。簡単なプロンプトを入力し、返答が返ってくることを確認しましょう。

```
今日の東京の天気は？
```

Antigravity CLI を終了します。スラッシュコマンド `/exit` で終了できます。

```
/exit
```

## Agents CLI のインストール

Agents CLI は Google Cloud 上で AI エージェントを構築、評価、デプロイするための CLI およびスキル パッケージです。

以下のコマンドでインストールします。

```sh
uvx google-agents-cli setup
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

Antigravity CLI を終了します。スラッシュコマンド `/exit` で終了できます。

```
/exit
```

## はじめてのシンプルエージェントの作成

### シンプルエージェントの作成

インストールした Agents CLI のスキルを使って、Antigravity CLI でシンプルな AI エージェントを作成してみましょう。

まずはディレクトリを作成し、ディレクトリに移動します。

```sh
mkdir weather-agent && cd weather-agent
```

次のコマンドで Antigravity CLI を起動します。前のステップで起動した状態の場合、この手順はスキップします。

```sh
agy
```

次のプロンプトで、シンプルエージェントの作成を開始します。

```
agents-cli を使って、地域の天気を調べるエージェントを作成します。ADK のバージョンは 2.0 で作成します。天気の取得には Google Maps Platform の Weather API  を使用します。
```

Antigravity CLI がエージェントの作成を進めます。下記のように各コマンドの実行許可が求められる場合があるので、問題がなければ `3` を選択します。

```
Do you want to proceed?
  1. Yes
  2. Yes, and always allow in this conversation for commands that start with 'mv'
> 3. Yes, and always allow for commands that start with 'mv' (Persist to settings.json)
  4. No
```

Antigravity CLI が自律的にコーディング・テスト・修正を行います。一通りの作業が完了するまで数分かかります。

完了したら、Antigravity CLI を終了します。

### エージェントの実行

作成したエージェントを実行してみましょう。

まずはじめに、エージェントが使用する Gemini API の設定を行う必要があります。次のコマンドで環境設定ファイルを作成します。

```sh
vim .env
```

`.env` の内容は、次のようにします。`<YOUR_GOOGLE_CLOUD_PROJECT>` は <walkthrough-project-id/> に書き換えます。

```
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=<YOUR_GOOGLE_CLOUD_PROJECT>
GOOGLE_CLOUD_LOCATION=global
```

次のコマンドで、ローカルでプレイグラインド環境を立ち上げます。

```sh
agents-cli playground
```

`agents-cli: command not found` と出てしまう場合は、Cloud Shell を再起動するか、次のコマンドを実行してください。

```sh
export PATH="/home/<Google アカウント名>/.local/bin:$PATH"
```

数秒後、下記のような結果が表示されていれば、起動できています。

```
+-----------------------------------------------------------------------------+
| ADK Web Server started                                                      |
|                                                                             |
| For local testing, access at http://127.0.0.1:8080.                         |
+-----------------------------------------------------------------------------+

INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
```

`http://127.0.0.1:8080` で立ち上がります。Web プレビューボタン <walkthrough-web-preview-icon></walkthrough-web-preview-icon> のアイコンをクリックし、メニューから「ポート 8080 でプレビュー」を選びます。

アプリケーションを検証するには `Select an App` から `app` を選択します。

実際の地域を入力し、動作を検証してみましょう。Weather API は日本は未サポートのため「ニューヨークの天気は？」や「ラスベガスの天気は？」などと質問してみましょう。

## エージェントのソースコードの確認

作成したエージェントがどのような実装になっているか確認してみましょう。

<walkthrough-cloud-shell-editor-icon></walkthrough-cloud-shell-editor-icon> のアイコンをクリックすると、Cloud Shell Editor (Code OSS ベースのエディタ) を開くことができます。

`weather-agent` のファイル構成は次のようになっていると思います。

```
.
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── agent_runtime_app.py
│   └── app_utils/
│     ├── telemetry.py
│     └── typing.py
├── tests/
├── agents-cli-manifest.yaml
├── GEMINI.md
├── pyproject.toml
├── README.md
└── uv.lock
```

エージェントの振る舞いを左右する、最も重要なファイルは `agent.py` です。`agent.py` を開いてみましょう。

現在の天気はエージェント単体では取得できないため、ツールとして使うための関数が作成されます。本ハンズオンでは関数名などの指定をプロンプトで行なっていないため、Antigravity CLI が必要と思われる関数を判断し作成します。例えば `get_current_weather` や `get_daily_forecast`、`get_hourly_forecast` などのような関数が定義され、エージェントの定義では次のようにツールが指定されます(実際にどのようなコードが作成されるかは Antigravity CLI の実装次第となります)。

```python
root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="You are a helpful AI assistant designed to provide accurate and useful weather information.",
    tools=[get_current_weather, get_daily_forecast, get_hourly_forecast],
)

app = App(
    root_agent=root_agent,
    name="app",
)
```

`Agent` でルートエージェントを定義しています。設定としては `instruction` にどのような役割を持つのかプロンプトを設定し、`tools` には事前に定義してある関数をツールとして指定しています。

## エージェントのデプロイ

作成したエージェントをデプロイします。Antigravity CLI を立ち上げ (`agy`)、次のプロンプトを入力します。

```
agents-cli を使って Agent Runtime にデプロイしてください。
```

テストの再実行、Agent Runtime への対応、デプロイが行われます。この処理が完了するまでは数分かかります。

デプロイが無事完了すると、次のような結果が表示されます。

```
• プロジェクト ID:  <YOUR_PROJECT_ID>
• デプロイ地域 (Location):  us-east1 
• Agent Runtime ID:  projects/<YOUR_PROJECT_NUMBER>/locations/us-east1/reasoningEngines/<ID> 
• サービスアカウント:  service-<YOUR_PROJECT_NUMBER>@gcp-sa-aiplatform-re.iam.gserviceaccount.com 
• Vertex AI Console プレイグラウンド:
  Vertex AI Console - Playground https://console.cloud.google.com/vertex-ai/agents/agent-engines/locations/us-east1/agent-engines/<ID>/playground?project=<YOUR_PROJECT_ID>
```

新しいタブで、Gemini Enterprise Agent Runtime のコンソールを開きます。

https://console.cloud.google.com/agent-platform/runtimes

一覧から `weather-agent` をクリックし `プレイグラウンド` タブに切り替えます。ローカルで立ち上げたプレイグラウンド環境と同様に、エージェントの動作の検証が行えます。

## おまけ : Managed Agents API でシングルエージェントを実行する

Managed Agents は API の呼び出しだけでフルマネージド環境でエージェントを起動・実行できるサービスです。シンプルなエージェントであれば、Managed Agents API を呼び出すだけでエージェントが実行できます。

### Antigravity エージェントの呼び出し

Antigravity エージェントは、デフォルトで用意されている Google ファーストパーティ エージェントです。カスタム エージェント リソースを作成する必要なく、1 回の API 呼び出しのみで実行できます。

次のコマンドを実行してみましょう。`<YOUR_PROJECT_ID>` は <walkthrough-project-id/> に置き換えます。

```
curl -X POST "https://aiplatform.googleapis.com/v1beta1/projects/<YOUR_PROJECT_ID>/locations/global/interactions" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Api-Revision: 2026-05-20" \
-d '{"stream": true, "background": true, "store": true, "agent": "antigravity-preview-05-2026", "environment": {"type": "remote"}, "tools": [{"type": "google_search"}], "input": [{"type": "user_input", "content": [{"type": "text", "text": "今日のニュースを教えて"}]}]}'
```

Google 検索で見つかるような、最新のニュースが取得できるはずです。

### カスタムエージェントの作成と呼び出し

次に、カスタムエージェントを作成し、呼び出してみましょう。

まずは次のコマンドでカスタムエージェントを作成します。`<YOUR_PROJECT_ID>` は <walkthrough-project-id/> に置き換えます。

```
curl -X POST "https://aiplatform.googleapis.com/v1beta1/projects/<YOUR_PROJECT_ID>/locations/global/agents" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -d '{"id": "news-agent", "base_agent": "antigravity-preview-05-2026", "description": "最新のニュースを分かりやすくサマリーするエージェントです。", "system_instruction": "google_search　を使って最新のニュースを調べ、わかりやすくサマリーします。", "tools": [{"type": "google_search"}]}'
```

作成後は、指定した `id` で呼び出すことができます。次のコマンドを実行します。`<YOUR_PROJECT_ID>` は <walkthrough-project-id/> に置き換えます。

```
curl -X POST "https://aiplatform.googleapis.com/v1beta1/projects/<YOUR_PROJECT_ID>/locations/global/interactions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Api-Revision: 2026-05-20" \
  -d '{"stream": true, "background": true, "store": true, "agent": "news-agent", "input": [{"type": "user_input", "content": [{"type": "text", "text": "今日のニュースを教えて"}]}], "environment": {"type": "remote"}}'
```

Antigravity エージェントと同様、最新のニュースが取得できるはずです。

## お疲れ様でした！

以上でシンプルエージェントの作成方法を学ぶハンズオンは終了です。お疲れ様でした！

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>