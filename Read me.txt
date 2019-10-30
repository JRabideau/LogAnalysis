### Project Name: News Website Logs Analysis Statistics ...
This project sets up a **PostgreSQL** database for a **news** website...
The provided Python script **<logananalysis.py>** uses the **psycopg2** library to query 
the database and produce a report that answers the following questions
#### Requirements
- Python
- PostgreSQL
- psycopg2 library
- The news database[Download from https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip]
- Virtual Box [https://www.virtualbox.org/wiki/Downloads]
- Vagrant [https://www.vagrantup.com/downloads.html]

The purpose of this project was to use SQL and python to answer three questions 
about a news website's database:

#1. What are the most popular three articles of all time?
#2. Who are the most popular article authors of all time?
#3. On which days did more than 1% of requests lead to errors?

For the first question's query, I used concat to make the slug and path values sync up.
I joined the articles and log tables and grouped by article name with a count 
aggregate to get total views for each article. I ordered by views with a limit 
of three to get the top three and added "desc" to get descending order. 

For the second question's query, I joined the authors table with a subquery that consisted 
of the first query with the authors table joined with the other two. 
In the parent query the total views for each author’s articles are added with 
a sum aggregate and grouped by author name.

For the third question's query I created two views, one counting the number of entries for each date, 
the other the number of errors for each date, using cast to extract just the date from the timestamp. 
The query joined them and calculated the percents using both views values and eliminating percents below 1%.

These are the views I made:

create view den as (select cast(time as varchar(10)) as date, count(status) as total 
from log group by date);


create view top as select cast(time as varchar(10)) as date, count(status) as total 
from log where status != '200 OK' group by date; 


The python script calls all three queries and formats the results in a readable format 
using a for loop and strip(). I looked up syntax of strip function on stack overflow.

The Python script was made with Python 3.7 on a Ubuntu virtual machine with Vagrant. Use Git Bash or other command-line interface
to go to the directory you want this in. Enter in "vagrant init" to create the enviroment. Enter "vagrant up" to get the 
enviroment running and then "vagrant ssh" to log in.

To run, place file in same directory as news database.
Enter the directory using the virtual machine and type "psql -d news -f <database file address>" to set up the database.
After it's initially set up, you may just enter "psql -d news" to enter the database. 
 Add the necessary views by entering the "create views" lines above. Then enter "python loganalysis.py" to run script.
