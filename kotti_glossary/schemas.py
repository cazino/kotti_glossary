import colander
from deform.widget import TextAreaWidget

from kotti_glossary import _


class GlossarySchema(colander.MappingSchema):
    title = colander.SchemaNode(
        colander.String(),
        title=_('Title'),
    )


class TermSchema(colander.MappingSchema):
    title = colander.SchemaNode(
        colander.String(),
        title=_('Title'),
    )
    definition = colander.SchemaNode(
        colander.String(),
        title=_('Definition'),
        widget=TextAreaWidget(cols=40, rows=5),
    )
