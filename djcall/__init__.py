from typing import Dict


class MockedUwsgi:
    """Mock uwsgi module within tests / when not running within uwsgi."""
    SPOOL_OK = -2
    SPOOL_RETRY = -1

    spoolers = []

    def spool(self, arg: Dict[bytes, str]) -> None:
        """Simulate uwsgi.spool by calling the spooler directly.

        Docs: https://uwsgi-docs.readthedocs.io/en/latest/Spooler.html#enqueueing-requests-to-a-spooler
        """  # noqa: E501
        uwsgi.spooler(arg)


try:
    import uwsgi
except ImportError:
    uwsgi = MockedUwsgi()

default_app_config = 'djcall.apps.DjcallConfig'
