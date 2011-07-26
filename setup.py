# -*- coding: utf-8 -*-

from os.path import join
from setuptools import setup, find_packages

name = 'dolmen.widget.file'
version = '2.0a1'
readme = open('README.txt').read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'dolmen.file >= 2.0a1',
    'grokcore.component',
    'setuptools',
    'dolmen.location',
    'zope.interface',
    'zope.size',
    'zope.i18n',
    'zope.location',
    'dolmen.forms.base',
    'dolmen.forms.ztk',
    'zope.i18nmessageid',
    ]

tests_require = [
    'zope.component',
    'zope.schema',
    'cromlech.browser [test]',
    ]

setup(name=name,
      version=version,
      description='File widget for Dolmen',
      long_description=readme + '\n\n' + history,
      keywords='Cromlech Dolmen Widget File',
      author='The Dolmen Team',
      author_email='dolmen@list.dolmen-project.org',
      url='http://gitweb.dolmen-project.org',
      license='ZPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages=['dolmen', 'dolmen.widget'],
      include_package_data=True,
      platforms='Any',
      zip_safe=False,
      tests_require=tests_require,
      install_requires=install_requires,
      extras_require={'test': tests_require},
      test_suite="dolmen.widget.file",
      classifiers=[
          'Environment :: Web Environment',
          'Programming Language :: Python',
          ],
      entry_points="""
      # -*- Entry points: -*-
      [dolmen.collection.components]
      file = dolmen.widget.file.widget:register
      """,
)
