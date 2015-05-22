from pprint import pprint

import numpy
import random
import redis
import argparse
from sklearn import cluster
from sklearn import metrics
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import pairwise_distances

def vectorize_key(key):
    return dict(enumerate(key.split(':')))

def unvectorize_key(key):
    return ':'.join(key.values())

def clusterize_keys(keys_vector, dbname):
    vectorizer = DictVectorizer()
    X = vectorizer.fit_transform(keys_vector)

    if dbname == 'kmeans':
        db = cluster.KMeans(n_clusters=10)
    else:
        X = pairwise_distances(X, metric='cosine')
        db = cluster.DBSCAN(min_samples=1)

    print "Feature len: {}".format(len(vectorizer.get_feature_names()))
    db.fit(X)

    labels = db.labels_
    nb_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    print 'Number of cluster found: {}'.format(nb_clusters)

    return labels


parser = argparse.ArgumentParser(description="Configuration for redis stats")
parser.add_argument('-r', '--redis-host',
        default='luke2.mapado.com', help='Redis hostname (default: localhost)')
parser.add_argument('-p', '--redis-port', type=int,
        default=6379, help='Redis port (default: 6379)')
parser.add_argument('--max-keys', type=int,
        default=None, help='Redis port (default: None)')


args = parser.parse_args()
print args

redis = redis.StrictRedis(host=args.redis_host, port=args.redis_port)

keys = redis.keys()
print "Keys OK: {}".format(len(keys))

keys_vector = [vectorize_key(key) for key in keys]

if args.max_keys:
    random.shuffle(keys_vector)
    keys_vector = keys_vector[:args.max_keys]

# X = pairwise_distances(X, metric='cosine')
# db = cluster.DBSCAN()

# import ipdb; ipdb.set_trace()

labels =clusterize_keys(keys_vector, 'kmeans')

groups = {}
keys_map = {}
for index, c in enumerate(labels):
    if c == -1:
        continue

    key = unvectorize_key(keys_vector[index])

    if not keys_map.get(c):
        keys_map[c] = key
        groups[key] = 1
    else:
        groups[keys_map[c]] += 1

pprint(groups)


second_keys = [vectorize_key(key) for key in groups.keys()]

labels = clusterize_keys(second_keys, 'dbscan')

out = {}
for index, c in enumerate(labels):
    key = unvectorize_key(second_keys[index])
    if not groups.get(c):
        out[c] = {
            'example': key,
            'number': groups[key]
        }
    else:
        out[c]['number'] += groups[key]

pprint(out)

#Y = vectorizer.fit_transform(second_keys)
#Y = pairwise_distances(Y, metric='cosine')
#dby = cluster.DBSCAN()
#dby.fit(Y)
#
