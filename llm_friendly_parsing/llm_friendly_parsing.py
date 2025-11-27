import json,os
import re
from typing import Any, Dict, List


def parse_numeric_field(value: str):
    """
    "53(71)" 같은 형태를 자동 분리하여 (53, 71)로 변환하고
    숫자 또는 None을 반환한다.
    """
    if value is None:
        return None
    
    value = value.strip()
    
    # 비어 있으면 None
    if value == "" or value.lower() in ["none", "null"]:
        return None

    # "53(71)" 같은 패턴
    pattern = r"(\d+)\((\d+)\)"
    match = re.match(pattern, value)
    if match:
        return {
            "value": int(match.group(1)),
            "raw_total": int(match.group(2))
        }

    # 숫자만 있는 경우
    if value.isdigit():
        return int(value)

    # float
    try:
        return float(value)
    except:
        return value  # 숫자가 아니면 원본 반환


def format_key(key: str) -> str:
    """
    키 이름을 사람이 읽기 쉬운 형태로 변환.
    예: "졸능_구분" → "졸업능력평가 구분"
    """
    key = key.replace("_", " ").replace("-", " ")
    return key


def flatten_json(json_obj: Dict[str, Any], parent_key=""):
    """
    nested JSON을 평탄화해서 dict로 변환
    """
    items = {}

    for key, value in json_obj.items():
        new_key = f"{parent_key}.{key}" if parent_key else key

        if isinstance(value, dict):
            items.update(flatten_json(value, new_key))
        else:
            items[new_key] = value

    return items


def generate_llm_friendly_text(data: Dict[str, Any]) -> str:
    text_output = []

    # 개인정보
    if "개인정보" in data:
        text_output.append("[개인 정보]")
        personal = flatten_json(data["개인정보"])
        for key, value in personal.items():
            label = format_key(key.split(".")[-1])
            text_output.append(f"- {label}: {value}")
        text_output.append("")

    # 졸업 기준 / 취득
    if "졸업판정" in data:
        criteria = data["졸업판정"].get("기준", {})
        status = data["졸업판정"].get("취득", {})

        text_output.append("[졸업 기준]")
        for key, value in criteria.items():
            label = format_key(key)
            parsed = parse_numeric_field(value)
            text_output.append(f"- {label}: {parsed}")
        text_output.append("")

        text_output.append("[학생 이수 현황]")
        for key, value in status.items():
            label = format_key(key)
            parsed = parse_numeric_field(value)
            text_output.append(f"- {label}: {parsed}")
        text_output.append("")

    # 수강과목
    if "수강과목" in data and "수강과목" in data["수강과목"]:
        text_output.append("[수강 과목 목록]")
        for c in data["수강과목"]["수강과목"]:
            code = c.get("학수번호", "")
            name = c.get("전공명", "")
            credit = c.get("학점", "")
            semester = c.get("수강학기", "")
            text_output.append(f"- {code} / {name} / {credit}학점 / {semester}")
        text_output.append("")

    return "\n".join(text_output)
