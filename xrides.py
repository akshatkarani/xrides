import psycopg2
import csv
from config import config
from datetime import datetime


def _get_datetime(val: (None, str)):
    """
    Takes input a string and converts it into a python datetime object.

    >>> get_datetime('1/14/2013 9:45')
    datetime(2013, 14, 1, 9, 45)
    """
    if val is None:
        return None
    val = val.split(' ')
    date = val[0].split('/')
    new_date = [int(date[2]), int(date[0]), int(date[1])]
    time = val[1].split(':')
    time = list(map(int, time))
    return datetime(*new_date, *time)


def _change_row(row: list):
    """
    Changes the NULL values to None and
    date time entries to datetime object.
    """
    for index, val in enumerate(row):
        if val == 'NULL':
            row[index] = None
    row[9] = _get_datetime(row[9])
    row[10] = _get_datetime(row[10])
    row[13] = _get_datetime(row[13])
    return row


def _insert_data(data: list):
    """
    :param data: List to tuples where each tuple is a row to be inserted.
    :return:     Return true if data was successfully inserted
                 into the database.
    """
    sql = """INSERT INTO xride_data
             VALUES(%s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s,
                    %s);"""
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.executemany(sql, data)
        conn.commit()
        cur.close()
        return True
    except (Exception, psycopg2.DatabaseError) as e:
        # Print the error so problem can be tracked
        print(e)
        return False
    finally:
        if conn is not None:
            conn.close()


def send_data(filename):
    """
    Main function of the API to insert the data into the database.

    :param filename: Name of the csv file
    :return:         Return true if data was succesfully inserted
                     into the database.
    """
    with open(filename, 'r') as csvfile:
        rows = []
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            rows.append(tuple(_change_row(row)))
        return _insert_data(rows)

# Usage
# status = send_data('path/to/data.csv')
