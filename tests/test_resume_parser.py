import unittest
from services.resume_parser import parse_candidate

class TestResumeParser(unittest.TestCase):

    def test_valid_input(self):
        candidate = {
            "name": "Atharav Tayade",
            "skills": [
                "Python",
                "Machine Learning",
                "Git"
            ]
        }
        expected_output = {
            "name": "Atharav Tayade",
            "skills": [
                "git",
                "machine learning",
                "python"
            ]
        }
        self.assertEqual(parse_candidate(candidate), expected_output)

    def test_empty_candidate_dict(self):
        candidate = {}
        expected_output = {"name": "", "skills": []}
        self.assertEqual(parse_candidate(candidate), expected_output)

    def test_missing_name_field(self):
        candidate = {
            "skills": [
                "Python"
            ]
        }
        expected_output = {"name": "", "skills": ["python"]}
        self.assertEqual(parse_candidate(candidate), expected_output)

    def test_missing_skills_field(self):
        candidate = {
            "name": "Atharav Tayade"
        }
        expected_output = {"name": "Atharav Tayade", "skills": []}
        self.assertEqual(parse_candidate(candidate), expected_output)

    def test_empty_name_field(self):
        candidate = {
            "name": "",
            "skills": [
                "Python"
            ]
        }
        expected_output = {"name": "", "skills": ["python"]}
        self.assertEqual(parse_candidate(candidate), expected_output)

    def test_name_normalization(self):
        candidate = {
            "name": "atharav tayade",
            "skills": [
                "Python"
            ]
        }
        expected_output = {"name": "Atharav Tayade", "skills": ["python"]}
        self.assertEqual(parse_candidate(candidate), expected_output)

    def test_name_with_extra_spaces(self):
        candidate = {
            "name": "  atharav tayade  ",
            "skills": [
                "Python"
            ]
        }
        expected_output = {"name": "Atharav Tayade", "skills": ["python"]}
        self.assertEqual(parse_candidate(candidate), expected_output)

    def test_empty_skills_list(self):
        candidate = {
            "name": "Atharav Tayade",
            "skills": []
        }
        expected_output = {"name": "Atharav Tayade", "skills": []}
        self.assertEqual(parse_candidate(candidate), expected_output)

    def test_skill_normalization(self):
        candidate = {
            "name": "Atharav Tayade",
            "skills": [
                "  PyThOn  ",
                "machine learning"
            ]
        }
        expected_output = {"name": "Atharav Tayade", "skills": ["machine learning", "python"]}
        self.assertEqual(parse_candidate(candidate), expected_output)

    def test_remove_duplicate_skills(self):
        candidate = {
            "name": "Atharav Tayade",
            "skills": [
                "Python",
                "python",
                "Git",
                "git "
            ]
        }
        expected_output = {"name": "Atharav Tayade", "skills": ["git", "python"]}
        self.assertEqual(parse_candidate(candidate), expected_output)

    def test_remove_empty_skill_values(self):
        candidate = {
            "name": "Atharav Tayade",
            "skills": [
                "Python",
                "",
                "Git",
                None, # Test None values in skills list
                " "
            ]
        }
        expected_output = {"name": "Atharav Tayade", "skills": ["git", "python"]}
        self.assertEqual(parse_candidate(candidate), expected_output)

    def test_non_list_skills_input(self):
        candidate = {"name": "Atharav Tayade", "skills": "Python, Git"}
        expected_output = {"name": "Atharav Tayade", "skills": []}
        self.assertEqual(parse_candidate(candidate), expected_output)

    def test_non_string_name_input(self):
        candidate = {"name": 123, "skills": ["Python"]}
        expected_output = {"name": "", "skills": ["python"]}
        self.assertEqual(parse_candidate(candidate), expected_output)

if __name__ == '__main__':
    unittest.main()
