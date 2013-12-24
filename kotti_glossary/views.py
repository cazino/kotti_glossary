from kotti import DBSession
from kotti.views.edit.content import DocumentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.view import view_defaults

from .resources import GlossDocument, Glossary, Term
from .schemas import GlossarySchema, TermSchema
from .utils import TermsProcessor


@view_defaults(permission='edit')
class NodeActions(object):
    """Actions related to content nodes."""

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.flash = self.request.session.flash

    def back(self, view=None):
        """
        Redirect to the given view of the context, the referrer of the request
        or the default_view of the context.

        :rtype: pyramid.httpexceptions.HTTPFound
        """
        url = self.request.resource_url(self.context)
        if view is not None:
            url += view
        elif self.request.referrer:
            url = self.request.referrer
        return HTTPFound(location=url)

    @view_config(name='scan-terms', permission='view',
                 renderer='kotti_glossary:templates/scan-terms-view.pt')
    def scan_terms(self):
        """
        """
        if 'scan-terms' in self.request.POST:
            body = self.context.body
            proc = TermsProcessor(body)
            _id = self.request.POST['glossary_id']
            glossary = DBSession.query(Glossary).get(_id)
            terms_dict = glossary.get_terms(self.request)
            proc.reset_anchors()
            self.context.body = proc.insert_anchors(terms_dict)
            return HTTPFound(location=self.request.resource_url(self.context))
        result = list()
        for node in DBSession.query(Glossary):
            result.append(node)
        return dict(glossaries=result)

    @view_config(name='reset-terms', permission='view')
    def reset_terms(self):
        body = self.context.body
        proc = TermsProcessor(body)
        self.context.body = proc.reset_anchors()
        return HTTPFound(location=self.request.resource_url(self.context))


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
