from functools import wraps
from flask import request
import memcache

mc = memcache.Client(['127.0.0.1:11211'], debug=0)

def rate_limit(limitPeriod, connsPerPeriod):
	def wrapper(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			ip = str(request.headers.getlist("X-Real-IP")[0])
			numRequests = mc.get(ip)
			if not numRequests:
				mc.set(ip, "1", int(limitPeriod))
				numRequests = "1"
			mc.incr(ip)
			if (int(numRequests) > int(connsPerPeriod)):
				return "You have been rate limited, try again in a few seconds (%s requests)" % numRequests, 429
			return f(*args, **kwargs)
		return wrapped
	return wrapper
