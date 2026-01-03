# SQLiteを使用したデータサイエンス100本ノック

## 概要

このディレクトリには、SQLiteを使用したCRUD（Create, Read, Update, Delete）操作の演習問題が含まれています。

## セットアップ

### Docker環境の場合

#### 1. SQLiteデータベースの作成

以下のコマンドを実行して、SQLiteデータベースを作成してください：

```bash
python3 setup_sqlite.py
```

このスクリプトは以下を実行します：
- `dsdojo.db` というSQLiteデータベースファイルを作成
- 必要なテーブル（customer, category, product, receipt, store, geocode）を作成
- CSVファイルからデータを読み込み

#### 2. データベースの確認

データベースが正しく作成されたか確認するには：

```bash
sqlite3 dsdojo.db "SELECT COUNT(*) FROM customer;"
```

### Windows環境（Dockerなし）の場合

WindowsのコマンドプロンプトでDockerを使わずに実行する手順です。

#### 前提条件

1. **Python 3のインストール**
   - [Python公式サイト](https://www.python.org/downloads/)から最新版をダウンロード
   - インストール時に「Add Python to PATH」にチェックを入れる
   - コマンドプロンプトで確認: `python --version`

2. **必要なパッケージのインストール**
   ```cmd
   pip install jupyter notebook ipython-sql sqlalchemy
   ```

#### セットアップ手順

1. **リポジトリのクローンまたはダウンロード**
   ```cmd
   git clone https://github.com/The-Japan-DataScientist-Society/100knocks-preprocess.git
   cd 100knocks-preprocess\docker\work
   ```
   
   または、GitHubからZIPをダウンロードして解凍し、`docker\work` フォルダに移動してください。

2. **SQLiteデータベースの作成**
   ```cmd
   python setup_sqlite.py
   ```
   
   実行が成功すると、以下のメッセージが表示されます：
   ```
   ✓ SQLite database created successfully: dsdojo.db
     Database size: 25.73 MB
   ```

3. **Jupyter Notebookの起動**
   ```cmd
   jupyter notebook
   ```
   
   ブラウザが自動的に開き、Jupyter Notebookの画面が表示されます。

4. **ノートブックを開く**
   - `preprocess_knock_SQLite.ipynb` をクリックして開く
   - 最初のセルを実行してSQLiteデータベースに接続
   - CRUD演習問題（C-001からC-010）を順番に解いていく

#### トラブルシューティング（Windows）

**Python が認識されない場合**
```cmd
python --version
```
が動作しない場合は、Pythonのインストールパスを環境変数PATHに追加してください。

**pip が認識されない場合**
```cmd
python -m pip install jupyter notebook ipython-sql sqlalchemy
```

**データベースファイルの場所**
```cmd
dir dsdojo.db
```
でファイルの存在を確認できます。

**データベースをリセットしたい場合**
```cmd
del dsdojo.db
python setup_sqlite.py
```

## 利用可能なノートブック

### `preprocess_knock_SQLite.ipynb`
CRUD操作の演習問題（10問）と基本的なデータ加工問題が含まれています。

**CRUD演習の内容:**
- C-001 〜 C-003: SELECT文による読み取り操作
- C-004: INSERT文によるデータ挿入
- C-005: データ挿入の確認
- C-006: UPDATE文によるデータ更新
- C-007: データ更新の確認
- C-008: COUNT関数の使用
- C-009: 複数行の一括挿入
- C-010: DELETE文によるデータ削除

### `answer/ans_preprocess_knock_SQLite.ipynb`
上記の演習問題の解答例です。

## PostgreSQLとの違い

SQLiteとPostgreSQLでは一部の構文や関数が異なります：

| 機能 | PostgreSQL | SQLite |
|------|-----------|--------|
| 日付フォーマット | `TO_CHAR(date, 'YYYY-MM-DD')` | `strftime('%Y-%m-%d', date)` |
| 日付抽出 | `EXTRACT(YEAR FROM date)` | `CAST(strftime('%Y', date) AS INTEGER)` |
| 現在日付 | `CURRENT_DATE` | `date('now')` |
| 文字列結合 | `\|\|` または `CONCAT()` | `\|\|` |
| データ型 | より厳密 | より柔軟 |

## データベースファイルの管理

- `dsdojo.db` は `.gitignore` に含まれており、Gitで管理されません
- 必要に応じて `setup_sqlite.py` を実行してデータベースを再作成できます
- データベースファイルは約25MBのサイズです

## トラブルシューティング

### Docker環境

**データベースが見つからない**

```python
# Jupyterノートブック内で実行
!python3 setup_sqlite.py
```

**データベースをリセットしたい**

既存の `dsdojo.db` ファイルを削除してから、再度 `setup_sqlite.py` を実行してください：

```bash
rm dsdojo.db
python3 setup_sqlite.py
```

### Windows環境

**Python が認識されない**
- Pythonが正しくインストールされているか確認: `python --version`
- 環境変数PATHにPythonのインストールパスが含まれているか確認
- コマンドプロンプトを再起動

**モジュールが見つからない (ModuleNotFoundError)**
```cmd
pip install jupyter notebook ipython-sql sqlalchemy
```

**データベースファイルが見つからない**
- 現在のディレクトリを確認: `cd`
- `docker\work` フォルダにいることを確認
- データベースファイルの存在を確認: `dir dsdojo.db`

**文字化けが発生する**
- コマンドプロンプトで `chcp 65001` を実行してUTF-8に設定

## 参考リンク

- [SQLite公式ドキュメント](https://www.sqlite.org/docs.html)
- [SQLite関数リファレンス](https://www.sqlite.org/lang_corefunc.html)
- [PostgreSQL vs SQLite比較](https://www.sqlite.org/different.html)
