# Avro 形式について

- https://docs.oracle.com/cd/E35584_01/html/GettingStartedGuide/avroschemas.html

## OSS：Apache Avro

Avro API は、Apache ソフトウェア財団が提供するオープン・ソース・プロジェクトとして開発されました。公式サイトはhttp://avro.apache.orgです。

## メリット

Avro スキーマを使用すると，シリアライズされた値を領域効率に非常に優れたバイナリ形式で格納できる．格納される各値は，サイズの小さい内部スキーマ識別子(1 から 4 バイト)以外のメタデータを持たない．このような参照情報がキーと値のペアごとに格納される．

このように，シリアライズされた Avro データ形式は，常に最小限のオーバーヘッドで，そのシリアライズに使用したスキーマに関連付けられる．この関連付けはアプリケーションに対して透過的に行われ，内部スキーマ識別子は AvroCatalog クラスの提供するバインディングによって管理される．アプリケーションが内部識別子を直接参照したり，使用することはない．

## Avro スキーマ

Avro スキーマは JSON 形式で作成する．

JSON (JavaScript Object Notation の略)は，人が簡単に読み書きできることを目的とした，軽量でテキストベースのデータ交換形式である．JSON については様々な場所(Web や市販の書籍)で解説されている．ただし，公式の解説は，IETF の RFC 4627 (http://www.ietf.org/rfc/rfc4627.txt?number=4627)を参照．

### Avro スキーマの例

Avro スキーマを記述するには，次のように，スキーマを指定する JSON レコードを作成する．

```json
{
  "type": "record",
  "namespace": "com.example",
  "name": "FullName",
  "fields": [
    { "name": "first", "type": "string" },
    { "name": "last", "type": "string" }
  ]
}
```

前述の例は，ストア内の「キーと値のペアの値部分」で使用されるスキーマを指定した JSON レコードを示している．人の姓名のスキーマが指定されている．

このレコードには次の 4 つのフィールドがあることに注意．

- `type`
  - JSON フィールドの型を指定する．Avro スキーマでは，スキーマの最上位で指定する場合は必ず `record` とする必要がある．`record` 型は，複数のフィールドが定義されることを示す．
- `namespace`
  - オブジェクトが存在する名前空間を指定する．基本的には，ユーザーや組織にとって意味のある URI にする．同じ名前を複数のスキーマ型で共有する可能性がある場合に，それぞれを区別するために使用する．
- `name`
  - これはスキーマ名で，名前空間と組み合せた場合に，ストア内でスキーマを一意に識別する．前述の例で，スキーマの完全修飾名は `com.example.FullName` である．
- `fields`
  - これが実際のスキーマ定義の部分．値に含まれるフィールドの種類と各フィールドのデータ型を定義する．フィールドには，整数や文字列などの単純なデータ型や複合データ型を指定できる．これについては，後述する．
  - スキーマのフィールド名は，[A-Za-z_]で始まり、続いて[A-Za-z0-9_]のみを使用する必要があることに注意してください。

スキーマを使用するには，スキーマをフラット・テキスト・ファイルに定義してから，適切なコマンドライン呼出しを使用してストアに追加する必要がある．また，なんらかの形でユーザーのコードにも提供する必要がある．コードで使用しているスキーマは，ストアに追加されたスキーマと一致する必要がある．

この章の残りの部分で，スキーマおよびそれをストアに追加する方法について説明する．スキーマをコードで使用する方法（Python など）の詳細は，「Avro バインディング」を参照．

### Avro スキーマ定義

Avro スキーマ定義は JSON レコードである．レコードなので，JSON 配列に編成された複数のフィールドで定義できる．この各フィールドでは，フィールド名とフィールド型を指定する．フィールド型には，整数のような単純なものや，別のレコードのような複雑なものを設定できる．

例えば、次の簡単な Avro スキーマ定義は，人の年齢のみを含む値に使用できる．

```json
{
  "type": "record",
  "name": "userInfo",
  "namespace": "my.example",
  "fields": [{ "name": "age", "type": "int" }]
}
```

データ格納の要件がこのように単純な場合は，整数を単なるバイト配列でストアに格納することもできる(ただし，これはベスト・プラクティスではない)．

前述の例で，単一フィールドのスキーマを定義している場合でも，スキーマ定義の最上位の型は `record` 型であることに注意．Oracle NoSQL Database では，必要なフィールドが 1 つのみでも，最上位の型には `record` を使用する必要がある．

また，スキーマのフィールドにはデフォルト値を定義しておくことを推奨する．これは，オプションだが，スキーマを変更する可能性がある場合は，そうすることで様々な問題を回避できる．デフォルト値を定義するには，`default` 属性を使用する．

```json
{
  "type": "record",
  "name": "userInfo",
  "namespace": "my.example",
  "fields": [{ "name": "age", "type": "int", "default": -1 }]
}
```

単一フィールドの定義を使用することはほとんどない．複数のフィールドを追加するには，`fields` フィールドに配列を指定する．次に例を示す．

```json
{
  "type": "record",
  "name": "userInfo",
  "namespace": "my.example",
  "fields": [
    { "name": "username", "type": "string", "default": "NONE" },

    { "name": "age", "type": "int", "default": -1 },

    { "name": "phone", "type": "string", "default": "NONE" },

    { "name": "housenum", "type": "string", "default": "NONE" },

    { "name": "street", "type": "string", "default": "NONE" },

    { "name": "city", "type": "string", "default": "NONE" },

    { "name": "state_province", "type": "string", "default": "NONE" },

    { "name": "country", "type": "string", "default": "NONE" },

    { "name": "zip", "type": "string", "default": "NONE" }
  ]
}
```

前述のスキーマ定義には様々な情報が含まれている．以下のように，単純だが，埋込みレコードを使用すれば，さらに構造を追加できる．

```json
{
  "type": "record",
  "name": "userInfo",
  "namespace": "my.example",
  "fields": [
    { "name": "username", "type": "string", "default": "NONE" },

    { "name": "age", "type": "int", "default": -1 },

    { "name": "phone", "type": "string", "default": "NONE" },

    { "name": "housenum", "type": "string", "default": "NONE" },

    {
      "name": "address",
      "type": {
        "type": "record",
        "name": "mailing_address",
        "fields": [
          { "name": "street", "type": "string", "default": "NONE" },

          { "name": "city", "type": "string", "default": "NONE" },

          { "name": "state_prov", "type": "string", "default": "NONE" },

          { "name": "country", "type": "string", "default": "NONE" },

          { "name": "zip", "type": "string", "default": "NONE" }
        ]
      }
    }
  ]
}
```

#### 注意

必要なレコード定義がストア全体で 1 つのみという状況は考えにくい．通常は，複数の種類のレコードを使用することになる．これに対処するには，各レコード定義をそれぞれ別のファイルに設定する．その後で，各レコード定義を処理するコードを記述する必要がある．その方法については，この章の後半で説明する．

### データ型

#### プリミティブ・データ型

前述の Avro スキーマの例では，文字列と整数のみを示した．次に，Avro でサポートされているプリミティブ型の完全なリストを示します。

- `null`

  - 値なし

- `boolean`
  - バイナリ値
- `int`

  - 32 ビットの符号付き整数

- `long`

  - 64 ビットの符号付き整数

- `float`

  - IEEE 754 単精度(32 ビット)浮動小数点数

- `double`

  - IEEE 754 倍精度(64 ビット)浮動小数点数

- `bytes`

  - 8 ビット符号なしバイトのシーケンス

- `string`
  - Unicode 文字のシーケンス

これらのプリミティブ型には固有の属性がない．プリミティブ型の名前は，型名の定義でもある．例えば，スキーマ `string` は，次と同等．

```json
{ "type": "string" }
```

#### 複合データ型

前の項で説明したプリミティブ・データ型の他に、Avro では 6 つの複合データ型(`Record`、`Enum`、`Array`、`Map`、`Union` および `Fixed`)をサポートしています。これらについてはこの項で説明します。

- `record`
  - レコードは属性がカプセル化されたもので、すべてを組み合せて 1 つのものを表します。Avro レコードでサポートしている属性は次のとおりです。
    - `name`
      - レコードの名前(必須)。レコードの内容を識別することを目的としています。たとえば、PersonInformation、Automobiles、Hats、BankDeposit などです。
      - レコード名は[A-Za-z_]で始まり、続いて[A-Za-z0-9_]のみを使用する必要があることに注意してください。
    - `namespace`
      - 名前空間はオプションの属性で，レコードを一意に識別する．オプションだが、レコードの名前が他のレコードの名前と競合する可能性がある場合は使用する必要があります。たとえば、従業員に関するレコードを例に考えてみましょう。従業員には様々な種別(正社員、パートタイム従業員、契約社員)があるとします。その場合は、名前 EmployeeInfo に、FullTime、PartTime および Contractor という名前空間を組み合せれば、3 つのレコード型すべてを作成できます。つまり、正社員を示すレコードの完全修飾名は、FullTime.EmployeeInfo になります。
      - また、ストアに様々な組織の情報が含まれている場合は、レコードで使用されている組織を識別する名前空間を使用して、レコード名の競合を回避できます。この場合、完全修飾レコードの名前は、My.Company.Manufacturing.EmployeeInfo や My.Company.Sales.EmployeeInfo のようになります。
    - `doc`
      - この属性(オプション)は、単にレコードに関するドキュメントを表します。これを解析してスキーマとともに格納すれば、Avro API を使用してスキーマ・オブジェクトから利用できますが、シリアライズでは使用されません。
    - `aliases`
      - この属性(オプション)は JSON 配列の文字列で、レコードの代替名を表します。JSON スキーマは名前変更の操作に対応していないので注意してください。最初に name 属性で定義した名前以外を使用してスキーマを参照する場合は、別名を使用してください。
    - `type`
      - 必須属性で、キーワード record または埋込みの JSON スキーマ定義のいずれかです。最上位のスキーマ定義に対する属性の場合は、record を使用する必要があります。
    - `fields`
      - JSON 配列を表す必須属性で、スキーマ内のすべてのフィールドを一覧で示します。各フィールドに name 属性と type 属性が必要です。また、doc、order、aliases および default 属性が指定されることがあります。
      - name、type、doc および aliases 属性の使用方法は、この項の前半で説明した方法とまったく同じです。
      - レコード名と同様に、フィールド名は[A-Za-z_]で始まり、続いて[A-Za-z0-9_]のみを使用する必要があります。
      - order 属性はオプションで、Oracle NoSQL Database では無視されます。この属性を使用するアプリケーション(Oracle NoSQL Database 以外)では、このフィールドで定義する当該レコードのソート順は、この属性で示します。有効な値は、ascending、descending または ignore です。この機能の詳細は、http://http://avro.apache.org/docs/current/spec.html#orderを参照してください。
      - default 属性はオプションですが、スキーマ展開をサポートするためには強くお薦めします。それはスキーマ展開のみを目的として、使用されるフィールドにデフォルト値を設定します。default 属性を使用しても、値オブジェクトの新規作成時にフィールドの初期化に失敗することはありません。default 属性の有無にかかわらず、すべてのフィールドを初期化する必要があります。
      - スキーマ展開については、「スキーマ展開」で説明します。
      - default 属性で使用できる値は、フィールドの型によって異なります。ユニオン型のデフォルト値は、ユニオンの最初のフィールドに依存します。バイト型および固定型フィールドのデフォルト値は JSON 文字列です。

---

- Enum
  - Enum は列挙型で、次の属性をサポートします。
    - name
      列挙の名前を指定する必須属性。この名前は[A-Za-z_]で始まり、続いて[A-Za-z0-9_]のみを使用する必要があります。
    - namespace
      - 列挙の name 属性を修飾する属性(オプション)。
    - aliases
      - 列挙の代替名の JSON 配列を表す属性(オプション)。
    - doc
      - 列挙のコメント文字列を表す属性(オプション)。
    - symbols
      - 列挙のシンボルを名前の配列として表す必須属性。これらのシンボルは[A-Za-z_]で始まり、続いて[A-Za-z0-9_]のみを使用する必要があります。

Enum の例を示す：

```json
{
  "type": "enum",
  "name": "Colors",
  "namespace": "palette",
  "doc": "Colors supported by the palette.",
  "symbols": ["WHITE", "BLUE", "GREEN", "RED", "BLACK"]
}
```

---

- Array
  - 配列フィールドを定義します。items 属性(必須)のみをサポートします。items 属性では、配列内の項目の型を指定します。

```json
{ "type": "array", "items": "string" }
```

---

- Map
  - マップとは、データをキーと値のペアに編成する結合配列またはディクショナリです。Avro マップのキーは文字列にする必要があります。Avro マップでサポートしている属性は values のみです。この属性は必須で、マップの値部分の型を定義します。

```json
{ "type": "map", "values": "int" }
```

---

- Union
  - ユニオンは、フィールドが複数の型を持つ可能性を示す場合に使用します。JSON 配列で表します。

たとえば、文字列または NULL のフィールドがあるとします。その場合、ユニオンは次のように表します。

```json
["string", "null"]
```

使用方法は次のとおりです。

```json
{
  "type": "record",
  "namespace": "com.example",
  "name": "FullName",
  "fields": [
    { "name": "first", "type": ["string", "null"] },
    { "name": "last", "type": "string", "default": "Doe" }
  ]
}
```

---

- Fixed
  - 固定型は、バイナリ・データの格納に使用できる固定サイズ・フィールドを宣言する場合に使用します。2 つの必須属性(フィールドの名前とバイト数で表したサイズ)があります。

たとえば、サイズが 1KB の固定フィールドを定義するには、次のようにします。

```json
{ "type": "fixed", "name": "bdata", "size": 1048576 }
```
