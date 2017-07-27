# Logs Analysis Project
Source code for a program analysing a database to glean information about blog
articles, their authors and their readers for **Full Stack Web Developer
Nanodegree Program** from **Udacity**.

## Overview
This code queries a database consisting of three tables, Logs, Authors, and
Articles. It asks three questions of these databases:
1. What are the most popular three articles of all time? The Query should return
a sorted list with the most popular on top.
2. Who are the most popular authors of all time? The Query should return a
sorted list with the most popular on top.
3. On which days did more than 1% of the requests lead to error codes? The Query
should return a single date that meets that description.

Once the database is queried, the program outputs the answers to the console, and
writes the answers to these queries in the results.txt file that is included
with this repo. Should one wish to stop this, then delete the `file = open(
  'results.txt', 'w') file.write(data + '\r\n') file.close()` commands from each
  method.

### Tables
The tables consisted of information in the following format:
1. Logs -- PATH | IP | METHOD | STATUS | TIME | ID
2. Authors -- NAME | BIO | ID (fkey with articles.author)
3. Articles -- AUTHOR | TITLE | SLUG | LEAD | BODY | TIME | ID (fkey with authors.id)

The database is located in a file named newsdata.sql. None of the code is
intended to change the newsdata.sql database in any way other than creating
views when necessary.

### Views
Views that need to be created prior to running the code:

2. **popularity** - creates a view that joins log and author so that log
has a column that has the Author id. It then groups the articles by the
author, counting them and putting that count in descending order. The Code
follows:

  `CREATE or REPLACE VIEW popularity as SELECT articles.author, count(*) as num\
    FROM articles, log where UPPER(log.path) LIKE UPPER(CONCAT('/article/',\
    articles.slug)) GROUP BY articles.author ORDER BY num DESC;`

3. **numerator** - creates a view that consists of the number of failed
requests on each given day in order to be compared against the view denominator.
The Code follows:

  `CREATE or REPLACE VIEW numerator as SELECT date(time) as numDate, count(*) as
  numNum FROM log WHERE status != '200 OK' GROUP BY Date(time) ORDER BY
  numDate;")`

4. **denominator** - creates a view that consists of the total number of
requests for each given day in order to be compared against numerator. The
Code follows:

  `CREATE or REPLACE VIEW denominator as SELECT date(time) as denDate, count(*)
  as denNum FROM log GROUP BY Date(time) ORDER BY denDate;`

5. **total** - joins numerator and denominator in order to be able to make a
query that compares the two. The Code follows:

  `CREATE or REPLACE VIEW total as SELECT * from numerator, denominator WHERE
  numDate = denDate;`

## Set-up Instructions
1. This program is intended to be used from a command line environment utilizing
a virtual machine.
2. You will need to set-up a virtual machine like Virtual Box, and a way to connect
to that virtual machine, like with Vagrant. Instructions for set-up VirtualBox can be found [here](https://www.virtualbox.org/manual/https://www.vagrantup.com/intro/getting-started/ch01.html) While Instructions to download and set up Vagrant can be found [here](https://www.vagrantup.com/intro/getting-started/)
4. Prior to setting up Vagrant, download the files for the program onto your local machine.
5. Navigate to the folder containing these files and run `vagrant up` in order to
initialize your virtualMachine and connect to it through Vagrant. These files contain
a Vagrantfile that handles the set-up.
6. Once you have set-up Vagrant and Virtual Box you can utilize the database and
program through the command line in vagrant.
8. Navigate to the local folder that you set up Vagrant in, and run vagrant.ssh.
9. Navigate to your News folder in the virtual machine through the Vagrant directory.
11. Run the command `psql -d news -f newsdata.sql` in order to start the database environment. If you get
an error, or postgreql is not set up on your computer look [here](http://www.techrepublic.com/blog/diy-it-guy/diy-a-postgresql-database-server-setup-anyone-can-handle/) for Instructions
on how to download it and how to set-up a postgresql database.
13. Create all the views from above.
13. Exit the psql database by running the command `\q`
13. Once the news database is initialized and the views are created, you can
run your python file.

## Sample Use
This file is intended simply to return the answer to three separate questions.
In order to use it, simply navigate to the proper folder and run `python answers.py`.
It should make the appropriate views, and queries and will output the answers
in a readable way.
## Known Issues
There are no known issues at this time.
