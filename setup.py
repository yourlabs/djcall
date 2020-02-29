from setuptools import setup


setup(
    name='djcall',
    versioning='dev',
    setup_requires='setupmeta',
    description='Leverage uWSGI spooler and cron in Django',
    author='James Pic',
    author_email='jpic@yourlabs.org',
    url='https://yourlabs.io/oss/djcall',
    include_package_data=True,
    keywords='django uwsgi cache spooler',
    install_requires=[
        'django-picklefield',
    ],
    extras_require=dict(
        django=[
            'django-threadlocals',
            'django-ipware',
        ],
        example=[
            'django>=2.0',
            'crudlfap>=0.7.1',
        ],
    ),
    entry_points={
        'console_scripts': [
            'djcall-example = djcall_example.manage:main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
