
class WorkingMemory:
    #Хранит исходные факты и результаты логического вывода

    def __init__(self):
        self.facts = {}
        self.fired_rules = set()
        self.trace = []

    def add_fact(
        self,
        name,
        value,
        source="input",
        rule_id=None,
        explanation=None,
        conditions=None
    ):
        #Добавляет факт и сохраняет сведения о его происхождении

        if name in self.facts:
            existing = self.facts[name]

            if existing["value"] != value:
                raise ValueError(
                    f"Конфликт значений факта {name}: "
                    f"{existing['value']} и {value}."
                )

            return False

        fact = {
            "name": name,
            "value": value,
            "source": source,
            "rule_id": rule_id,
            "explanation": explanation,
            "conditions": conditions or []
        }

        self.facts[name] = fact
        return True

    def get_value(self, name):
        #Возвращает значение факта или None, если факт неизвестен

        fact = self.facts.get(name)
        return fact["value"] if fact else None

    def has_fact(self, name, value):
        #Проверяет наличие факта с заданным значением

        return self.get_value(name) == value

    def get_all_facts(self):
        #Возвращает все факты в виде списка

        return list(self.facts.values())

    def get_diagnoses(self):
        #Возвращает заключения, сформированные правилами

        return [
            fact
            for fact in self.facts.values()
            if fact["source"] == "rule"
            and fact.get("kind") == "diagnosis"
        ]

    def record_firing(self, rule_id):
        #Запоминает срабатывание правила

        self.fired_rules.add(rule_id)

    def add_trace(self, entry):
        #Сохраняет запись для последующего объяснения

        self.trace.append(entry)
