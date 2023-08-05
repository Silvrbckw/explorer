import re
import random

from blockexplorer.settings import BASE_URL


def get_max_pages(num_items, items_per_page):
    if num_items < items_per_page:
        return 1
    elif num_items % items_per_page == 0:
        return num_items // items_per_page
    else:
        return num_items // items_per_page + 1


def get_client_ip(request):
    """
    Get IP from a request
    """
    return (
        x_forwarded_for.split(',')[0]
        if (x_forwarded_for := request.META.get('HTTP_X_FORWARDED_FOR'))
        else request.META.get('REMOTE_ADDR')
    )


def get_user_agent(request):
    return request.META.get('HTTP_USER_AGENT')


def is_good_status_code(status_code):
    return str(status_code).startswith('2')


def assert_good_status_code(status_code):
    err_msg = f'Expected status code 2XX but got {status_code}'
    assert is_good_status_code(status_code), err_msg


def simple_csprng(num_chars=32, eligible_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKMNPQRSTUVWXYZ23456789'):

    """
    Generate a random password using the characters in `chars` and with a length of `num_chars`.

    http://stackoverflow.com/a/2257449

    Cryptographically secure but may not work on all OSs.
    Shouldn't cause blocking but it's possible.
    """
    return ''.join(
        random.SystemRandom().choice(eligible_chars) for _ in range(num_chars)
    )


def simple_pw_generator(num_chars=10, eligible_chars='abcdefghjkmnpqrstuvwxyz23456789'):
    """
    Generate a random password using the characters in `chars` and with a
    length of `size`.

    http://stackoverflow.com/a/2257449
    """
    return ''.join(random.choice(eligible_chars) for _ in range(num_chars))


def uri_to_url(uri, base_url=BASE_URL):
    """
    Take a URI and map it a URL:
    /foo -> http://coinsafe.com/foo
    """
    if not uri:
        return base_url
    return f'{base_url}{uri}' if uri.startswith('/') else f'{base_url}/{uri}'


def cat_email_header(name, email):
    assert '@' in email
    return f'{name} <{email}>' if name else email


def split_email_header(header):
    if '<' in header and '>' in header:
        name, email = re.findall('(.*)<(.*)>', header)[0]
    else:
        name = None
        email = header
    assert '@' in email
    return name, email
