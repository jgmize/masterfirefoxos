from django.test import RequestFactory
from django.test.utils import override_settings

from .. import views


@override_settings(
    LOCALE_LATEST_VERSION={
        'de': {'slug': '1-1', 'name': '1.1'},
        'en': {'slug': '1-3T', 'name': '1.3T'}
    })
def test_home_redirect_de():
    request = RequestFactory().get('/de/')
    request.LANGUAGE_CODE = 'de'  # normally added by LocaleMiddleware
    response = views.home_redirect(request)
    assert response.status_code == 302
    assert response['location'] == '1-1/'


@override_settings(
    LOCALE_LATEST_VERSION={},
    LOCALE_LATEST_PENDING_VERSION={'xx': {'slug': '4-2', 'name': '4.2'}},
    ENABLE_ALL_LANGUAGES=True)
def test_home_redirect_pending_version():
    request = RequestFactory().get('/xx/')
    request.LANGUAGE_CODE = 'xx'  # normally added by LocaleMiddleware
    response = views.home_redirect(request)
    assert response.status_code == 302
    assert response['location'] == '4-2/'


@override_settings(LOCALE_LATEST_VERSION={'en': {'slug': '1-3T', 'name': '1.3T'}},
                   ENABLE_ALL_LANGUAGES=False)
def test_home_redirect_english_default():
    request = RequestFactory().get('/de/')
    request.LANGUAGE_CODE = 'de'  # normally added by LocaleMiddleware
    response = views.home_redirect(request)
    assert response.status_code == 302
    assert response['location'] == '/en/1-3T/'
