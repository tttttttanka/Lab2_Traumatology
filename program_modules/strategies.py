
def choose_by_priority(agenda):
    #Выбирает правило с наибольшим приоритетом

    return max(
        agenda,
        key=lambda rule: rule["priority"]
    )


def choose_by_specificity(agenda):
    #Выбирает правило с наибольшим числом условий

    return max(
        agenda,
        key=lambda rule: (
            len(rule["conditions"]) + len(rule["not_conditions"]),
            rule["priority"]
        )
    )


def choose_first(agenda):
    
    #Выбирает первое правило в повестке

    return agenda[0]


STRATEGIES = {
    "priority": choose_by_priority,
    "specificity": choose_by_specificity,
    "first": choose_first
}


def choose_rule(agenda, strategy):
    #Выбирает активное правило заданной стратегией

    if not agenda:
        return None

    if strategy not in STRATEGIES:
        raise ValueError(
            f"Неизвестная стратегия: {strategy}. "
            f"Доступны: {', '.join(STRATEGIES)}."
        )

    return STRATEGIES[strategy](agenda)
