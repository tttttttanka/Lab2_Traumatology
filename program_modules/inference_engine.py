
from strategies import choose_rule


class InferenceEngine:
    #Механизм прямого логического вывода

    def __init__(self, rules, working_memory):
        self.rules = rules
        self.memory = working_memory

    def conditions_match(self, rule):
        #Проверяет положительные и отрицательные условия

        for condition in rule["conditions"]:
            if not self.memory.has_fact(
                condition["fact"],
                condition["value"]
            ):
                return False

        for condition in rule["not_conditions"]:
            if self.memory.has_fact(
                condition["fact"],
                condition["value"]
            ):
                return False

        return True

    def get_agenda(self):
        #Возвращает активные правила, ещё не сработавшие

        agenda = []

        for rule in self.rules:
            if rule["id"] in self.memory.fired_rules:
                continue

            if self.conditions_match(rule):
                agenda.append(rule)

        return agenda

    def run(self, strategy="priority", max_steps=100):
        #Выполняет прямой вывод до отсутствия активных правил

        steps = 0

        while steps < max_steps:
            agenda = self.get_agenda()

            if not agenda:
                break

            rule = choose_rule(agenda, strategy)
            conclusion = rule["conclusion"]

            supporting_facts = [
                {
                    "fact": condition["fact"],
                    "value": condition["value"]
                }
                for condition in rule["conditions"]
            ]

            added = self.memory.add_fact(
                name=conclusion["name"],
                value=conclusion["value"],
                source="rule",
                rule_id=rule["id"],
                explanation=rule["explanation"],
                conditions=supporting_facts
            )

            if added:
                self.memory.facts[conclusion["name"]]["kind"] = (
                    conclusion["kind"]
                )

            self.memory.record_firing(rule["id"])

            self.memory.add_trace({
                "rule_id": rule["id"],
                "priority": rule["priority"],
                "strategy": strategy,
                "conclusion": conclusion["name"],
                "value": conclusion["value"],
                "added": added
            })

            steps += 1

        if steps >= max_steps and self.get_agenda():
            raise RuntimeError(
                "Превышен предел шагов логического вывода."
            )

        return self.memory.get_diagnoses()
