from django import apps

try:
    import uwsgi
except ImportError:
    uwsgi = None


class DjcallConfig(apps.AppConfig):
    name = 'djcall'

    def ready(self):
        if not uwsgi:
            return
        from .models import setup
        try:
            setup()
        except Exception as e:
            print(e)
            print('Could not register cron objects to uWSGI')
