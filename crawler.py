#!/usr/bin/env python
from ukplanning import run
import json
import time
from ukplanning.scrapers.dates import idox
from ukplanning.scrapers import base
import collections
import sys

scraper_dict = run.all_scraper_classes(parent_class=base.DateScraper)
# scraper_dict = run.all_scraper_classes(parent_class=base.ListScraper)
# scraper_dict = run.all_scraper_classes(parent_class=base.PeriodScraper)
ordered_scrapers = collections.OrderedDict(sorted(scraper_dict.items()))

timingLogFile = "./logs/timings.log"
plannings = []
count = 0

totalScrapers = '{0} total scrapers found for type {1}\n'.format(len(scraper_dict), base.DateScraper.__name__)
print totalScrapers
with open(timingLogFile, 'a') as f:
    f.write(totalScrapers)

for council in ordered_scrapers:
    try:
        count = count + 1
        foundScraper = '{0} scraper, number {1}\n'.format(council, count)
        print foundScraper
        with open(timingLogFile, 'a') as f:
            f.write(foundScraper)
        scraper = run.get_scraper(council, log_directory='logs')
        print 'Gathering Ids for %s ...' % council
        start = time.time()
        scraped = scraper.gather_ids('2021-02-01', ' 2021-02-02')
        end = time.time()

        if scraped.get('result'):

            planningIds = scraped['result']
            timerLog = "{0} scraper found {1} planning applications from {2} to {3} in {4:6.2f} seconds\n".format(
                council, len(planningIds), scraped['from'], scraped['to'], end - start)
            print timerLog
            with open(timingLogFile, 'a') as f:
                f.write(timerLog)

            for planningId in planningIds[:1]:

                start = time.time()
                detailPage = scraper.get_application_details(planningId)
                end = time.time()
                elapsed = end - start

                if 'scrape_error' not in detailPage:
                    record = detailPage["record"]
                    timerLog = '{0} scraper, planning record {1} fetched in {2:6.2f} seconds\n'.format(council, record["uid"], elapsed)
                    print timerLog
                    with open(timingLogFile, 'a') as f:
                        f.write(timerLog)
                    plannings.append(record)
                else:
                    detailError = '{0} scraper, Error during application update: {1}\n'.format(council, detailPage[
                        'scrape_error'])
                    print detailError
                    with open(timingLogFile, 'a') as f:
                        f.write(error)

            outfile = open("./logs/data.json", "w")
            outfile.write(json.dumps(plannings))
            outfile.close()
        else:
            error = '{0} scraper, Error when gathering applications: {1}\n'.format(council, scraped['scrape_error'])
            print error
            with open(timingLogFile, 'a') as f:
                f.write(error)
    except Exception as e:
        exc = '{0} scraper, Error, threw exception {1}\n'.format(council, e)
        print exc
        with open(timingLogFile, 'a') as f:
            f.write(exc)
