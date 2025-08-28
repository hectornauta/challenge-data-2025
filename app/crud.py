from db import get_connection
import pandas as pd


def list_employees_by_quarter():
    conn = get_connection()
    dataframe = pd.read_sql(
        sql="""
            SELECT
                d.name,
                j.name,
                SUM(CASE WHEN strftime('%m', he.datetime) IN ('01','02', '03') THEN 1 ELSE 0 END) AS Q1,
                SUM(CASE WHEN strftime('%m', he.datetime) IN ('04','05', '06') THEN 1 ELSE 0 END) AS Q2,
                SUM(CASE WHEN strftime('%m', he.datetime) IN ('07','08', '09') THEN 1 ELSE 0 END) AS Q3,
                SUM(CASE WHEN strftime('%m', he.datetime) IN ('10', '11','12') THEN 1 ELSE 0 END) AS Q4
            FROM
                departments AS d
                INNER JOIN hired_employees as he ON he.department_id=d.id
                INNER JOIN jobs as j ON he.job_id=j.id
            WHERE
                strftime('%Y', he.datetime) = '2021'
            GROUP BY
                d.name,
                j.name
            ORDER BY
                d.name,
                j.name
        """,
        con=conn
    )
    print(dataframe)



def list_mean_hired_employees():
    conn = get_connection()
    dataframe = pd.read_sql(
        sql="""
            SELECT
                d.id,
                d.name,
                COUNT(he.id) AS mean_he
            FROM
                departments AS d
                INNER JOIN hired_employees as he ON he.department_id=d.id
                INNER JOIN jobs as j ON he.job_id=j.id
            GROUP BY
                d.id,
                d.name
            HAVING COUNT(he.id) >= (SELECT AVG(temp_table.he_number) FROM (
                SELECT
                    d.id,
                    d.name,
                    COUNT(he.id) AS he_number
                FROM
                    departments AS d
                    INNER JOIN hired_employees as he ON he.department_id=d.id
                    INNER JOIN jobs as j ON he.job_id=j.id
                GROUP BY
                    d.id,
                    d.name
            ) AS temp_table
        )
        """,
        con=conn
    )
    print(dataframe)

# list_employees_by_quarter()
list_mean_hired_employees()