import unittest
from services.jd_parser import parse_job_description


class TestJDParser(unittest.TestCase):

    def test_normal_input(self):
        """Test a normal job description with title, skills and keywords."""
        jd = "We are looking for a Senior Python Developer with Machine Learning experience using Docker and Kubernetes."

        result = parse_job_description(jd)

        self.assertIsInstance(result["title"], str)
        self.assertIsInstance(result["skills"], list)
        self.assertIsInstance(result["keywords"], list)

    def test_empty_input(self):
        """Test an empty job description returns defaults for title and skills arrays of keywords are both also."""
        jd = ""

        result = parse_job_description(jd)

        self.assertEqual(result["title"], "")
        assert len(result["skills"]) == 0


if __name__ == "__main__":
    unittest.main()
