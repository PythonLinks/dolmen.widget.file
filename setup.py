from setuptools import setup, find_packages
from os.path import join

name = 'dolmen.widget.file'
version = '0.2dev'
readme = open(join('src', 'dolmen', 'widget', 'file', 'README.txt')).read()
history = open(join('docs', 'HISTORY.txt')).read()

install_requires = [
    'setuptools',
    'dolmen.file>=0.1',
    'megrok.z3cform.base>=0.1',
    'z3c.form>=2.1',
    'grokcore.component',
    'zope.size',
    'zope.component',
    'zope.interface',
    'zope.traversing',
    ]

tests_require = install_requires + [
    'zope.testing',
    'zope.app.testing',
    'zope.app.zcmlfiles',
    ]

setup(name = name,
      version = version,
      description = 'File widget for z3c.form, using Grok',
      long_description = readme + '\n\n' + history,
      keywords = 'Grok Zope3 Dolmen Widget File',
      author = 'Souheil Chelfouh',
      author_email = 'trollfot@gmail.com',
      url = '',
      license = 'GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir={'': 'src'},
      namespace_packages = ['dolmen', 'dolmen.widget'],
      include_package_data = True,
      platforms = 'Any',
      zip_safe = False,
      tests_require = tests_require,
      install_requires = install_requires,
      extras_require = {'test': tests_require},
      test_suite="dolmen.widget.file",
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Zope3',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ],
)
