from setuptools import setup, find_packages
import sys, os

version = '0.1'

readme = open('README.txt').read()

setup(name='django-inactive_user_workflow',
      version=version,
      description=("tools to let inactive users log in to your site "
                   "with limited access after registration "
                   "until they confirm their account"),
      long_description=readme,
      classifiers=['Framework :: Django'],
      keywords='django registration',
      author='Ethan Jucovy',
      author_email='ethan.jucovy@gmail.com',
      url='',
      license='GPLv3 or greater',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'djangohelpers',
          'django-registration',
      ],
      entry_points="""
      """,
      )
