import setuptools
import os

project_url = 'http://github.com/Quantmatic/iq2mongo/'

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    if os.path.exists('README.md'):
        long_description = open('README.md').read()
    else:
        long_description = 'IQFeed / DTN Data downloader. See details at: %s' % project_url

setuptools.setup(name='iq2mongo',
                 version='0.0.1',
                 description='IQFeed / DTN Data downloader',
                 long_description=long_description,
                 classifiers=[
                             'Development Status :: 1 - Beta',
                             'License :: OSI Approved :: Apache Software License',
                             'Programming Language :: Python :: 2.7',
                             'Topic :: Office/Business :: Financial :: Investment',

                 ],
                 url=project_url,
                 author='Alex Orion',
                 author_email='',
                 license='Apache License, Version 2.0',
                 packages=setuptools.find_packages(),
                 install_requires=['pandas', 'pymongo'],
                 entry_points={'console_scripts': ['']},
                 zip_safe=False)
