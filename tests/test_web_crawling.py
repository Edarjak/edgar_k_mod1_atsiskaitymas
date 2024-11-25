import unittest
from unittest.mock import mock_open, patch

from edgar_k_mod1_atsiskaitymas.web_crawling import crawl


class TestCrawl(unittest.TestCase):
    @patch("requests.get")
    @patch("builtins.open", new_callable=mock_open)
    def test_crawl(self, mock_file_open, mock_requests_get):
        mock_response = patch("requests.get", autospec=True)
        mock_requests_get.return_value = mock_response

        test_cases = [
            {"data": (2, "camelia", "csv"), "expect_error": False},
            {"data": (3, "camelia", "txt"), "expect_error": False},
            {
                "data": ("4", "camelia", "csv"),
                "expect_error": True,
                "expected_error_message": "Wrong type of the input data",
            },
            {
                "data": (4, "autoplius", "csv"),
                "expect_error": True,
                "expected_error_message": (
                    "Wrong source. Can crawl only cameliavaistine.lt and varle.lt"
                ),
            },
            {
                "data": (4, "camelia", "json"),
                "expect_error": True,
                "expected_error_message": "Can't output in this format",
            },
            {"data": (5, "varle", "txt"), "expect_error": False},
            {"data": (6, "varle", "csv"), "expect_error": False},
            {
                "data": (4, "varle", "json"),
                "expect_error": True,
                "expected_error_message": "Can't output in this format",
            },
            {
                "data": ("7", "varle", "csv"),
                "expect_error": True,
                "expected_error_message": "Wrong type of the input data",
            },
        ]

        for case in test_cases:
            data = case["data"]
            expect_error = case["expect_error"]

            if expect_error:
                with self.assertRaises(TypeError) as context:
                    crawl(*data)
                self.assertEqual(str(context.exception), case["expected_error_message"])
            else:
                try:
                    crawl(*data)
                except Exception as e:
                    self.fail(f"crawl raised an unexpected exception: {e}")

        self.assertTrue(
            mock_file_open.called, "File open was not called in non-error cases"
        )


if __name__ == "__main__":
    unittest.main()
