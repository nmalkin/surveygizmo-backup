SurveyGizmo backup tools
========================

This is a set of scripts that helps you export your surveys from SurveyGizmo.
Specifically, they automate the download of the data CSV and PDF and Word exports for all of your surveys.
That export functionality is accessible through the website, but there isn't a way to perform these actions in bulk.
These scripts address that need.

Warning
-------
This code doesn't use formal APIs; it's reverse-engineered from the SG website.
As such, it's liable to be more brittle and break without notice.
It worked as of September 2017.

Prerequisites
--------------
You need Python 3.6+ and the single required Python package,
which you can get with `pip install -r requirements.txt`.

Usage
-----

1. Log in to SurveyGizmo and go to your dashboard
2. Click "Download Survey List" near the bottom of the page to export a list of all your surveys. We use it to get the IDs of all the surveys. Note that this button [is available to account administrators only](https://help.surveygizmo.com/help/project-list).
3. Put that CSV in the `surveygizmo` directory below this code, naming it `all_surveys.csv`.
4. The code piggy-backs on your existing session cookies to run. The easiest way to get them is to open your browser's Developer Tools, go to the Network panel, and make a request (e.g., refresh the dashboard page). Click on one of the requests and click on the Cookies tab (or equivalent). There will be two you need, `PHPSESSID` and `appsact`.
5. Make the cookie values available to the scripts: `export PHPSESSID=<value>;export APPSACT=<other value>`
6. Now you should be ready to go. Download all your surveys with `python download_all.py`.
7. Note that the code runs several downloads in parallel to speed things up. If that's not working, or you don't need the parallelism, you can change that easily; see `download_all.py`.
