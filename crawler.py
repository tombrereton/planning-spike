#!/usr/bin/env python
from ukplanning import run
import json

scraper = 'Chelmsford'
scraper_dict = run.all_scraper_classes()
if not scraper in scraper_dict.keys():
    print 'Scraper class not yet implemented for %s' % scraper
else:
    print 'Found scraper class for %s' % scraper
    scraper_obj = run.get_scraper(scraper, log_directory='logs')
    print 'Wait ...'
    # scraped = scraper_obj.gather_ids('2021-02-01', ' 2021-02-02')
    # if scraped.get('result'):
    #     result = scraped['result']
    #     print "Found %d planning applications from %s to %s" % (len(result), scraped['from'], scraped['to'])
    #     planningSummary = result[0]
    planningSummary = {}
    planningSummary['uid'] = '21/00219/FUL'
    planningDetails = scraper_obj.get_application_details(planningSummary)
    if 'scrape_error' not in planningDetails:
        print 'Updated first full record from %s' % scraper
        print planningDetails
        print json.dumps(planningDetails)
        print 'OK'
    else:
        print 'Error during application update: %s' % planningDetails['scrape_error']
    # else:
    #     print 'Error when gathering applications: %s' % scraped['scrape_error']
