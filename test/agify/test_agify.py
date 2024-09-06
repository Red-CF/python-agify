import pytest

from agify import Agify, AgifyException


def test_batch_process_should_retrieve_ages_ok():
    # Given
    expected_genders = {
        'Abraham': 61,
        'Eufrassio': 39,
        'Martino Delfino': 58,
    }

    # When
    actual_genders = dict((elem['name'], elem['age']) for elem in Agify().get_many(expected_genders.keys()))

    # Then
    assert expected_genders == actual_genders, "Expected {0}, got {1}".format(expected_genders, actual_genders)


def test_get_one_should_retrieve_one_age_ok():
    # Given
    expected = 'male'

    # When
    actual = Agify().get_one('Peter')['age']

    # Then
    assert expected == actual, "Expected {0}, got {1}".format(expected, actual)


def test_exception_is_thrown_when_apikey_is_null():
    # Given
    caught = False
    try:
        # When
        Agify(api_key='invalid_api_key').get_one('Bernardino')
    except AgifyException:
        caught = True
    # Then
    assert caught, "Expected a AgifyException to be thrown"


def test_with_headers():
    """
    Retrieve a single name with response headers.
    """
    response = Agify().get_many(['Peter'], None, True)
    assert response['data'][0]['name'] == 'Peter', \
        "Expected name data to be returned"
    assert response['headers'], "Expected response headers to be returned"
    expected_headers = [
        'X-Rate-Limit-Limit',
        'X-Rate-Limit-Remaining'
    ]
    for header in expected_headers:
        assert header in response['headers'], \
            "Expected {0} header to be returned".format(header)


def test_chunked_full_blocks():
    """
    Test chunking when the input length is a multiple of the block length.
    """
    chunks = list(Agify()._collect_chunks("abcd", 2))
    assert len(chunks) == 2
    assert len(chunks[0]) == 2
    assert len(chunks[1]) == 2


def test_chunked_uneven_blocks():
    """
    Test chunking when the input length isn't a multiple of the block length.
    """
    chunks = list(Agify()._collect_chunks("abcde", 2))
    assert len(chunks) == 3
    assert len(chunks[0]) == 2
    assert len(chunks[1]) == 2
    assert len(chunks[2]) == 1


def test_chunked_empty():
    """
    Test chunking when the input is empty.
    """
    chunks = list(Agify()._collect_chunks("", 2))
    assert len(chunks) == 0


@pytest.mark.parametrize(
    "names",
    [
        (["Bad", "Myke", "Bunny", "Towers", "Don", "Alvaro", "Omar", "Diez", "Rosalia", "Toki", "Rauw", "Julieta"]),
        (["John", "Jane", "Doe", "Smith", "Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Bobby", "Emilio", "Arcangel", "Juan Emilio"]),
    ]
)
def test_when_using_more_than_10_names_should_make_another_request(names):
    """
    Test that when using more than 10 names, multiple HTTP requests are made.
    """
    # When
    response = Agify().get_many(names)

    # Then
    assert len(names) == len(response), 'Expected response length to match names'
    for name, data in zip(names, response):
        assert name == data['name'], 'Expected names to be returned'
