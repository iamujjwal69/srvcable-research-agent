import unittest
from pathlib import Path
from main import check_entity_mismatch_caution, validate_report, load_documents


class TestEntityMismatchValidation(unittest.TestCase):
    def setUp(self):
        self.docs = load_documents()

    def test_correct_distinction_run_3_file(self):
        """Verify that the actual generated Run 3 report passes entity_mismatch_caution."""
        run_3_file = Path("output/srvcable_brief_run_3.md")
        if run_3_file.exists():
            text = run_3_file.read_text(encoding="utf-8")
            res = validate_report(text, self.docs)
            self.assertTrue(
                res["entity_mismatch_caution"],
                "Expected actual output/srvcable_brief_run_3.md to pass entity_mismatch_caution",
            )

    def test_correct_distinction_synthetic_wording(self):
        """Verify various correct distinction phrasings pass."""
        test_cases = [
            (
                "An ₹8 lakh penalty was issued against Sarvottam Cable Network [S8]; "
                "the evidence indicates this is distinct from the listed cable manufacturer SRVCABLE.",
                {"S8"},
            ),
            (
                "S8 reports a penalty on an unrelated local cable TV and broadband operator in Nagpur [S8].",
                {"S8"},
            ),
            (
                "The research pack does not establish that the Nagpur cable network is the same entity as SRVCABLE [S8].",
                {"S8"},
            ),
            (
                "A local operator was fined, but it does not appear to be the listed manufacturing company [S8].",
                {"S8"},
            ),
            (
                "A local news report mentions 'Sarvottam Cable Network' being penalised in Nagpur [S8]. "
                "It is unclear if these entities are related or distinct.",
                {"S8"},
            ),
            (
                "This report does not cite S8 at all, focusing strictly on official disclosures.",
                {"S1", "S2"},
            ),
        ]
        for snippet, cited_ids in test_cases:
            with self.subTest(snippet=snippet):
                self.assertTrue(
                    check_entity_mismatch_caution(snippet, cited_ids),
                    f"Expected caution to be True for: {snippet}",
                )

    def test_incorrect_attribution_fails(self):
        """Verify that reports incorrectly attributing the Nagpur penalty to SRVCABLE fail."""
        test_cases = [
            (
                "SRVCABLE was fined ₹8 lakh by Nagpur Municipal Corporation for overhead cables [S8].",
                {"S8"},
            ),
            (
                "The company was penalized ₹8 lakh in Nagpur for illegal overhead lines [S8].",
                {"S8"},
            ),
            (
                "Nagpur authorities imposed a penalty against SRVCABLE of ₹8 lakh [S8].",
                {"S8"},
            ),
            (
                "Sarvottam Cables Ltd was fined ₹8 lakh in Nagpur [S8].",
                {"S8"},
            ),
            (
                "The company received an ₹8 lakh penalty in Nagpur [S8], although some say it is a separate business.",
                {"S8"},
            ),
            (
                "The listed company faces an ₹8 lakh penalty from Nagpur Municipal Corporation [S8].",
                {"S8"},
            ),
        ]
        for snippet, cited_ids in test_cases:
            with self.subTest(snippet=snippet):
                self.assertFalse(
                    check_entity_mismatch_caution(snippet, cited_ids),
                    f"Expected caution to be False (rejected) for: {snippet}",
                )

    def test_s8_cited_without_any_distinction_fails(self):
        """Verify that citing S8 without providing any entity distinction wording fails."""
        report = (
            "A fine of ₹8 lakh was reported in Nagpur City Times [S8]. "
            "Municipal officers conducted an inspection across the ward yesterday."
        )
        self.assertFalse(
            check_entity_mismatch_caution(report, {"S8"}),
            "Expected failure when S8 is cited without distinction wording",
        )


if __name__ == "__main__":
    unittest.main()
