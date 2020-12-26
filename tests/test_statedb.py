import mongomock
import pytest
import datetime

from mongodb_statedb import StateDb

DATABASE_NAME = 'mongodb_statedb'
COLLECTION_NAME = 'state'

STRING_KEY = 'user name'
STRING_VALUE = 'Audrow Nash'
NUMBER_KEY = 'difficulty'
NUMBER_VALUE = 1.0
DATE_KEY = 'last checkin'
DATE_VALUE = datetime.datetime(2021, 2, 3, 4, 5, 6)

TEST_KEYS = (STRING_KEY, NUMBER_KEY, DATE_KEY)
TEST_VALUES = (STRING_VALUE, NUMBER_VALUE, DATE_VALUE)

STATE_PAIRS = zip(TEST_KEYS, TEST_VALUES)


@pytest.fixture
def mongo_client():
    client = mongomock.MongoClient()
    db = client[DATABASE_NAME][COLLECTION_NAME]
    db.insert_many([
        {'_id': STRING_KEY, 'value': STRING_VALUE},
        {'_id': NUMBER_KEY, 'value': NUMBER_VALUE},
        {'_id': DATE_KEY, 'value': DATE_VALUE},
    ])
    return client


@pytest.fixture
def statedb(mongo_client):
    return StateDb(mongo_client)


def test_get_values(statedb):
    for key, value in STATE_PAIRS:
        assert statedb.exists(key)
        assert statedb.get(key) == value


def test_raise_on_get_and_set_bad_key(statedb):
    for bad_key in ['foo', 'bar', 'baz']:
        assert not statedb.exists(bad_key)
        with pytest.raises(KeyError):
            statedb.get(bad_key)
        with pytest.raises(KeyError):
            statedb.set(bad_key, 'foo value')


def test_set_keys(statedb):
    new_string = STRING_VALUE[::2]
    new_number = NUMBER_VALUE*3+1
    new_date = DATE_VALUE + datetime.timedelta(days=3)
    new_values = (new_string, new_number, new_date)
    for key, new_value in zip(TEST_KEYS, new_values):
        statedb.exists(key)
        statedb.set(key, new_value)
        assert statedb.get(key) == new_value


def test_create_keys(statedb):
    new_key = 'my new key'
    new_value = 42
    assert not statedb.exists(new_key)
    statedb.create(new_key, new_value)
    assert statedb.exists(new_key)
    assert statedb.get(new_key) == new_value


def test_cant_create_existing_key(statedb):
    for key in TEST_KEYS:
        assert statedb.exists(key)
        with pytest.raises(KeyError):
            statedb.create(key, 'foo value')


def test_delete_keys(statedb):
    assert len(statedb) == len(TEST_KEYS)
    for key in TEST_KEYS:
        assert statedb.exists(key)
        statedb.delete(key)
        assert not statedb.exists(key)
    assert len(statedb) == 0


def test_delete_all(statedb):
    assert len(statedb) == len(TEST_KEYS)
    statedb.delete_all()
    assert len(statedb) == 0
