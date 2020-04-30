Requirements
============

Upgrade from v0.3 to v0.4
=========================

As of v0.4, djcall uses a PostgreSQL JSON field instead of a Picklefield for
Caller.kwargs, which means that unless you have only JSON serializable contents
in your djcall_caller.kwargs columns: the migration will fail, so will it if
you don't run PostgreSQL. Sorry, but it became too much of an annoyance not to
be able to query of Call kwargs. Anyway, a migration should take care of this
for you. It leaves the old Picklefield renamed from kwargs to old_kwargs until
next release where it will be dropped.

Install
=======

pip install djcall

Add djcall to INSTALLED_APPS and migrate.

Usage
=====

.. code-block:: python

    from djcall.models import Caller

    Caller(
        # path to python callback
        callback='djblockchain.tezos.transaction_watch',
        # JSON serializable kwargs
        kwargs=dict(
            pk=transaction.pk,
        ),
    ).spool('blockchain')  # optionnal spooler name

No decorator, no nothing,

If you have CRUDLFA+ or django.contrib.admin, you should see the jobs there,
and be able to cancel them.

Example project
===============

Setup example project::

    djcall-example collectstatic
    djcall-example migrate
    djcall-example createsuperuser

Run with runserver::

    djcall-example runserver

Or with uWSGI::

    uwsgi --env DJANGO_SETTINGS_MODULE=djcall_example.settings --env DEBUG=1 --spooler=/spooler/blockchain --spooler=/spooler/mail --spooler-processes 1 --http=:8000 --plugin=python --module=djcall_example.wsgi:application --honour-stdin --static-map /static=static

History
=======

First made a dead simple pure python generic spooler for uwsgi:
https://gist.github.com/jpic/d28333b0573c3c555fbe6e55862ecddb

The made a first implementation including CRUDLFA+ support:
https://github.com/yourlabs/django-uwsgi-spooler

This version adds:

- Cron model and support for uWSGI cron, can't add/remove them without restart,
  but can change kwargs and options online
- CRUDLA+ support is on hold waiting for what's currently in
  https://github.com/tbinetruy/CHIP because i don't want to build crud support
  here with templates because of the debt this will add, it's time to use
  components in CRUDLFA+ to make the CRUD for Cron/Background tasks awesome
