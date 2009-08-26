# -*- coding: utf-8 -*-

import grokcore.view as grok

from zope.size import byteDisplay
from zope.interface import Interface, implements
from zope.component import getMultiAdapter
from zope.traversing.browser.absoluteurl import absoluteURL

import megrok.z3cform as z3cform
from z3c.form.browser import file
from z3c.form.widget import FieldWidget
from z3c.form.interfaces import DISPLAY_MODE, INPUT_MODE, NOVALUE
from z3c.form.interfaces import IFieldWidget, IFormLayer, IDataManager
from dolmen.file import INamedFile, IFileField


class IFileWidget(Interface):
    """A widget that represents a file.
    """


class FileWidget(file.FileWidget):
    """A widget for a named file object
    """
    klass = u'file-widget'
    value = None
    implements(IFileWidget)

    def update(self):
        file.FileWidget.update(self)
        self.url = absoluteURL(self.context, self.request)
        
    @property
    def allow_nochange(self):
        return not self.ignoreContext and \
                   self.field is not None and \
                   self.value is not None and \
                   self.value != self.field.missing_value

    @property
    def filename(self):           
        if INamedFile.providedBy(self.value):
            return self.value.filename
        return None
 
    @property
    def file_size(self):
        if INamedFile.providedBy(self.value):
            size = self.value.getSize()
            return {'raw': size, 'display': byteDisplay(size)}
        return None

    @property
    def download_url(self):
        if self.field is None:
            return None
        if self.ignoreContext:
            return None
        return '%s/++download++%s' % (self.url, self.field.__name__)

    def extract(self, default=NOVALUE):
        nochange = self.request.get("%s.nochange" % self.name, None)
 
        if nochange == 'nochange':
            dm = getMultiAdapter((self.context, self.field), IDataManager)
            return dm.get()
        elif nochange == 'delete':
            return None
        else:
            return file.FileWidget.extract(self, default)


class FileWidgetInput(z3cform.WidgetTemplate):
    grok.context(Interface)
    grok.layer(IFormLayer)
    grok.template('templates/input.pt')
    z3cform.directives.field(IFileField)
    z3cform.directives.mode(INPUT_MODE)


class FileWidgetDisplay(z3cform.WidgetTemplate):
    grok.context(Interface)
    grok.layer(IFormLayer)
    grok.template('templates/display.pt')
    z3cform.directives.field(IFileField)
    z3cform.directives.mode(DISPLAY_MODE)


@grok.adapter(IFileField, IFormLayer)
@grok.implementer(IFieldWidget)
def FileFieldWidget(field, request):
    """IFieldWidget factory for FileWidget."""
    return FieldWidget(field, FileWidget(request))
