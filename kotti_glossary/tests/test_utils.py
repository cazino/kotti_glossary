import unittest


class TestInsertAnchors(unittest.TestCase):

    def _getTargetClass(self):
        from kotti_glossary.utils import TermsProcessor
        return TermsProcessor

    def _makeOne(self, html_text):
        return self._getTargetClass()(html_text)

    def test_basic(self):
        text = 'toto'
        tm = self._makeOne(text)
        expected = '<a data-glossary-term="toto" href="/url">toto</a>'
        self.assertEquals(expected, tm.insert_anchors(dict(toto="/url")))

    def test_p(self):
        text = "<p>toto</p>"
        tm = self._makeOne(text)
        expected = '<p><a data-glossary-term="toto" href="/url">toto</a></p>'
        self.assertEquals(expected, tm.insert_anchors(dict(toto="/url")))

    def test_multiple_markup(self):
        text = u'<p>toto <strong>tata</strong></p>'
        tm = self._makeOne(text)
        expected = \
            ('<p>toto <strong><a data-glossary-term="tata" href="/url">' +
             'tata</a></strong></p>')
        self.assertEquals(expected, tm.insert_anchors(dict(tata="/url")))

    def test_space_after_term(self):
        text = u'<p>toto tata aa</p>'
        tm = self._makeOne(text)
        expected = ('<p>toto <a data-glossary-term="tata" href="/url">' +
                    'tata</a> aa</p>')
        self.assertEquals(expected, tm.insert_anchors(dict(tata="/url")))


class TestResetAnchors(unittest.TestCase):

    def _getTargetClass(self):
        from kotti_glossary.utils import TermsProcessor
        return TermsProcessor

    def _makeOne(self, html_text):
        return self._getTargetClass()(html_text)

    def test_basic(self):
        text = '<a data-glossary-term="toto" href="/url">toto</a>'
        tm = self._makeOne(text)
        expected = 'toto'
        self.assertEquals(expected, tm.reset_anchors())

    def test_p(self):
        text = '<p><a data-glossary-term="toto" href="/url">toto</a></p>'
        expected = "<p>toto</p>"
        tm = self._makeOne(text)
        self.assertEquals(expected, tm.reset_anchors())

    def test_multiple_markup(self):
        text = \
            ('<p>toto <strong><a data-glossary-term="tata" href="/url">' +
             'tata</a></strong></p>')
        expected = u'<p>toto <strong>tata</strong></p>'
        tm = self._makeOne(text)
        self.assertEquals(expected, tm.reset_anchors())

    def test_space_after_term(self):
        text = ('<p>toto <a data-glossary-term="tata" href="/url">' +
                'tata</a> aa</p>')
        tm = self._makeOne(text)
        expected = u'<p>toto tata aa</p>'
        self.assertEquals(expected, tm.reset_anchors())
