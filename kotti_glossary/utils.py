import re
from bs4 import BeautifulSoup


class TermsProcessor(object):

    regexp = re.compile("term:\w*[\s\.]*")

    def __init__(self, html_text):
        self.html_text = html_text
        self.soup = BeautifulSoup(html_text, "html.parser")

    def _create_anchor(self, term):
        anchor = self.soup.new_tag('a')
        anchor['data-glossary-term'] = term
        anchor['href'] = ""
        anchor.append(term)
        return anchor

    def _create_text(self, text):
        res = self.soup.new_string(text)
        return res

    def _create_elems(self, token):
        res = list()
        end = len(token)
        start = 0
        for match in self.regexp.finditer(token):
            match_start, match_end = match.span()
            if start != match_start:
                res.append(self._create_text(token[start:match_start]))
            term = token[match_start:match_end].replace("term:", '')
            res.append(self._create_anchor(term))
            start = match_end
        if start < end and start != 0:
            res.append(self._create_text(token[start:]))
        return res

    def transform_terms(self):
        """Scan the text for term:xxx ocuurences and replace it with anchors
        """
        text_tokens = self.soup.find_all(text=True)
        for token in text_tokens:
            elems = self._create_elems(token)
            if elems:
                parent = token.parent
                token.extract()
                for elem in elems:
                    parent.append(elem)
        return str(self.soup)

    def _is_gl(self, tag):
        return tag.name == 'a' and tag.has_attr('data-glossary-term')

    def apply_glossary(self, glossary):
        """glossary: dict of term: url
        """
        for link in self.soup.find_all(self._is_gl):
            term = link['data-glossary-term']
            link['href'] = glossary[term]
        return str(self.soup)
