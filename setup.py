import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_urireferencer',
    'requests',
    'PyYAML'
    ]

setup(name='uriregistry',
      version='0.1.2',
      description='A central URI registry that tracks where a certain URI is being used.',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Flanders Heritage Agency',
      author_email='ict@onroerenderfgoed.be',
      url='http://uriregistry.readthedocs.org',
      license='GPLv3',
      keywords='web wsgi pyramid uri',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='uriregistry',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = uriregistry:main
      """,
      )
