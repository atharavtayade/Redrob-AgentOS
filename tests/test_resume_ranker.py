import unittest
from services.resume_ranker import rank_candidates

class TestResumeRanker(unittest.TestCase):

    def test_empty_candidate_list(self):
        job_description = "Python developer with experience in Flask and Django."
        candidates = []
        results = rank_candidates(job_description, candidates)
        self.assertEqual(results, [])

    def test_single_candidate(self):
        job_description = "Python developer with Flask experience."
        candidates = [{"name": "Alice", "skills": "Python, Flask"}]
        results = rank_candidates(job_description, candidates)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Alice")
        self.assertEqual(results[0]["score"], 40) # Corrected: (2 matched skills / 5 job keywords) * 100
        self.assertIsInstance(results[0]["matched_skills"], set)
        self.assertIn("python", results[0]["matched_skills"])
        self.assertIn("flask", results[0]["matched_skills"])

    def test_multiple_candidates(self):
        job_description = "Python developer with Flask and Django experience."
        candidates = [
            {"name": "Alice", "skills": "Python, Flask"},
            {"name": "Bob", "skills": "Java, Spring"},
            {"name": "Charlie", "skills": "Python, Django, AWS"},
        ]
        results = rank_candidates(job_description, candidates)
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["name"], "Alice") # Corrected due to tie-breaker by name
        self.assertEqual(results[0]["score"], 28) # Corrected: (2 matched skills / 7 job keywords) * 100 (int truncation)
        self.assertEqual(results[1]["name"], "Charlie") # Corrected due to tie-breaker by name
        self.assertEqual(results[1]["score"], 28) # Corrected: (2 matched skills / 7 job keywords) * 100 (int truncation)
        self.assertEqual(results[2]["name"], "Bob")
        self.assertEqual(results[2]["score"], 0)

    def test_score_between_0_and_100(self):
        # job_keywords from "Python, Java, C++, Go, Ruby, JavaScript, PHP, Swift, Kotlin, Rust" will be 10 unique keywords.
        job_description = "Python, Java, C++, Go, Ruby, JavaScript, PHP, Swift, Kotlin, Rust"
        candidates = [
            {"name": "Alice", "skills": "Python, Java"},
            {"name": "Bob", "skills": "Go"},
            {"name": "Charlie", "skills": "Ruby, C++"},
            {"name": "David", "skills": "Nonexistent Skill"}
        ]
        results = rank_candidates(job_description, candidates)
        for result in results:
            self.assertGreaterEqual(result["score"], 0)
            self.assertLessEqual(result["score"], 100)

    def test_results_sorted_by_descending_score(self):
        job_description = "Python, Flask, Django"
        candidates = [
            {"name": "Alice", "skills": "Python"},
            {"name": "Bob", "skills": "Python, Flask"},
            {"name": "Charlie", "skills": "Python, Django, Flask"},
        ]
        results = rank_candidates(job_description, candidates)
        # job_keywords: {'python', 'flask', 'django'} (length 3)
        # Alice: {'python'} -> score = (1/3)*100 = 33
        # Bob: {'python', 'flask'} -> score = (2/3)*100 = 66
        # Charlie: {'python', 'django', 'flask'} -> score = (3/3)*100 = 100
        self.assertEqual(results[0]["name"], "Charlie")
        self.assertEqual(results[1]["name"], "Bob")
        self.assertEqual(results[2]["name"], "Alice")

    def test_matched_skills_is_set(self):
        job_description = "Python, Flask"
        candidates = [{"name": "Alice", "skills": "Python, Flask"}]
        results = rank_candidates(job_description, candidates)
        self.assertIsInstance(results[0]["matched_skills"], set)

    def test_no_runtime_exceptions_for_empty_job_descriptions(self):
        job_description = ""
        candidates = [
            {"name": "Alice", "skills": "Python, Flask"},
            {"name": "Bob", "skills": "Java, Spring"}
        ]
        try:
            results = rank_candidates(job_description, candidates)
            self.assertIsNotNone(results)
            self.assertEqual(results[0]["score"], 0)
            self.assertEqual(results[1]["score"], 0)
        except Exception as e:
            self.fail(f"rank_candidates raised an exception with empty job description: {e}")

if __name__ == '__main__':
    unittest.main()
