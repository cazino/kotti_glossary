from kotti import DBSession
from kotti.views.edit.content import DocumentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from .resources import GlossDocument, Glossary, Term
from .schemas import GlossarySchema, TermSchema
from .utils import TermsProcessor


@view_config(name='scan-terms', permission='view',
             renderer='kotti_glossary:templates/scan-terms-view.pt')
def scan_terms(context, request):
    """
    """
    if 'scan-terms' in request.POST:
        body = context.body
        proc = TermsProcessor(body)
        _id = request.POST['glossary_id']
        glossary = DBSession.query(Glossary).get(_id)
        terms_dict = glossary.get_terms(request)
        proc.reset_anchors()
        context.body = proc.insert_anchors(terms_dict)
        return HTTPFound(location=request.resource_url(context))
    result = list()
    for node in DBSession.query(Glossary):
        result.append(node)
    return dict(glossaries=result)


@view_config(name='reset-terms', permission='view')
def reset_terms(context, request):
    body = context.body
    proc = TermsProcessor(body)
    context.body = proc.reset_anchors()
    return HTTPFound(location=request.resource_url(context))


@view_config(name='view', context=Glossary,
             permission='view',
             renderer='kotti_glossary:templates/view-glossary.pt')
def view_glossary(context, request):

    def key_gettter(obj):
        return obj.title.lower()

    terms = context.children
    terms.sort(key=key_gettter)
    return dict(glossary=context, terms=terms)


class GlossDocAddForm(AddFormView):
    schema_factory = DocumentSchema
    add = GlossDocument
    item_type = u"GlossDocument"


class GlossDocEditForm(EditFormView):
    schema_factory = DocumentSchema


class GlossaryAddForm(AddFormView):
    schema_factory = GlossarySchema
    add = Glossary
    item_type = u"Glossary"


class GlossaryEditForm(EditFormView):
    schema_factory = GlossarySchema


class TermAddForm(AddFormView):
    schema_factory = TermSchema
    add = Term
    item_type = u"Term"


class TermEditForm(EditFormView):
    schema_factory = TermSchema


def includeme(config):
    config.add_view(
        GlossDocAddForm,
        name=GlossDocument.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
    )

    config.add_view(
        GlossDocEditForm,
        context=GlossDocument,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
    )
    config.add_view(
        GlossaryAddForm,
        name=Glossary.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
    )

    config.add_view(
        GlossaryAddForm,
        context=Glossary,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
    )
    config.add_view(
        TermAddForm,
        name=Term.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
    )

    config.add_view(
        TermEditForm,
        context=Term,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
    )
