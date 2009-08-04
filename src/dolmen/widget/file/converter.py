# -*- coding: utf-8 -*-

import grokcore.component as grok
from dolmen.file import IFileField
from dolmen.widget.file import FileWidget
from z3c.form.converter import BaseDataConverter


class RawDataConverter(BaseDataConverter, grok.MultiAdapter):
    """Converts from a file-upload to a NamedFile variant.
    """
    grok.adapts(IFileField, FileWidget)

    def toWidgetValue(self, value):
        return value

    def toFieldValue(self, value):
        return value
