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
                ORDER BY num desc
                LIMIT 3;
            """
    cursor.execute(query)
    results = cursor.fetchall()
    return results
    db.close()


def errors():
    """Determines which days did more than 1% of requests lead to errors."""
    db, cursor = connect()
    query = """
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

                SELECT to_char(percent.time, 'FMMonth FMDD, YYYY'), percent.percentage
                    FROM (SELECT error_sum.time,
                        sum(error_sum.error_count::float/
                        access_sum.access_count::float)*100
                        as percentage
                        FROM error_sum, access_sum
                        WHERE error_sum.time = access_sum.time
                        GROUP BY error_sum.time)
                        as percent
                    WHERE percent.percentage > 1;
                """
    cursor.execute(query)
    results = cursor.fetchall()
    return results
    db.close()


top_3_articles = top_3_articles()
top_3_authors = top_3_authors()
errors = errors()

print('Most Popular Three Articles of All Time:\n')
for i in range(3):
    print("\""+str(top_3_articles[i][0])+"\" - "+str(top_3_articles[i][1])+" views")

print('\n\nMost Popular Three Authors of All Time:\n')
for j in range(3):
    print(str(top_3_authors[j][0])+" - "+str(top_3_authors[j][1])+" views")

print('\n\nDays where more than 1% of server requests led to errors:\n')
for k in range(len(errors)):
    print(str(errors[k][0])+" - "+str(round(errors[k][1], 2))+"%")

