
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

    @view_config(name='scan-glossary', context=GlossDocument)
    def scan_glossary(self):
        """
        """
        body = self.context.body
        proc = TermsProcessor(body)
        proc.transform_terms()
        proc.apply_glossary(dict())
        return self.back()
