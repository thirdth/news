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


"""Views"""


def createViewCleanLog():
    """creates a view that makes the path column of the log table more like the
    title column of the articles table so they can be compared."""
    conn = connect()
    c = conn.cursor()
    c.execute("CREATE or REPLACE VIEW cleanLog as\
                    select replace(replace(replace(\
                    path, '/article/', ''), '/', ''), '-', ' '), * from log;")
    conn.commit()
    conn.close()


def createViewPopularity():
    """creates a view that joins cleanLog and author so that cleanLog has a
    column that has the Author id in it and then groups the articles by the
    author, counting them and putting that count in descending order """
    conn = connect()
    c = conn.cursor()
    c.execute("CREATE or REPLACE VIEW popularity as\
                    SELECT articles.author, count(*) as num\
                        FROM articles, cleanLog\
                        where UPPER(articles.title) LIKE UPPER(CONCAT('%',\
                                    cleanLog.replace ,'%'))\
                        GROUP BY articles.author\
                        ORDER BY num DESC;")
    conn.commit()
    conn.close()


def createNumerator():
    """gets the number of failed requests on each given day """
    conn = connect()
    c = conn.cursor()
    c.execute("CREATE or REPLACE VIEW numerator as\
                    SELECT date(time) as numDate, count(*) as numNum\
                    FROM log\
                    WHERE status != '200 OK'\
                    GROUP BY Date(time)\
                    ORDER BY numDate;")
    conn.commit()
    conn.close()


def createDenominator():
    """gets the total number of requests for each given day """
    conn = connect()
    c = conn.cursor()
    c.execute("CREATE or REPLACE VIEW denominator as\
                    SELECT date(time) as denDate, count(*) as denNum\
                    FROM log\
                    GROUP BY Date(time)\
                    ORDER BY denDate;")
    conn.commit()
    conn.close()


def createTotal():
    """joins the numerator and denominator views so they can be compared"""
    conn = connect()
    c = conn.cursor()
    c.execute("CREATE or REPLACE VIEW total as\
                    SELECT * from numerator, denominator\
                    WHERE numDate = denDate\
                    ;")
    conn.commit()
    conn.close()


"""Methods"""


def topThree():
    """gets the top three most popular articles and displays them in descending
    order with the title and how many views they have had"""
    conn = connect()  # initiates a connection
    c = conn.cursor()  # creates a cursor on that connection

    """ query that counts how many views each article has had by joining articles
    with the cleanLog view created above, sorts in descending order and only
    returns the top three"""
    c.execute("SELECT articles.title, count(*) as num\
                    FROM articles, cleanLog\
                    where UPPER(articles.title) LIKE UPPER(CONCAT('%',\
                                cleanLog.replace ,'%'))\
                    GROUP BY articles.title\
                    ORDER BY num DESC LIMIT 3;")
    result = c.fetchall()  # puts the results into a variable
    conn.commit()  # commits all changes
    conn.close()  # close connection after we're done -we weren't born in barns
    data = "\r\nTop Three Articles:\r\n 1. " + result[0][0] + "\r\n Views: " +\
        str(result[0][1]) + "\r\n 2. " + result[1][0] + "\r\n Views: " +\
        str(result[1][1]) + "\r\n 3. " + result[2][0] + "\r\n Views: " +\
        str(result[2][1]) + "\r\n"
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
    result = c.fetchall()  # puts the results into a variable
    conn.commit()  # commits all changes
    conn.close()  # close connection after we're done -we weren't born in barns
    data = "Most Popular Authors:\r\n 1. " + result[0][0] + "\r\n Views: " +\
        str(result[0][1]) + "\r\n 2. " + result[1][0] + "\r\n Views: " +\
        str(result[1][1]) + "\r\n 3. " + result[2][0] + "\r\n Views: " +\
        str(result[2][1]) + "\r\n"
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
    errors is greater than or equal to 1% of the number of requests"""
    c.execute("SELECT numDate from total\
                    WHERE numNum >= .01*denNum\
                    ;")
    result = c.fetchall()
    conn.close()
    data = "Day(s) in which more than 1% of requests returned errors:\r\n " +\
        str(result[0][0])
    #  appends the resuls of this query to the results.txt file
    file = open('results.txt', 'a')
    file.write(data + '\r\n')
    file.close()
    # prints the output when the function is called
    print(data)


if __name__ == '__main__':
    createViewCleanLog()
    createViewPopularity()
    createNumerator()
    createDenominator()
    createTotal()
    topThree()
    popularWriters()
    errorPercent()
