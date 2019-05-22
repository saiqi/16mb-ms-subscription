import logging
import datetime

from nameko.rpc import rpc
from nameko.events import EventDispatcher
from nameko_mongodb.database import MongoDatabase
import bson.json_util

_log = logging.getLogger(__name__)


class SubscriptionError(Exception):
    pass


class SubscriptionManagerService(object):
    name = 'subscription_manager'

    database = MongoDatabase(result_backend=False)

    dispatch = EventDispatcher()

    @rpc
    def add_subscription(self, user, subscription):
        _log.info(f'Adding a subscription to {user} ...')
        self.database.subscriptions.update_one({'user': user},
            {'$set': {'subscription': subscription, 'modification_date': datetime.datetime.utcnow()}}, upsert=True)
        payload = {'user': user, 'subscription': subscription}

        self.dispatch('user_sub', payload)

    @rpc
    def get_subscription_by_user(self, user):
        cursor = self.database.subscriptions.find_one({'user': user}, {'_id': 0})
        return bson.json_util.dumps(cursor)
