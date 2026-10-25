import ast
import unittest
from pathlib import Path

SOURCE = Path(__file__).parents[1] / "ace_tool.py"
TEXT = SOURCE.read_text()

class AceCoreContractTests(unittest.TestCase):
    def test_release_and_visible_marker(self):
        self.assertIn('version: 0.3.1', TEXT)
        self.assertIn('description: ACE 0.3.1', TEXT)
        self.assertIn('ACE_VERSION = "0.3.1"', TEXT)

    def test_evidence_paths_do_not_strip_content(self):
        tree = ast.parse(TEXT)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in {"_replay", "ace_get_message", "ace_get_context"}:
                segment = ast.get_source_segment(TEXT, node) or ""
                self.assertNotIn(".strip()", segment)

    def test_temporal_contract_markers_present(self):
        self.assertIn('ACE_TURN_CONTRACT = "turn-v1"', TEXT)
        self.assertIn('ACE_COORDINATE_CONTRACT = "trajectory-v1"', TEXT)
        self.assertIn('"oldest_first", "newest_first"', TEXT)
        self.assertIn('stamp >= float(before)', TEXT)

    def test_tilde_coordinate_notation(self):
        self.assertIn('return f"~{position}"', TEXT)
        self.assertIn('r"~?(\\d+)"', TEXT)
        self.assertNotIn('return f"@{position}"', TEXT)

if __name__ == "__main__":
    unittest.main()
