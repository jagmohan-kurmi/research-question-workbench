import json
import tempfile
import unittest
from pathlib import Path
from research_question_workbench.cli import main, validate

class WorkbenchTests(unittest.TestCase):
    def setUp(self):
        self.data = {g: {f: "value" for f in fs} for g, fs in {"pico":("population","intervention","comparison","outcome"),"spider":("sample","phenomenon","design","evaluation","research_type"),"finer":("feasible","interesting","novel","ethical","relevant")}.items()}
        self.data.update(question="How does treatment affect outcome?", inclusion=["adults"], exclusion=[])
    def test_completeness_and_overlap(self):
        self.assertEqual(validate(self.data), [])
        self.assertIn("missing question", validate({**self.data, "question": ""}))
        self.data["exclusion"] = [" Adults "]
        self.assertTrue(any("contradiction" in x for x in validate(self.data)))
        del self.data["pico"]["outcome"]
        self.assertTrue(any("missing pico.outcome" in x for x in validate(self.data)))
    def test_cli_exports_and_exit_codes(self):
        with tempfile.TemporaryDirectory() as td:
            src, out = Path(td)/"in.json", Path(td)/"out.md"
            src.write_text(json.dumps(self.data), encoding="utf-8")
            self.assertEqual(main([str(src), "--output", str(out)]), 0)
            self.assertIn("PICO", out.read_text(encoding="utf-8"))
            src.write_text("{broken", encoding="utf-8")
            self.assertEqual(main([str(src)]), 2)
    def test_non_object_rejected(self):
        with self.assertRaises(ValueError): validate([])

if __name__ == "__main__": unittest.main()
