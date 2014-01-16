import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
    'markdown',
    'WebTest',
    'pyramid_persona',
    'pyatom',
    'psycopg2',
    'pyramid_chameleon',
    ]

setup(name='Writers_Choice',
      version='1.4',
      description='Writers_Choice',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Anton Eliasson',
      author_email='devel@antoneliasson.se',
      url='http://www.antoneliasson.se',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='writers_choice',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = writers_choice:main
      [console_scripts]
      initialize_Writers_Choice_db = writers_choice.scripts.initializedb:main
      """,
      )
