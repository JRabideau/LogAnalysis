#!/usr/bin/env python3
# Code for the log analysis project.
# It is meant to run from Git bash within the vagrant folder with
# the "news" database ready and virtual machine
# running.

import datetime
import psycopg2

db = psycopg2.connect("dbname=news")

query1 = """
select articles.title, count(*) as views
from articles,log
where concat('/article/', articles.slug) = log.path
group by articles.title order by views desc
limit 3;
"""
query2 = """
select authors.name, sum(views) as totalviews
from authors,
(
select articles.title, count(*) as views, authors.id as num
from articles,log,authors
where concat('/article/', articles.slug) =
log.path and authors.id= articles.author
group by articles.title,authors.id
order by views
) as original
where authors.id = original.num
group by authors.name
order by totalviews
desc;
"""

query3 = """
select top.date,
((cast(top.total as decimal(10)))/(cast(den.total as decimal(10))))*100
as "percent errors"
from top, den
where top.date = den.date
and
((cast(top.total as decimal(10)))/(cast(den.total as decimal(10))))*100 > 1;
"""


c = db.cursor()

c.execute(query1)

print("Here are the three most popular articles\n")

result = c.fetchall()
output = []

for row in result:
    output.append(list(map(str, list(row + ("Views",)))))
for x in output:
    print(
     str(x[0]).strip("[]")
     + ": " + str(x[1]).strip("[]") + " "
     + str(x[2]).strip("[]"))
print("\n")

print("Here are the most popular authors:\n")
c.execute(query2)
result = c.fetchall()
output = []

for row in result:
    output.append(list(map(str, list(row + ("Total Article Views",)))))
for x in output:
    print(str(x[0]).strip("[]")
          + ": " + str(x[1]).strip("[]") + " "
          + str(x[2]).strip("[]"))

print("Here are the dates that produced more that 1 percent errors:\n")
c.execute(query3)
result = c.fetchall()
output = []

for row in result:
    output.append(list(map(str, list(row + ("Percent Errors",)))))
for x in output:
    print(str(x[0]).strip("[]")
          + ": " + str(x[1]).strip("[]") + " "
          + str(x[2]).strip("[]"))
