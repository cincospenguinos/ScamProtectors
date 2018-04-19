# email_cronjob

The cron job that will grab emails and modify them if they are faulty.

## How to run this

1. `source ../bin/activiate`
2. `python [name of file].py`
3. ??????????
4. Profit

## Plan

1. Get access to VTU's email account
	* I'll need to use the [Gmail API](https://developers.google.com/gmail/api/quickstart/python).
	* I'll need to find a way to get access to a VTU's account
2. Grab all the mail messages that we haven't seen before
	* I may need a DB table that maps email accounts to seen email IDs or something to that effect
3. Scan each one with our classifier
	* Pull up the classifier from disk
	* Run it against the DB
4. If one of them matches, flag it.
	* Again, check Gmail's API

## Features of this portion

* Multithreaded to ensure that we get every user super fast
* Put on a cron job so it's done regularly