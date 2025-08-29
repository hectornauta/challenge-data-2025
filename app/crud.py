from app.db import get_connection
import pandas as pd


def add_jobs(list_jobs: list):
    """"
    Añade una lista de Jobs
    """
    conn = get_connection()
    collection_jobs = [{'id': x.id, 'name': x.name} for x in list_jobs]
    dataframe = pd.DataFrame(collection_jobs)
    dataframe.to_sql(
        'jobs',
        conn,
        if_exists='append',
        index=False
    )
    conn.close()


def add_hired_employees(list_hired_employees: list):
    """"
    Añade una lista de Hired Employees
    """
    conn = get_connection()
    collection_hired_employees = [
        {
            'id': x.id,
            'name': x.name,
            'datetime': x.datetime,
            'department_id': x.department_id,
            'job_id': x.job_id
        } for x in list_hired_employees
    ]
    dataframe = pd.DataFrame(collection_hired_employees)
    dataframe.to_sql(
        'hired_employees',
        conn,
        if_exists='append',
        index=False
    )
    conn.close()


def add_departments(list_departments: list):
    """"
    Añade una lista de Departments
    """
    conn = get_connection()
    collection_departments = [{'id': x.id, 'name': x.name} for x in list_departments]
    dataframe = pd.DataFrame(collection_departments)
    dataframe.to_sql(
        'departments',
        conn,
        if_exists='append',
        index=False
    )
    conn.close()


def list_employees_by_quarter():
    """"
    Obtiene una tabla de cantidad de hired employees por trimestre
    """
    conn = get_connection()
    dataframe = pd.read_sql(
        sql="""
            SELECT
                d.name,
                j.name,
                SUM(CASE WHEN strftime('%m', he.datetime) IN ('01', '02', '03') THEN 1 ELSE 0 END) AS Q1,
                SUM(CASE WHEN strftime('%m', he.datetime) IN ('04', '05', '06') THEN 1 ELSE 0 END) AS Q2,
                SUM(CASE WHEN strftime('%m', he.datetime) IN ('07', '08', '09') THEN 1 ELSE 0 END) AS Q3,
                SUM(CASE WHEN strftime('%m', he.datetime) IN ('10', '11', '12') THEN 1 ELSE 0 END) AS Q4
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
    return dataframe.to_dict('records')



def list_mean_hired_employees():
    """"
    Obtiene una tabla de cantidad de hired employees por Departments, siempre y cuando esa cantidad sea mayor a la media por Departments
    """
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
        ORDER BY mean_he DESC
        """,
        con=conn
    )
    print(dataframe)
    return dataframe.to_dict('records')
