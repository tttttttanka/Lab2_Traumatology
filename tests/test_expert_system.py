
import json
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

from knowledge_base import load_knowledge_base
from working_memory import WorkingMemory
from inference_engine import InferenceEngine
from strategies import choose_rule


class ExpertSystemTests(unittest.TestCase):

    def test_load_json_rules(self):
        path = PROJECT_ROOT / "knowledge_base" / "rules.json"
        rules = load_knowledge_base(path)

        self.assertGreater(len(rules), 0)

    def test_invalid_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text("{invalid", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_knowledge_base(path)

    def test_working_memory(self):
        memory = WorkingMemory()

        added = memory.add_fact("bol_v_kolene", "yes")

        self.assertTrue(added)
        self.assertTrue(
            memory.has_fact("bol_v_kolene", "yes")
        )

    def test_conflicting_fact_values(self):
        memory = WorkingMemory()
        memory.add_fact("otek", "yes")

        with self.assertRaises(ValueError):
            memory.add_fact("otek", "no")

    def test_forward_chaining(self):
        rules = [
            {
                "id": "test-rule",
                "priority": 10,
                "conditions": [
                    {"fact": "pain", "value": "yes"}
                ],
                "not_conditions": [],
                "conclusion": {
                    "name": "result",
                    "value": "yes",
                    "kind": "diagnosis"
                },
                "explanation": "Тестовое правило."
            }
        ]

        memory = WorkingMemory()
        memory.add_fact("pain", "yes")

        engine = InferenceEngine(rules, memory)
        diagnoses = engine.run()

        self.assertEqual(len(diagnoses), 1)
        self.assertTrue(memory.has_fact("result", "yes"))

    def test_negative_condition(self):
        rules = [
            {
                "id": "negative-rule",
                "priority": 10,
                "conditions": [
                    {"fact": "pain", "value": "yes"}
                ],
                "not_conditions": [
                    {"fact": "locking", "value": "yes"}
                ],
                "conclusion": {
                    "name": "result",
                    "value": "yes",
                    "kind": "diagnosis"
                },
                "explanation": "Тест отрицательного условия."
            }
        ]

        memory = WorkingMemory()
        memory.add_fact("pain", "yes")
        memory.add_fact("locking", "yes")

        engine = InferenceEngine(rules, memory)
        diagnoses = engine.run()

        self.assertEqual(diagnoses, [])

    def test_priority_strategy(self):
        agenda = [
            {
                "id": "low",
                "priority": 10,
                "conditions": [],
                "not_conditions": []
            },
            {
                "id": "high",
                "priority": 20,
                "conditions": [],
                "not_conditions": []
            }
        ]

        selected = choose_rule(agenda, "priority")

        self.assertEqual(selected["id"], "high")

    def test_specificity_strategy(self):
        agenda = [
            {
                "id": "simple",
                "priority": 10,
                "conditions": [
                    {"fact": "a", "value": "yes"}
                ],
                "not_conditions": []
            },
            {
                "id": "specific",
                "priority": 10,
                "conditions": [
                    {"fact": "a", "value": "yes"},
                    {"fact": "b", "value": "yes"}
                ],
                "not_conditions": []
            }
        ]

        selected = choose_rule(agenda, "specificity")

        self.assertEqual(selected["id"], "specific")

    def test_first_strategy(self):
        agenda = [
            {
                "id": "first",
                "priority": 1,
                "conditions": [],
                "not_conditions": []
            },
            {
                "id": "second",
                "priority": 100,
                "conditions": [],
                "not_conditions": []
            }
        ]

        selected = choose_rule(agenda, "first")

        self.assertEqual(selected["id"], "first")


if __name__ == "__main__":
    unittest.main()
