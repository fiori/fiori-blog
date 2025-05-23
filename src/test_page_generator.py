import unittest

from page_generator import extract_title

class Test_PageGenerator(unittest.TestCase):

    def test_extract_title(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

# This is a title

## This is an heading 2

"""


        title = extract_title(md)
        self.assertEqual(title, "This is a title")

    def test_eq_double(self):
        actual = extract_title(
            """
# This is a title

# This is a second title that should be ignored
"""
        )
        self.assertEqual(actual, "This is a title")

    def test_eq_long(self):
        actual = extract_title(
            """
# title

this is a bunch

of text

- and
- a
- list
"""
        )
        self.assertEqual(actual, "title")

    def test_none(self):
        try:
            extract_title(
                """
no title
"""
            )
            self.fail("Should have raised an exception")
        except Exception as e:
            pass

if __name__ == "__main__":
    unittest.main()
