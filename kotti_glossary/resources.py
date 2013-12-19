from kotti.resources import Content, Document
from kotti.util import Link
import sqlalchemy


class Glossary(Content):
    id = sqlalchemy.Column(
        sqlalchemy.Integer(), sqlalchemy.ForeignKey('contents.id'),
        primary_key=True)

    type_info = Content.type_info.copy(
        name=u'Glossary',
        title=u'Glossary',
        add_view=u'add_glossary',
        addable_to=[u'Document'],
    )


class Term(Content):

    id = sqlalchemy.Column(
        sqlalchemy.Integer(), sqlalchemy.ForeignKey('contents.id'),
        primary_key=True)

    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    type_info = Content.type_info.copy(
        name=u'Term',
        title=u'Term',
        add_view=u'add_term',
        addable_to=[u'Glossary'],
    )


class Definition(Content):
    id = sqlalchemy.Column(
        sqlalchemy.Integer(), sqlalchemy.ForeignKey('contents.id'),
        primary_key=True)

    body = sqlalchemy.Column(sqlalchemy.Text)

    type_info = Content.type_info.copy(
        name=u'Term',
        title=u'Term',
        add_view=u'add_term',
        addable_to=[u'Term'],
    )


class GlossDocument(Document):

    id = sqlalchemy.Column(
        sqlalchemy.Integer(),
        sqlalchemy.ForeignKey('documents.id'),
        primary_key=True
    )

    type_info = Document.type_info.copy(
        name=u'GlossDocument',
        title=u'GlossDocument'
    )
    type_info.edit_links.append(Link('scan-glossary', title=u'scan-glossary'),)