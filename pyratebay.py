#!/usr/bin/python
import BeautifulSoup
import urllib2
import re
import sys


class PyPirate(object):
	tpb_search_url = 'http://thepiratebay.org/search/%s/0/7/0'

	def _get_page_descriptor(self, query):
		tpb_search_url = self.tpb_search_url % '+'.join(query)
		return urllib2.urlopen(tpb_search_url)

	def _parse_search_results(self, page, hide_noseeds=True, limit=None):
		bs = BeautifulSoup.BeautifulSoup(page)

		regex = re.compile('Size (.*)&nbsp;(.*),')

		# first row has TH information, skip that
		for row in bs.findAll('tr')[1:]:
			torrent_href = row.findChild(attrs=dict(title="Download this torrent"))
			torrent = str(torrent_href.attrMap.get('href'))

			size_td = row.findChild(attrs={'class':'detDesc'})
			size, scale = regex.findall(repr(size_td))[0]

			seeds_and_leeches = row.findChildren(attrs=dict(align='right'))
			seeds, leeches = [int(td.string) for td in seeds_and_leeches]
			#import ipdb; ipdb.set_trace()
			if seeds == 0:
				continue
			else:
				yield (torrent, seeds, leeches, ' '.join((size, scale)))
				if limit is not None:
					limit -= 1
					if limit == 0:
						break

	def __init__(self, query, lucky=False):
		fd = self._get_page_descriptor(query)
		page_contents = '\n'.join(fd.readlines())
		fd.close()
		self.results = list(self._parse_search_results(page_contents, limit=(1 if lucky else None)))
		self.results.reverse()

	def __repr__(self):
		return '\n'.join('%s (%d seeds / %d leeches)\n%s' % (size.ljust(10), seeds, leeches, torrent) for torrent, seeds, leeches, size in self.results)

def usage():
	return ('Usage:\n'
		'All results: python ./pypirate.py my search query\n'
		'Top result:  python ./pypirate.py --lucky my search query\n'
	)


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print usage()
		sys.exit(-1)

	lucky = False
	if sys.argv.count('--lucky') > 0:
		sys.argv.remove('--lucky')
		lucky = True

	testing = False
	if sys.argv.count('--testing'):
		sys.argv.remove('--testing')
		for test_file in ('test/%s' % file for file in ('100', '100.1', '100.2', '100.3', '100.4')):
			# monkey patch the file descriptor loading function
			PyPirate._get_page_descriptor = lambda x, y: open(test_file, 'r')
			print PyPirate(sys.argv[1:], lucky=lucky)
	else:
		#print "Using query: %s" % (repr(query))
		print PyPirate(sys.argv[1:], lucky=lucky)
