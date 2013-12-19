# -*- coding: utf-8 -*-

"""
Created on 2013-12-17
:author: Emmanuel Cazenave (cazino)
"""


def kotti_configure(settings):
    settings['kotti.available_types'] += \
        ' kotti_glossary.resources.GlossDocument'
    settings['pyramid.includes'] += ' kotti_glossary'


def includeme(config):
    """
    Pyramid includme hook.  Don't use it directly but indirectly via the
    :func:`kotti_configure` hook.

    :param config: Pyramid config object
    :type config: :class:`pyramid.config.Configurator`
    """
    config.scan('kotti_glossary.views')