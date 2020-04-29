import pytest

from djcall.models import Call, Caller, Cron, spooler


def mockito(**kwargs):
    exception = kwargs.get('exception')
    if exception:
        raise exception
    subcalls = kwargs.get('subcalls')
    if subcalls:
        for subcall in subcalls:
            Call(
                callback='djcall.test_models.mockito',
                kwargs=dict(id=subcall),
            )
    return kwargs.get('id', None)


@pytest.mark.django_db(transaction=True)
def test_call_execute_result():
    call = Caller(
        callback='djcall.test_models.mockito',
        kwargs=dict(id=1),
    ).call()
    assert call.result == 1
    assert call.status == call.STATUS_SUCCESS
    assert call.caller.status == call.STATUS_SUCCESS


@pytest.mark.django_db(transaction=True)
def test_call_execute_exception():
    caller = Caller(
        callback='djcall.test_models.mockito',
        kwargs=dict(exception=Exception('lol')),
    )
    with pytest.raises(Exception):
        caller.call()
    call = caller.call_set.last()
    assert call.status == call.STATUS_FAILURE
    assert call.caller.status == call.STATUS_RETRYING
    assert call.result is None
    assert call.exception.startswith('Traceback')
    assert 'raise exception' in call.exception


@pytest.mark.django_db(transaction=True)
def test_spool():
    # tests spool() call works outside uwsgi (we're in py.test)
    caller = Caller.objects.create(
        callback='djcall.test_models.mockito',
        kwargs=dict(exception=Exception('lol')),
    )

    with pytest.raises(Exception):
        caller.spool()


@pytest.mark.django_db(transaction=True)
def test_uwsgi_spooler():
    # test uwsgi spooler
    caller = Caller.objects.create(
        callback='djcall.test_models.mockito',
        kwargs=dict(exception=Exception('lol')),
        max_attempts=2,
    )

    call = caller.call_set.create()
    kwargs = {b'call': call.pk}
    with pytest.raises(Exception):
        spooler(kwargs)

    # The call should be marked as failed
    call.refresh_from_db()
    assert call.status == call.STATUS_FAILURE

    # But max_attempt not reached, caller should be marked retrying
    caller.refresh_from_db()
    assert caller.status == caller.STATUS_RETRYING

    # Simulate retry by uWSGI, caused by Exception raise of spooler()
    call = caller.call_set.create()
    kwargs = {b'call': call.pk}
    assert spooler(kwargs)

    # this is attempt 2 of 2 so it should settle with FAILURE
    caller.refresh_from_db()
    assert caller.status == caller.STATUS_FAILURE


def test_cron_matrix():
    cron = Cron(
        minute='1-2',
        hour=1,
        day=1,
        month='*',
        weekday='*',
    )

    assert cron.get_matrix() == [
        (1, 1, 1, -1, -1),
        (2, 1, 1, -1, -1),
    ]


def test_python_callback():
    caller = Caller(callback='djcall.models.Caller.objects.all')
    assert caller.python_callback == Caller.objects.all

    caller = Caller(callback='doesnotexit.foobar')
    with pytest.raises(ModuleNotFoundError,
                       match="No module named 'doesnotexit'"):
        caller.python_callback


def test_str():
    assert str(Caller(callback='lol')) == 'lol()'
    assert str(
        Caller(callback='lol', kwargs=dict(a=1, b=2))
    ) == 'lol(a=1, b=2)'
