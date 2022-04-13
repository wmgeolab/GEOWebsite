import os
from venv import create
import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import Error
import os


def transfer_data(file_to_transfer):
    table_name = file_to_transfer[0, len(file_to_transfer) - 4]
    df = pd.read_csv(file_to_transfer)

    col_names = list(df.columns)
    print(col_names)

    conn = mysql.connector.connect(
        user=str(os.getenv("DB_USER", "")).rstrip(), password=str(os.getenv("DB_PASSWORD", "")), host=str(os.getenv("DB_HOST", "")).rstrip(), database=str(os.getenv("DB_NAME", "")).rstrip())
    cursor = conn.cursor()
    # CREATING THE TABLE:
    cursor.execute("DROP TABLE IF EXISTS %s;", (table_name, ))
    # dataTypes = dict(df.dtypes)
    create_table_string = "CREATE TABLE {}(id INT NOT NULL AUTO_INCREMENT".format(
        table_name)
    for column in col_names:
        create_table_string += ', {} VARCHAR(2000)'.format(column)

    create_table_string += ", PRIMARY KEY (id)"
    create_table_string += ");"
    cursor.execute(create_table_string)

    # ENTERING DATA VALUES INTO DB:
    np_arr = df.to_numpy()

    for entry in range(len(df)):
        sql = "INSERT INTO {}(".format(table_name)
        for col in range(len(col_names)):
            if col == len(col_names) - 1:
                sql += col_names[col]
            else:
                sql += col_names[col] + ", "
        sql += ") VALUES ("
        args = []
        for col in range(len(col_names)):
            if col == len(col_names) - 1:
                sql += '%s'
            else:
                sql += '%s'
                sql += ", "
            args.append("'" + str(np_arr[entry][col]) + "'")
        sql += ");"
        print(sql)
        cursor.executemany(sql, (args, ))
        conn.commit()

    print(np_arr)
