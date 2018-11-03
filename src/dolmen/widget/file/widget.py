# -*- coding: utf-8 -*-

from os import path
import crom
from cromlech.file import IFile, IFileField,FileField
from dolmen.forms.base.interfaces import IWidget, IWidgetExtractor
from dolmen.location import get_absolute_url
from dolmen.template import TALTemplate
from dolmen.widget.file import MF as _
from dolmen.forms.base import interfaces, NO_VALUE, NO_CHANGE
from dolmen.forms.base.widgets import DisplayFieldWidget, WidgetExtractor
from dolmen.forms.ztk.fields import (
    SchemaField, SchemaFieldWidget, registerSchemaField)


from zope.interface import Interface, implementer
from zope.location import ILocation
from zope.size.interfaces import ISized


KEEP = "keep"
DELETE = "delete"
REPLACE = "replace"
TEMPLATE_DIR = path.join(path.dirname(__file__), 'templates')


def register():
    """Entry point hook.
    """
    registerSchemaField(FileSchemaField, IFileField)


class IFileWidget(interfaces.IFieldWidget):
    """A widget that represents a file.
    """
    
from dolmen.forms.ztk.interfaces import ISchemaField
class IFileSchemaField(ISchemaField):
    pass

@implementer (IFileSchemaField)
class FileSchemaField(SchemaField):
    """A file field.
    """

@crom.adapter
@crom.target(IWidget)
@crom.sources(IFileSchemaField, Interface, Interface)
class FileWidget(SchemaFieldWidget):

    url = None
    allow_action = False

    filesize = None
    filename = None
    download = None

    template = TALTemplate(path.join(TEMPLATE_DIR, 'input.pt'))

    def prepareContentValue(self, value):
        if value is NO_VALUE or value is None:
            return {self.identifier: False}
        return {self.identifier: True}

    def update(self):
        SchemaFieldWidget.update(self)

        if not self.form.ignoreContent:
            content = self.form.getContentData().getContent()
            fileobj = self.component._field.get(content)

            if fileobj:
                self.allow_action = True
                if IFile.providedBy(fileobj):
                    self.filename = fileobj.filename
                    self.filesize = ISized(fileobj, None)
                else:
                    self.filename = _(u'download', default=u"Download")

                if ILocation.providedBy(content):
                    self.url = get_absolute_url(content, self.request)
                    self.download = "%s/++download++%s" % (
                        self.url, self.component.identifier)

@crom.adapter
@crom.name('display')
@crom.target(IWidget)
@crom.sources (IFileSchemaField, interfaces.IFormData, Interface)
class DisplayFileWidget(DisplayFieldWidget):
    url = None
    filesize = None
    filename = None
    download = None

    template = TALTemplate(path.join(TEMPLATE_DIR, 'display.pt'))

    def update(self):
        DisplayFieldWidget.update(self)
        content = self.form.getContentData().getContent()
        fileobj = self.component._field.get(content)

        if fileobj:
            if IFile.providedBy(fileobj):
                self.filename = fileobj.filename
                self.filesize = ISized(fileobj, None)

            self.url = get_absolute_url(content, self.request)
            self.download = "%s/++download++%s" % (
                self.url, self.component.identifier)

@crom.adapter
@crom.target(IWidgetExtractor)
@crom.sources(FileSchemaField, interfaces.IFormData, Interface)
class FileWidgetExtractor(WidgetExtractor):
    """A value extractor for a file widget (including image)
    """
    

    def extract(self):
        """This method allows us to decide what we do with the different
        options of our field. We handle the 3 options, here :
        keep, replace, delete.
        """
        action = self.request.form.get(self.identifier + '.action', None)
        if action == KEEP:
            # We return a marker that is understood by the form datamanager.
            value = NO_CHANGE
        elif action == DELETE:
            # We explicitly return None instead of  NO_VALUE
            # File storage should take this in consideration
            value = None
        else:
            # Return the value if it exists or a marker uderstood by the
            # form datamanager.
            value = self.request.form.get(self.identifier, NO_VALUE)
        return (value, None)
