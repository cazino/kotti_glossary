import os

from setuptools import find_packages
from setuptools import setup

version = '0.1dev'

here = os.path.abspath(os.path.dirname(__file__))

README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

install_requires = [
    'Kotti',
    'BeautifulSoup'
]


setup(
    name='kotti_glossary',
    version=version,
    description='',
    long_description='',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Pylons',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'License :: Repoze Public License',
    ],
    keywords='kotti',
    author='Emmanuel Cazenave',
    author_email='emmanuel.cazenave@gmail.com',
    url='https://github.com/cazino/kotti_glossary',
    license='BSD-derived (http://www.repoze.org/LICENSE.txt)',
    packages=find_packages(exclude=[
        'ez_setup',
        'examples',
        'tests'
    ]),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require={},
    test_suite="kotti_glossary.tests",
    message_extractors={
        'kotti_media': [
            ('**.py', 'lingua_python', None),
            ('**.zcml', 'lingua_xml', None),
            ('**.pt', 'lingua_xml', None),
        ],
    },
    entry_points={
    }
)
