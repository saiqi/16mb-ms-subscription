import pytest
from pymongo import MongoClient
import bson.json_util
from nameko.testing.services import worker_factory
from application.services.subscription_manager import SubscriptionManagerService, SubscriptionError


@pytest.fixture
def database(db_url):
    client = MongoClient(db_url)

    yield client['test_db']

    client.drop_database('test_db')
    client.close()


def test_add_subscription(database):
    service = worker_factory(SubscriptionManagerService, database=database)
    service.add_subscription('foo', {'myfeed': True})

    result = database.subscriptions.find_one({'user': 'foo'})
    assert result
    assert result['modification_date']
    assert result['user'] == 'foo'
    assert result['subscription']
    assert result['subscription']['myfeed']


def test_get_subscription_by_user(database):
	service = worker_factory(SubscriptionManagerService, database=database)
	database.subscriptions.insert_one({'user': 'foo', 'subscription': {'myfeed': True}})

	sub = bson.json_util.loads(service.get_subscription_by_user('foo'))
	assert sub
	assert sub['user'] == 'foo'
	assert sub['subscription']
	assert sub['subscription']['myfeed']

