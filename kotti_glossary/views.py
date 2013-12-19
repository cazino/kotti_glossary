from kotti.views.edit.content import DocumentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.view import view_defaults

from .resources import GlossDocument
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

    @view_config(name='scan-glossary')
    def scan_glossary(self):
        """
        """
        body = self.context.body
        proc = TermsProcessor(body)
        proc.transform_terms()
        try:
            proc.apply_glossary(dict())
        except KeyError as e:
            self.request.session.flash('Unkown term: %s' % e)
        return self.back()


class GlossDocAddForm(AddFormView):
    schema_factory = DocumentSchema
    add = GlossDocument
    item_type = u"GlossDocument"


class GlossDocEditForm(EditFormView):
    schema_factory = DocumentSchema


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
