import colander
from deform.widget import TextAreaWidget


class GlossarySchema(colander.MappingSchema):
    title = colander.SchemaNode(
        colander.String(),
        title=u'Title',
    )


class TermSchema(colander.MappingSchema):
    title = colander.SchemaNode(
        colander.String(),
        title=u'Title',
    )
    definition = colander.SchemaNode(
        colander.String(),
        title=u'Definition',
        widget=TextAreaWidget(cols=40, rows=5),
    )
