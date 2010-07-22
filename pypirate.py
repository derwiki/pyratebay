import BeautifulSoup
import urllib2
import sys


class PyPirate(object):
	tpb_search_url = 'http://thepiratebay.org/search/%s/0/7/100'

	def _get_page_descriptor(self, query):
		print "Using query: %s" % (repr(query))
		tpb_search_url = self.tpb_search_url % '+'.join(query)
		return urllib2.urlopen(tpb_search_url)


	def __init__(self, query):
		page_contents = '\n'.join(self._get_page_descriptor(query).readlines())
		bs = BeautifulSoup.BeautifulSoup(page_contents)


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'usage'
		sys.exit(-1)

	PyPirate(sys.argv[1:])
