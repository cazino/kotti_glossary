from kotti.resources import Content, Document
from kotti.util import Link
import sqlalchemy


class Glossary(Content):
    id = sqlalchemy.Column(
        sqlalchemy.Integer(), sqlalchemy.ForeignKey('contents.id'),
        primary_key=True)

    title = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    type_info = Content.type_info.copy(
        name=u'Glossary',
        title=u'Glossary',
        add_view=u'add_glossary',
        addable_to=[u'Document'],
    )

    def get_terms(self, request):
        """Retrurns a adict of term: url.
        """
        res = dict()
        for term in self.children:
            title = term.title
            anchor = 'term-%s' % title
            url = request.resource_url(self, anchor=anchor)
            res[title] = url
        return res


class Term(Content):

    id = sqlalchemy.Column(
        sqlalchemy.Integer(), sqlalchemy.ForeignKey('contents.id'),
        primary_key=True)

    title = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    definition = sqlalchemy.Column(sqlalchemy.Text)

    type_info = Content.type_info.copy(
        name=u'Term',
        title=u'Term',
        add_view=u'add_term',
        addable_to=[u'Glossary'],
    )


class GlossDocument(Document):

    id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey('documents.id'),
        primary_key=True
    )
    type_info = Document.type_info.copy(
        name=u'GlossDocument',
        title=u'GlossDocument',
        add_view=u'add_glossdoc',
    )
    type_info.edit_links.append(Link('scan-terms', title=u'scan-terms'))
