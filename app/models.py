from config import WHOOSH_ENABLED

enable_search = WHOOSH_ENABLED
if enable_search:
	import flask_whooshalchemy as whooshalchemy

# ...
if enable_search:
	whooshalchemy.whoosh_index(app, Post)