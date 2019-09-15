import numpy as np
import pandas as pd
import os
import time
import psycopg2

"""
Author: Bhishan Poudel
Purpose: Postgresql database utility functions

Available functions:
1. get_postgres_configs(dbname)
dbname, dbuser, dbpass, dbport = get_postgres_configs('dvdrental')

2. get_conn(dbname=None, dbuser=None, dbpass=None)
dbname, dbuser, dbpass, dbport = get_postgres_configs(dbname)
with get_conn(dbname,dbuser,dbpass) as conn: df = pd.read_sql(query, conn)

3. execute_query(sql_query=None, dbname=None)
from util_database import execute_query
execute_query(query, dbname='dvdrental')

4. get_all_tables_names_in_database(dbname)
from util_database import get_all_tables_names_in_database
tables_names = get_all_tables_names_in_database('dvdrental')

5. show_given_tables_info(dbname, tablename)
from util_database import show_given_tables_info
show_given_tables_info(dbname, 'customer')

6. get_pandas_dataframe(dbname, tablename)
customer = get_pandas_dataframe(dbname, 'customer')

7. show_df_tables_first_value_and_dtype(df_tables, tables_names=None,
                              num=0, style=True)
tables_names = ['actor', 'store']
(actor, store) = [get_pandas_dataframe(dbname, i)
                                        for i in tables_names]
df_tables = [actor, store]
show_df_tables_first_value_and_dtype(df_tables, tables_names = tables_names, num=14)

8. get_dataframe_of_all_tables_and_all_columns(df_tables,
                                                tables_names,style=True)

tables_names = ['actor', 'store']
(actor, store) = [get_pandas_dataframe(dbname, i)
                                        for i in tables_names]
df_tables = [actor, store]
get_dataframe_of_all_tables_and_all_columns(df_tables, tables_names, style=True)
"""

def show_method_attributes(method):
    """Print a nice dataframe of all attributes of given method."""

    x = [i for i in dir(method) if i[0].islower()]
    x = [i for i in x if i not in 'np pd os sys time sns psycopg2'.split()]

    return pd.DataFrame(np.array_split(x,2)).T.fillna('')

def get_postgres_configs(dbname, print=False):
    """Get the configs for postgres database.

    Example:
    ========
    dbname, dbuser, dbpass, dbport = get_postgres_configs('dvdrental')
    %load_ext sql
    %sql postgres://postgres:$dbpass@localhost:$dbport/$dbname
    """
    import os
    import yaml

    with open( os.path.expanduser('~') + "/.postgres_conf.yml", 'r') as stream:
        try:
            postgres_configs = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    dbname = dbname
    dbuser = 'postgres'
    dbpass = postgres_configs['password']
    dbport = postgres_configs['port']

    out = """
%load_ext sql
%sql postgres://postgres:$dbpass@localhost:$dbport/$dbname"""
    if print: print(out.lstrip())

    return dbname, dbuser, dbpass, dbport


def get_conn(dbname=None, dbuser=None, dbpass=None):
    """Get connection to postgres database using psycopg2.

    Usage:
    dbname, dbuser, dbpass, dbport = get_postgres_configs(dbname)
    with get_conn(dbname,dbuser,dbpass) as conn: df = pd.read_sql(query, conn)

    """
    try:
        conn = psycopg2.connect(dbname=dbname,
                                user=dbuser,
                                password=dbpass)

    except psycopg2.Error as e:
        print(e.pgerror)

    except Exception as e:
        print(e)
        return None

    return conn

def execute_query(sql_query=None, dbname=None):
    """Execute the sql query using pd.read_sql()

    Usage:
    =======
    execute_query(query, dbname='dvdrental')
    """
    # first get postgres configs
    dbname, dbuser, dbpass, dbport = get_postgres_configs(dbname)

    # connect to the database
    with get_conn(dbname,dbuser,dbpass) as conn:
        df = pd.read_sql(sql_query, conn)

    return df


def get_all_tables_names_in_database(dbname):
    """Show the name of all tables in given database.

    Example:
    ========
    from util_database import get_all_tables_names_in_database
    tables_names = get_all_tables_names_in_database('dvdrental')

    """

    sql_query = r"""SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
AND TABLE_CATALOG='{}'
and TABLE_NAME  not like 'pg_%'
and TABLE_NAME  not like 'sql_%'""".format(dbname)

    # first get postgres configs
    dbname, dbuser, dbpass, dbport = get_postgres_configs(dbname)

    # connect to the database
    with get_conn(dbname,dbuser,dbpass) as conn:
        df = pd.read_sql(sql_query, conn)

    tables_names = df['table_name'].values.tolist()
    return tables_names

def show_given_tables_info(dbname, tablename):
    """Show the column names, data types and one example of
       all columns in table.

    Example:
    ========
    from util_database import show_given_tables_info
    show_given_tables_info(dbname, 'customer')

    """
    sql_query = r"""select column_name, data_type, character_maximum_length
    from INFORMATION_SCHEMA.COLUMNS
    where table_name = '{}';""".format(tablename)
    #print(execute_query(sql_query, dbname))

    # first get postgres configs
    dbname, dbuser, dbpass, dbport = get_postgres_configs(dbname)

    # connect to the database
    with get_conn(dbname,dbuser,dbpass) as conn:
        df = pd.read_sql(sql_query, conn)

    return df.fillna('')


