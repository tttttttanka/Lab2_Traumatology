
import json
from pathlib import Path


def validate_rules(rules):
    #Проверяет структуру продукционной базы знаний

    if not isinstance(rules, list):
        raise ValueError("Поле rules должно содержать список.")

    identifiers = set()

    for index, rule in enumerate(rules):
        prefix = f"Правило № {index + 1}"

        if not isinstance(rule, dict):
            raise ValueError(f"{prefix}: ожидается объект.")

        rule_id = rule.get("id")

        if not isinstance(rule_id, str) or not rule_id:
            raise ValueError(f"{prefix}: отсутствует id.")

        if rule_id in identifiers:
            raise ValueError(f"Повторяется идентификатор {rule_id}.")

        identifiers.add(rule_id)

        if not isinstance(rule.get("priority"), int):
            raise ValueError(f"{rule_id}: priority должен быть целым числом.")

        for field in ("conditions", "not_conditions"):
            conditions = rule.get(field)

            if not isinstance(conditions, list):
                raise ValueError(f"{rule_id}: {field} должен быть списком.")

            for condition in conditions:
                if (
                    not isinstance(condition, dict)
                    or not isinstance(condition.get("fact"), str)
                    or not isinstance(condition.get("value"), str)
                ):
                    raise ValueError(
                        f"{rule_id}: некорректное условие в {field}."
                    )

        conclusion = rule.get("conclusion")

        if not isinstance(conclusion, dict):
            raise ValueError(f"{rule_id}: отсутствует conclusion.")

        if not isinstance(conclusion.get("name"), str):
            raise ValueError(f"{rule_id}: отсутствует имя заключения.")

        if not isinstance(conclusion.get("value"), str):
            raise ValueError(f"{rule_id}: отсутствует значение заключения.")

        if conclusion.get("kind") not in ("syndrome", "diagnosis"):
            raise ValueError(f"{rule_id}: неизвестный тип заключения.")

        if not isinstance(rule.get("explanation"), str):
            raise ValueError(f"{rule_id}: отсутствует explanation.")

    return True


def load_knowledge_base(path):
    #Загружает JSON-файл и возвращает проверенный список правил

    path = Path(path)

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as error:
        raise FileNotFoundError(
            f"Файл базы знаний не найден: {path}"
        ) from error
    except json.JSONDecodeError as error:
        raise ValueError(
            f"Ошибка JSON в строке {error.lineno}: {error.msg}"
        ) from error

    if not isinstance(data, dict) or "rules" not in data:
        raise ValueError("В базе знаний отсутствует поле rules.")

    rules = data["rules"]
    validate_rules(rules)

    return rules
