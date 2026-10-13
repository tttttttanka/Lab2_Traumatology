
from pathlib import Path

from knowledge_base import load_knowledge_base
from working_memory import WorkingMemory
from inference_engine import InferenceEngine
from explanation import explain_results


PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_PATH = PROJECT_ROOT / "knowledge_base" / "rules.json"


QUESTIONS = [
    ("koleno_hodit", "Колено нормально двигается?"),
    ("otek", "Есть отек?"),
    ("bol_pri_nagruzke", "Боль усиливается при нагрузке?"),
    ("srok_72", "Симптомы сохраняются более 72 часов?"),
    ("zaklinilo", "Было заклинивание сустава?"),
    ("hrust", "Слышен хруст?")
]


def ask_yes_no(question):
    #Запрашивает ответ, пока пользователь не введёт yes или no

    while True:
        answer = input(f"{question} (yes/no): ").strip().lower()

        if answer in ("yes", "no"):
            return answer

        print("Введите yes или no.")


def collect_facts(memory):
    #Собирает симптомы и помещает их в рабочую память

    print("\nОтветьте на вопросы о состоянии колена.")
    pain = ask_yes_no("Есть боль в колене?")

    memory.add_fact("bol_v_kolene", pain)

    if pain == "no":
        print("\nБоль в колене не отмечена.")
        print("Дополнительные вопросы не задаются.")
        return

    for fact_name, question in QUESTIONS:
        answer = ask_yes_no(question)
        memory.add_fact(fact_name, answer)


def choose_strategy():
    #Позволяет выбрать стратегию разрешения конфликтов

    print("\nВыберите стратегию разрешения конфликтов:")
    print("1 — priority (наибольший приоритет)")
    print("2 — specificity (наибольшее число условий)")
    print("3 — first (первое правило в повестке)")

    strategies = {
        "1": "priority",
        "2": "specificity",
        "3": "first"
    }

    while True:
        answer = input("Ваш выбор: ").strip()

        if answer in strategies:
            return strategies[answer]

        print("Введите 1, 2 или 3.")


def main():
    print("ЭКСПЕРТНАЯ СИСТЕМА: ТРАВМАТОЛОГИЯ")

    try:
        rules = load_knowledge_base(KNOWLEDGE_PATH)
    except (OSError, ValueError) as error:
        print(f"Ошибка загрузки базы знаний: {error}")
        return

    print(f"\nЗагружено правил: {len(rules)}")

    memory = WorkingMemory()
    collect_facts(memory)

    if memory.has_fact("bol_v_kolene", "no"):
        print("\nЗаключения по правилам системы не сформированы.")
        explain_results(memory)
        return

    strategy = choose_strategy()

    engine = InferenceEngine(rules, memory)

    try:
        diagnoses = engine.run(strategy=strategy)
    except (ValueError, RuntimeError) as error:
        print(f"Ошибка логического вывода: {error}")
        return

    print(f"\nИспользованная стратегия: {strategy}")
    print("\nРЕЗУЛЬТАТЫ")

    if diagnoses:
        for diagnosis in diagnoses:
            print(f"- {diagnosis['name']}")
    else:
        print("Подходящих заключений не получено.")

    explain_results(memory)

    print(
        "\nВажно: результаты являются учебными гипотезами, "
        "а не медицинским диагнозом."
    )


if __name__ == "__main__":
    main()
