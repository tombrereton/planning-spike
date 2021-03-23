#!/usr/bin/env python
from ukplanning import run
import json
import time

council = 'Chelmsford'
scraper_dict = run.all_scraper_classes()
if not council in scraper_dict.keys():
    print 'Scraper class not yet implemented for %s' % council
else:
    timerLogs = []

    print 'Found scraper class for %s' % council
    scraper = run.get_scraper(council, log_directory='logs')
    print 'Gathering Ids...'
    start = time.time()
    scraped = scraper.gather_ids('2021-02-01', ' 2021-02-02')
    end = time.time()

    if scraped.get('result'):

        planningIds = scraped['result']
        timerLog = "Found {0} planning applications from {1} to {2} in {3:6.2f} seconds".format(len(planningIds), scraped['from'], scraped['to'], end - start)
        print timerLog
        timerLogs.append(timerLog)

        plannings = []
        for planningId in planningIds[:10]:

            start = time.time()
            detailPage = scraper.get_application_details(planningId)
            end = time.time()
            elapsed = end - start

            if 'scrape_error' not in detailPage:
                record = detailPage["record"]
                timerLog = 'Planning record {0} fetched in {1:6.2f} seconds'.format(record["uid"], elapsed)
                print timerLog
                timerLogs.append(timerLog)
                plannings.append(record)
            else:
                print 'Error during application update: %s' % detailPage['scrape_error']

        outfile = open("./logs/data.json", "w")
        outfile.write(json.dumps(plannings))
        outfile.close()

        outfile = open("./logs/timings.json", "w")
        outfile.write(json.dumps(timerLogs))
        outfile.close()
    else:
        print 'Error when gathering applications: %s' % scraped['scrape_error']
