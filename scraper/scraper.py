from BeautifulSoup import BeautifulSoup
import urllib3

class Scraper():
    """ A general scraper that uses BeautifulSoup """

    def get_response(self, url):
        http = urllib3.PoolManager()
        try:
            response = http.request('GET', url)
        except URLError, error:
            if hasattr(error, 'reason'):
                print 'Failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        else:
            print 'Retrieved response from the given url.'

        return response

    def prettify(self, response):
        data = response.data
        soup = BeautifulSoup(data)
        soup = soup.prettify()

        return soup

if __name__ == "__main__":
    # do some testing / use Nose later
    scraper = Scraper()
    response = scraper.get_response('http://google.com')
    print scraper.prettify(response)
