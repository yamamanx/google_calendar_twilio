# Google Calendar Twilio Call

Googleカレンダーの予定をX時間前にTwilioで電話します。

Googleアカウントと電話する連絡先はkintoneで管理します。


## kintoneアプリの作成

以下の項目を持つアプリを作成します。

フィールド名|フィールドコード|タイプ|内容
:--|:--|:--|:--
メールアドレ|calendar＿id|文字列(1行)|Googleアカウントのメールアドレス
電話番号|tel_number|文字列(1行)|Twilioからかかってくる先の電話番号
無効|invalid|チェックボックス|選択項目は「無効」のみ

※「無効」は設定を無効にするための項目です。レコード削除でも同じですが。


## AWS Lambda

ソースコードをダウンロードして、requirements.txtに記載のパッケージをソースコードと同じフォルダにインストールしてzipで固めて、Lambdaにアップロードします。


## AWS Lambdaに設定する環境変数


変数名|設定値
:--|:--
TIME_LAG|予定を何時間前に通知するかを設定します
TIME_ZONE|Asia/Tokyoなど
BUCKET_NAME|Amazon Pollyが生成するMP3ファイルを格納するS3バケット名
BUCKET_REGION|ap-northeast-1など S3バケットがあるリージョン名
VOICE_ID|Amazon PollyのボイスID 日本語なので Mizuki
POLLY_REGION|Amazon Pollyのリージョン名
KINTONE_DOMAIN|kintoneのドメイン xxx.cybozu.com
KINTONE_APP|kintoneのアプリの数字
KINTONE_HEADERS_KEY|X-Cybozu-API-Token
KINTONE_API_KEY|kintoneのAPIキー
KINTONE_BASIC_HEADERS_VALUE|kintoneベーシック認証のキー(Basic)で始まる
DOMAIN|Googleのドメイン GSuiteは独自ドメイン、フリーアカウントはgmail.com
GOOGLE_SERVICE_ACCOUNT_ID|GoogleのサービスアカウントID
TWILIO_ACCOUNT_SID|TwilioのアカウントSID
