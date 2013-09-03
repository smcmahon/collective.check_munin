from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='collective.check_munin',
      version=version,
      description="Nagios plugin to check munin via rrd",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Monitoring",
        "Intended Audience :: System Administrators",
        "Environment :: Plugins",
        "Development Status :: 5 - Production/Stable",
        ],
      keywords='',
      author='Steve McMahon',
      author_email='steve@dcn.org',
      url='https://github.com/smcmahon/collective.check_munin',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'nagiosplugin',
      ],
      entry_points= {
          'console_scripts' : [
              'check_munin = collective.check_munin.check_munin:main',
          ],
      },
      )