def show_tables_primary_keys(dbname, table_name):
    """Show the primary keys of given table.

    Example:
    ========
    from util_database import show_tables_primary_keys
    show_tables_primary_keys(dbname, 'customer')

    """
    sql_query = """SELECT KU.table_name as TABLENAME,column_name as PRIMARYKEYCOLUMN
    FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS TC
    INNER JOIN
        INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KU
              ON TC.CONSTRAINT_TYPE = 'PRIMARY KEY' AND
                 TC.CONSTRAINT_NAME = KU.CONSTRAINT_NAME AND
                 KU.table_name='{}'
    ORDER BY KU.TABLE_NAME, KU.ORDINAL_POSITION;""".format(table_name)

    # first get postgres configs
    dbname, dbuser, dbpass, dbport = get_postgres_configs(dbname)

    # connect to the database
    with get_conn(dbname,dbuser,dbpass) as conn:
        df = pd.read_sql(sql_query, conn)

    return df

def show_all_tables_primary_keys(dbname):
    """Show the pandas dataframe of all tables and thier primary keys.

    Example:
    ========
    from util_database import show_all_tables_primary_keys
    show_all_tables_primary_keys(dbname)

    """
    table_names = get_all_tables_names_in_database(dbname)
    df_tables_primarykeys = [show_tables_primary_keys(dbname, table_name)
                        for table_name in table_names]

    df_out = pd.concat(df_tables_primarykeys, axis=0,ignore_index=True)

    return df_out

def get_pandas_dataframe(dbname, tablename):
    """Get pandas dataframe from sql query.

    Usage:
    ======
    customer = get_pandas_dataframe(dbname, 'customer')
    """
    # first get postgres configs
    dbname, dbuser, dbpass, dbport = get_postgres_configs(dbname)

    # connect to the database
    sql_query = "select * from {}".format(tablename)
    with get_conn(dbname,dbuser,dbpass) as conn:
        df = pd.read_sql(sql_query, conn)

    return df

def show_pandas_dataframes_list(tables_names):
    """Show list of pandas dataframes from given tables names.
    """
    dataframes_lst = ["{0} = get_pandas_dataframe(dbname, '{0}')".format(i)
            for i in tables_names ]

    dataframes_str = '\n'.join(dataframes_lst)
    df_tables = 'df_tables = [' + ', '.join(tables_names) + ' ]'
    cmds = dataframes_str + '\n\n' + df_tables

    print(cmds)

def show_df_tables_first_value_and_dtype(df_tables, tables_names=None,
                                        num=0, style=True):
    """Show pandas dataframe of all the table's first value and its dtype.

    Usage:
    =======
    tables_names = ['actor', 'store']
    (actor, store) = [get_pandas_dataframe(dbname, i)
                                           for i in tables_names]
    df_tables = [actor, store]
    show_df_tables_first_value_and_dtype(df_tables, tables_names = tables_names, num=14)
    """
    df_tables_dtypes = [df_tables[i].dtypes.to_frame()
                        for i in range(len(df_tables)) ]
    df_tables_first_value = [df_tables[i].head(1).T
                             for i in range(len(df_tables)) ]

    out = pd.concat([df_tables_first_value[num],
                     df_tables_dtypes[num]],
                      axis=1, sort=True,ignore_index=True).rename(
                      columns={0: 'value', 1: 'dtype'})

    if style:
        out = (pd.concat([df_tables_first_value[num],
                          df_tables_dtypes[num]],
                          axis=1, sort=True,ignore_index=True)
                 .rename(columns={0: 'value', 1: 'dtype'})
                 .style.apply(lambda x: ['background: lightblue'
                                 if x['dtype'] == 'object'
                                 else ''
                                 for _ in x],axis=1)
                .set_caption('Dataframe name: ' + tables_names[num])
               )

    return out

def get_dataframe_of_all_tables_and_all_columns(df_tables,
                                                tables_names,style=True):
    """Get dataframe of all tables and all columns and optionally style it.

    Usage:
    =======
    tables_names = ['actor', 'store']
    (actor, store) = [get_pandas_dataframe(dbname, i)
                                           for i in tables_names]
    df_tables = [actor, store]
    get_dataframe_of_all_tables_and_all_columns(df_tables, tables_names, style=True)
    """
    all_columns = [df.columns.tolist() for df in df_tables]
    df_tables_cols = pd.DataFrame(all_columns).T.fillna('')
    df_tables_cols.columns = tables_names

    # find repeated column names
    repeated_cols = (pd.Series([i for sub in all_columns for i in sub])
                     .value_counts()
                     .loc[lambda x: x>1]
                     .index.values.tolist()
                    )
    # create colors dict
    cells = repeated_cols
    colors = ['salmon', 'khaki','rosybrown','tomato','olive',
              'gray',  'mediumpurple','orchid',  'plum','lavender',
              'lightgreen','lightsteelblue', 'lightblue','skyblue','orange',
              'orangered']
    colors = colors * 100
    colors = colors[:len(cells)]
    cell_colors = dict(zip(cells,colors))

    # colored dataframe
    df_tables_cols_styled = df_tables_cols.style.apply(lambda x:
                                     ["background: %s" % cell_colors[v]
                              if  v in cell_colors.keys()
                              else "" for v in x], axis = 1)

    return df_tables_cols_styled if style else df_tables_cols
