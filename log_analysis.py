#! /usr/bin/env python3
import psycopg2

"""
Questions:
    1. What are the most popular three articles of all time?
    2. Who are the most popular article authors of all time?
    3. On which days did more than 1% of requests lead to errors?

"""


def connect(database_name="news"):
    """Connects to database"""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print ("<error message>")


def top_3_articles():
    """Determines the most popular three articles of all time."""
    db, cursor = connect()
    query = """
            SELECT articles.title, count(*) as num
                FROM log JOIN articles
                ON log.path = concat('/article/', articles.slug)
                GROUP BY articles.title
                ORDER BY num desc
                LIMIT 3;
            """
    cursor.execute(query)
    results = cursor.fetchall()
    return results
    db.close()


def top_3_authors():
    """Determines the most popular article authors of all time."""
    db, cursor = connect()
    query = """
            SELECT authors.name, count(*) as num
                FROM
                    authors
                JOIN
                    articles
                ON articles.author = authors.id
                JOIN
                    log
                ON log.path = concat('/article/', articles.slug)
                GROUP BY authors.name
                ORDER BY num desc;
            """
    cursor.execute(query)
    results = cursor.fetchall()
    return results
    db.close()


def errors():
    """Determines which days did more than 1% of requests lead to errors."""
    db, cursor = connect()
    query = """
                SELECT to_char(
                    percent.time, 'FMMonth FMDD, YYYY'),
                    round(percent.percentage, 2)
                    FROM (
                        SELECT error_sum.time,
                            (error_sum.error_total::decimal/
                            access_sum.access_total::decimal)*100
                            as percentage
                            FROM error_sum, access_sum
                            WHERE error_sum.time = access_sum.time)
                        as percent
                    WHERE percent.percentage > 1
                    ;
                """
    cursor.execute(query)
    results = cursor.fetchall()
    return results
    db.close()

if __name__ == "__main__":

    top_3_articles = top_3_articles()
    top_3_authors = top_3_authors()
    errors = errors()

    print('\nMost Popular Three Articles of All Time:\n')
    for articles, views in top_3_articles:
        print("\""+str(articles)+"\" - "+str(views)+" views")

    print('\n\nMost Popular Three Authors of All Time:\n')
    for authors, views in top_3_authors:
        print(str(authors)+" - "+str(views)+" views")

    print('\n\nDays where more than 1% of server requests led to errors:\n')
    for date, percent in errors:
        print(str(date)+" - "+str(percent)+"%")
    print('\n')
