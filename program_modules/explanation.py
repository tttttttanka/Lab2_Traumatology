
def explain_results(working_memory):
    #Объясняет заключения на основе рабочей памяти

    print("ОБЪЯСНЕНИЕ РЕЗУЛЬТАТОВ")

    diagnoses = working_memory.get_diagnoses()

    if not diagnoses:
        print("По заданным правилам заключения не получены.")
    else:
        for diagnosis in diagnoses:
            print(f"\nЗаключение: {diagnosis['name']}")
            print(f"Значение: {diagnosis['value']}")
            print(f"Правило: {diagnosis['rule_id']}")
            print(f"Основание: {diagnosis['explanation']}")

            conditions = diagnosis.get("conditions", [])

            if conditions:
                print("Факты, использованные правилом:")

                for condition in conditions:
                    print(
                        f"  - {condition['fact']} = "
                        f"{condition['value']}"
                    )

    print("\nИстория логического вывода:")

    if not working_memory.trace:
        print("Правила не срабатывали.")
    else:
        for entry in working_memory.trace:
            print(
                f"- {entry['rule_id']}: "
                f"{entry['conclusion']} = {entry['value']}"
            )
