import unittest


class TestRegexp(unittest.TestCase):

    def test_basic(self):
        from kotti_glossary.utils import TermsProcessor
        self.assertIsNotNone(TermsProcessor.regexp.search("term:aa "))

    def test_end_term(self):
        from kotti_glossary.utils import TermsProcessor
        self.assertIsNotNone(TermsProcessor.regexp.search("term:aa"))


class TestTransformTerms(unittest.TestCase):

    def _getTargetClass(self):
        from kotti_glossary.utils import TermsProcessor
        return TermsProcessor

    def _makeOne(self, html_text):
        return self._getTargetClass()(html_text)

    def test_p(self):
        text = "<p>term:toto</p>"
        tm = self._makeOne(text)
        expected = '<p><a data-glossary-term="toto" href="">toto</a></p>'
        self.assertEquals(expected, tm.transform_terms())

    def test_no_tag(self):
        text = "term:toto"
        tm = self._makeOne(text)
        expected = '<a data-glossary-term="toto" href="">toto</a>'
        self.assertEquals(expected, tm.transform_terms())


class TestApplyGlossary(unittest.TestCase):

    def _getTargetClass(self):
        from kotti_glossary.utils import TermsProcessor
        return TermsProcessor

    def _makeOne(self, html_text):
        return self._getTargetClass()(html_text)

    def test_basic(self):
        text = '<p><a data-glossary-term="toto" href="">toto</a></p>'
        tm = self._makeOne(text)
        expected = '<p><a data-glossary-term="toto" href="/url">toto</a></p>'
        self.assertEquals(expected, tm.apply_glossary(dict(toto="/url")))

    def test_raise_exec(self):
        text = '<p><a data-glossary-term="toto" href="">toto</a></p>'
        tm = self._makeOne(text)
        self.assertRaises(KeyError, tm.apply_glossary, dict())
