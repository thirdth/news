#!/usr/bin/python3

import sys
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection, or
    it prints the relevant error message."""
    try:
        return psycopg2.connect("dbname=news")

    except:
        print('An error occured connecting to the database "news".')
        sys.exit()


"""Methods"""


def topThree():
    """gets the top three most popular articles and displays them in descending
    order with the title and how many views they have had"""
    conn = connect()  # initiates a connection
    c = conn.cursor()  # creates a cursor on that connection

    """ query that counts how many views each article has had by joining
    articles with the log on the log.path and articles.slug columns, it then
    sorts in descending order and only returns the top three"""
    c.execute("SELECT articles.title, count(*) as num, articles.slug\
                    FROM articles, log\
                    where log.path = CONCAT('/article/',\
                                articles.slug)\
                    GROUP BY articles.title, articles.slug\
                    ORDER BY num DESC LIMIT 3;")
    results = c.fetchall()  # puts the results into a variable
    conn.close()  # close connection after we're done -we weren't born in barns
    data = "\r\nTop Three Articles:\r\n"
    i = 1
    #  iterates through results to append each result to the data variable
    for result in results:
        data += str(i) + ". Article: " + str(result[0]) + "\r\n Views: " +\
            str(result[1]) + "\r\n"
        i = i + 1
    #  opens a results.txt file and writes the results into it
    file = open('results.txt', 'w')
    file.write(data + '\r\n')
    file.close()
    # prints the output when the function is called
    print(data)


def popularWriters():
    """sorts all the writers by popularity and puts them in descending order.
    Popularity is based on views of all of their articles."""
    conn = connect()  # initiates a connection
    c = conn.cursor()  # creates a cursor on that connection

    """joins authors to the view popularity by their related columns, then gets
    the name of the author for each row in popularity and displays them in
    descending order"""
    c.execute("SELECT name, num from authors, popularity\
                where authors.id = popularity.author;\
                ")
    results = c.fetchall()  # puts the results into a variable
    conn.close()  # close connection after we're done -we weren't born in barns
    data = "Most Popular Writers:\r\n"
    i = 1
    #  iterates through results to append each result to the data variable
    for result in results:
        data += str(i) + ". Writer: " + result[0] + "\r\n Views: " +\
            str(result[1]) + "\r\n"
        i = i+1
    #  appends the resuls of this query to the results.txt file
    file = open('results.txt', 'a')
    file.write(data + '\r\n')
    file.close()
    #  prints the output when the function is called
    print(data)


def errorPercent():
    """tells us which day(s) had more than 1% of the requests lead to errors"""
    conn = connect()
    c = conn.cursor()
    """queries the view total and returns the Date in which the number of
    errors is greater than or equal to 1% of the number of requests, and the
    percentage."""
    c.execute("SELECT numDate, numNum, denNum from total\
                    WHERE numNum >= .01*denNum\
                    ;")
    results = c.fetchall()
    conn.close()
    i = 0
    data = "Day(s) in which more than 1% of requests returned errors:\r\n"
    for result in results:
        #  gets the percentage of errors and saves it in a string variable
        percent = str((round(float((result[1])/float(result[2])*100), 2)))
        #  appends the resuls of this query to the results.txt file
        data += str(result[0]) + " Percentage: " + percent + "%"
        i = i + 1
    file = open('results.txt', 'a')
    file.write(data + '\r\n')
    file.close()
    # prints the output when the function is called
    print(data)


if __name__ == '__main__':
    topThree()
    popularWriters()
    errorPercent()
