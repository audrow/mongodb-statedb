mongodb-statedb
===============

Use MongoDB to track the state. For example, in robotics applications.

Features
--------
* Uses MongoDB to handle possible concurrency issues
* Create, Read, Update, and Delete (CRUD) database entries
* Enforces that there is only one entry for each key

Usage
-----

1. `Install MongoDB <https://docs.mongodb.com/manual/installation/>`_

1. Start a MongoDB server::

    cd your/mongodb
    mongod --dbpath . --port 62345

1. Clone this package and run the ``setup.py`` script::

    git clone https://github.com/audrow/mongodb-statedb
    cd mongodb-statedb
    python setup.py

1. Use a ``StateDb`` instance in your code to read and write to the MongoDB database. You can see an example in ``example.py``.

About mongodb-statedb
---------------------

``mongodb-statedb`` was created by `Audrow Nash <https://audrow.github.io/>`_ - `audrow@hey.com <audrow@hey.com>`_

Distributed under the MIT license. See ``LICENSE.txt`` for more information.
