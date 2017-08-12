
Log Analysis Project for Udacity Full-Stack Nanodegree Program

Author: Jonathan Prell
v1.0	8/11/2017
_________________________________________________________________

The log_analysis.py file uses SQL queries on a PostgreSQL database for online news articles to answer three simple questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?
_________________________________________________________________

Instructions:

Run log_analysis.py in vagrant virtual machine with newsdata.sql pre-run.
_________________________________________________________________

The 'news' database contains three tables:

Articles:
Column	Type
author 	integer (foreign key with Authors ID)
title	text
slug	text
lead	text
body	text
time	timestamp with time zone
id		integer (primary key)

Authors:
Column	Type
name	text
bio		text
id		integer (primary key; referenced key with Articles: Author)

Log:
Column	Type
path	text
ip		inet
method	text
status	text
time 	timestamp with time zone
id 		integer (primary key)

_________________________________________________________________

Question 1 Solution:

	Joined articles with log using similarities between strings in log.path and articles.slug columns.

	Counted total number of articles, ordered them by the count column in descending order, and returned only the top 3.

Question 2 Solution:

	Extrapolated on the first question's query by joining the authors table to the author and log which were joined using the LIKE operator.

	Replaced articles.title with authors.name.

Question 3 Solution:
	
	Created two Views with subqueries. First view created a table with the log table's time column (filtered by date to remove time) and the count of the log table's status column. The second query in the view consolodated the dates and number of total statuses.

	The second view generated a similar table except it only counted '404 NOT FOUND' statuses.

	The final query's subquery created a table with the date column and column with percentages of error status generated from the numbers created in the two View tables. The final query returned only the dates with errors greater than 1%.
_________________________________________________________________

Views:

CREATE VIEW access_sum AS
	SELECT access_t.time, count(access_t.access_total)
		as access_count
	FROM (SELECT log.time::date, count(log.status)
		as access_total
	FROM log
	GROUP BY log.time)
		as access_t
	GROUP BY access_t.time;

CREATE VIEW error_sum AS
	SELECT error_t.time, count(error_t.error_total)
		as error_count
	FROM (SELECT log.time::date, count(log.status)
		as error_total
	FROM log
	WHERE log.status = '404 NOT FOUND'
	GROUP BY log.time)
		as error_t
	GROUP By error_t.time;