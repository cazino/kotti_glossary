import unittest


class TestTransformTerms(unittest.TestCase):

    def _getTargetClass(self):
        from kotti_glossary.utils import TermsProcessor
        return TermsProcessor

    def _makeOne(self, html_text):
        return self._getTargetClass()(html_text)

    def test_p(self):
        text = "<p>{{toto}}</p>"
        tm = self._makeOne(text)
        expected = '<p><a data-glossary-term="toto" href="">toto</a></p>'
        self.assertEquals(expected, tm.transform_terms())

    def test_no_tag(self):
        text = "{{toto}}"
        tm = self._makeOne(text)
        expected = '<a data-glossary-term="toto" href="">toto</a>'
        self.assertEquals(expected, tm.transform_terms())

    def test_what(self):
        text = u'<p>toto <strong>{{tata}}</strong></p>'
        tm = self._makeOne(text)
        expected = ('<p>toto <strong><a data-glossary-term="tata" href="">' +
                    'tata</a></strong></p>')
        self.assertEquals(expected, tm.transform_terms())

    def test_space_after_term(self):
        text = u'<p>toto {{tata}} aa</p>'
        tm = self._makeOne(text)
        expected = ('<p>toto <a data-glossary-term="tata" href="">' +
                    'tata</a> aa</p>')
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
