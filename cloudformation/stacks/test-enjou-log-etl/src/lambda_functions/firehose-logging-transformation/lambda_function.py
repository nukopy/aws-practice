import base64
import zlib
import json
import logging
from logging import raiseExceptions
from typing import Any, Callable, Dict, List


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def func_logger(func: Callable):
    def _inner(event, context):
        # logger.info("===== Start function =====")
        # logger.info(f"Recieved event: {json.dumps(event, indent=2)}")
        print("===== Start function =====")
        print("Recieved event:\n", json.dumps(event))
        print(event)
        res = func(event, context)
        print("===== End function =====")

        return res

    return _inner


def load_json(path) -> List[List[str]]:
    with open(path, mode="r", encoding="utf-8") as f:
        obj = json.load(f)
        return obj


def str_to_bytes(string: str) -> bytes:
    string_bytes = string.encode("utf-8")
    return string_bytes


def bytes_to_str(data_bytes: bytes) -> str:
    return data_bytes.decode("utf-8")


def bytes_to_b64bytes(string_bytes: bytes) -> bytes:
    b64bytes = base64.b64encode(string_bytes)
    return b64bytes


def b64bytes_to_b64str(b64bytes: bytes) -> str:
    b64str = b64bytes.decode("utf-8")
    return b64str


def str_to_b64str(string: str) -> str:
    string_bytes: bytes = str_to_bytes(string)
    b64bytes: bytes = bytes_to_b64bytes(string_bytes)
    b64str: str = b64bytes_to_b64str(b64bytes)

    return b64str


def decode_b64str(b64str: str) -> bytes:
    return base64.b64decode(b64str)


def decompress_gzip_bytes(gzip_bytes: bytes) -> bytes:
    # gzip で圧縮されている文字列を解凍
    gzip_bytes = zlib.decompress(gzip_bytes, 16 + zlib.MAX_WBITS)
    return gzip_bytes


def b64jsonstr_to_dict(b64str: str) -> Dict[str, Any]:
    gzip_json_bytes: bytes = decode_b64str(b64str)
    # TODO: なんで gzip で渡されてくるか原因調べる
    # CloudWatch Logs -> Firehose の間で gzip 圧縮が入る
    json_bytes: bytes = decompress_gzip_bytes(gzip_json_bytes)
    json_str: str = bytes_to_str(json_bytes)
    return json.loads(json_str)


def extract_logEvents(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    return data["logEvents"]


def clean_logEvent(logEvent: Dict[str, Any]) -> Dict[str, Any]:
    # logEvent のメタデータを除去し，タイムスタンプ，ログメッセージのみにする
    return {
        "timestamp": logEvent["timestamp"],
        "message": logEvent["message"],
    }


def filter_logEvents(logEvents: Dict[str, Any]) -> List[Dict[str, Any]]:
    filtered_logEvents = []
    for logEvent in logEvents:
        # JSON 形式のログのみ抽出
        # -2 は末尾の "\n" を除いている
        if logEvent["message"][0] == "{" and logEvent["message"][-2] == "}":
            cleaned_logEvent = clean_logEvent(logEvent)
            filtered_logEvents.append(cleaned_logEvent)

    return filtered_logEvents


def convert_logEvents_to_json_str(logEvents: Dict[str, Any]) -> str:
    json_str = "\n".join([json.dumps(logEvent) for logEvent in logEvents])
    return json_str + "\n"  # for JSON line log


def convert_data_to_base64str(data: Dict[str, Any]) -> str:
    # data から logEvents のみを抽出し，base64 文字列に変換する
    logEvents: List[Dict[str, Any]] = extract_logEvents(data)
    filtered_logEvents: List[Dict[str, Any]] = filter_logEvents(logEvents)
    logEvents_json_str = convert_logEvents_to_json_str(filtered_logEvents)
    data_base64: str = str_to_b64str(logEvents_json_str)

    return data_base64


def create_payload(record) -> Dict[str, Any]:
    record_id = record["recordId"]
    ts = record["approximateArrivalTimestamp"]
    b64_data: str = record["data"]
    data = b64jsonstr_to_dict(b64_data)

    return {
        "recordId": record_id,
        "timestamp": ts,
        "data": convert_data_to_base64str(data),
        "result": "Ok",  # MUST
    }


@func_logger
def lambda_handler(event, context):
    # process event
    records = event["records"]
    payloads = []

    for rec in records:
        payload = create_payload(rec)
        payloads.append(payload)

    response = {"records": payloads}
    print("Response:\n", json.dumps(response))

    return response


if __name__ == "__main__":
    # test
    event = load_json("./event.json")
    res = lambda_handler(event, {})
