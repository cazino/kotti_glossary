from bs4 import BeautifulSoup
import nltk


class TermsProcessor(object):

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

    def _is_gl(self, tag):
        return tag.name == 'a' and tag.has_attr('data-glossary-term')

    def _transform_term(self, term, term_lower, glossary):
        anchor = self.soup.new_tag('a')
        anchor['data-glossary-term'] = term_lower
        anchor['href'] = glossary[term_lower]
        anchor.append(term)
        return anchor

    def _create_anchors(self, text_soup, glossary):
        result = list()
        word_buffer = list()
        match = False
        for word in nltk.tokenize.word_tokenize(text_soup):
            word_lower = word.lower()
            if word_lower in glossary:
                match = True
                if word_buffer:
                    result.append(
                        self._create_text(" ".join(word_buffer) + " "))
                    word_buffer = list()
                result.append(self._transform_term(word, word_lower, glossary))
            else:
                word_buffer.append(word)
        if word_buffer:
            result.append(self._create_text(" " + " ".join(word_buffer)))
        if not match:
            result = list()
        return result

    def insert_anchors(self, glossary):
        """Scan the glossary text for terms and replaces it with
        anchors
        """
        text_soup_list = self.soup.find_all(text=True)
        for text_soup in text_soup_list:
            elems = self._create_anchors(text_soup, glossary)
            if elems:
                parent = text_soup.parent
                text_soup.extract()
                for elem in elems:
                    parent.append(elem)
        return str(self.soup)

    def reset_anchors(self):
        """Replaces anchor tho the glossar by the raw term.
        """
        for anchor in self.soup.find_all(self._is_gl):
            text = self._create_text(anchor.text)
            anchor.insert_before(text)
            anchor.extract()
        return str(self.soup)
