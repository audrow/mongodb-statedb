"""Use MongoDB to keep track of state."""

from pymongo import MongoClient
from typing import Any


class StateDb:
    """Wraps `pymongo` to make keeping track of state easy."""

    _VALUE_KEY = 'value'

    def __init__(
            self, mongo_client: MongoClient,
            database_name='mongodb_statedb',
            collection_name='state',
    ):
        """
        Constructor for the ``StateDb`` class.

        :param mongo_client: A connected MongoDB client.
        :param database_name:  The MongoDB database to use.
        :param collection_name:   The collection in the database to use.
        """
        self._db = mongo_client[database_name][collection_name]

    def get(self, key: str) -> Any:
        """
        Get the stored value of a key, if it exists.

        :param key: The unique key in the database.
        :return: The value stored for that key.
        """
        self._throw_error_if_key_doesnt_exist(key)
        return self._db.find_one({'_id': key})[self._VALUE_KEY]

    def get_all_as_dict(self):
        collection_contents = self._db.find({})
        collection_contents_as_dict = {}
        for document in collection_contents:
            key = document['_id']
            value = document[self._VALUE_KEY]
            collection_contents_as_dict[key] = value
        return collection_contents_as_dict

    def set(self, key: str, value: Any) -> None:
        """
        Set the stored value for a key, if it exists.

        :param key: The unique key in the database.
        :param value: The value you wish to associate with the key.
        """
        self._throw_error_if_key_doesnt_exist(key)
        self._db.update_one(
            {'_id': key},
            {'$set': {self._VALUE_KEY: value}})

    def _throw_error_if_key_doesnt_exist(self, key: str) -> None:
        if not self.exists(key):
            raise KeyError(f'Key "{key}" does not exist')

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in the database.

        :param key: The unique key in the database.
        :return:
        """
        return self._db.find_one({'_id': key}) is not None

    def is_set(self, key: str) -> bool:
        """Check if a key exists in the database and its value is not None."""
        return self.exists(key) and self.get(key) is not None

    def create(self, key: str, value: Any) -> None:
        """
        Add a new key-value pair in the MongoDB collection used.

        :param key: The unique key in the database.
        :param value: The value you wish to associate with the key.
        """
        if self.exists(key):
            raise KeyError(f'Key "{key}" already exists')
        self._db.insert_one({'_id': key, self._VALUE_KEY: value})

    def delete(self, key: str) -> None:
        """
        Delete a key from the MongoDB collection used.

        :param key:
        """
        self._throw_error_if_key_doesnt_exist(key)
        self._db.delete_one({'_id': key})

    def delete_all(self) -> None:
        """Delete all of the key-value pairs stored in the used collection."""
        self._db.drop()

    def clear(self, key: str) -> None:
        """
        Set the value of the specified key to None.

        :param key:
        """
        self.set(key, None)

    def clear_all(self) -> None:
        """Set the value of every key in the used collection to None."""
        for document in self._db.find({}):
            self.clear(document['_id'])

    def __len__(self) -> int:
        """Get the number of keys in the MongoDB collection used."""
        return self._db.estimated_document_count()

    def __contains__(self, key: str) -> bool:
        return self.exists(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.set(key, value)

    def __getitem__(self, key: str) -> Any:
        return self.get(key)
