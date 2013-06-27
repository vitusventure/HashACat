from functools import wraps
from flask import request
import memcache

mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def rate_limit(limitPeriod, connsPerPeriod, domain):
	def wrapper(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			keyID = str(request.headers.getlist("X-Real-IP")[0]) + domain
			numRequests = mc.get(keyID)
			if not numRequests:
				mc.set(keyID, "1", int(limitPeriod))
				numRequests = "1"
			mc.incr(keyID)
			if (int(numRequests) > int(connsPerPeriod)):
				return "You have been rate limited, try again in a few seconds (%s requests)" % numRequests, 429
			return f(*args, **kwargs)
		return wrapped
	return wrapper
