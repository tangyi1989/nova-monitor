
import pymongo

from openwlee.openstack.common import cfg

mongo_opts = [
    cfg.StrOpt('mongodb_host', default = 'localhost', 
               help = 'Mongodb server host'),
    cfg.IntOpt('mongodb_port', default = 27017,
               help = 'Mongodb server port')
              ]

CONF = cfg.CONF
CONF.register_opts(mongo_opts)

def get_connection():
    host = CONF.mongodb_host
    port = CONF.mongodb_port
    
    return pymongo.Connection(host=host, port=port)

def get_database(db_name = 'wlee_db'):
    conn = get_connection()
    return conn[db_name]

def ensure_collction(collection_name, db_name = 'wlee_db', indexes=None, options=None):
    conn = get_connection()
    db = conn[db_name]
    
    if collection_name not in db.collection_names():
        db.create_collection(collection_name, options=options)
    
    coll = db[collection_name]
    if indexes != None:
        coll.ensure_index(indexes)

