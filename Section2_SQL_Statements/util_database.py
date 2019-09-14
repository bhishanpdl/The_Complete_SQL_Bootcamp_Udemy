import numpy as np
import pandas as pd
import os
import time
import psycopg2


def get_postgres_configs(dbname):
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
    
    return dbname, dbuser, dbpass, dbport


def get_conn(dbname=None, dbuser=None, dbpass=None):
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

def execute_query(sql_query=None, dbname='None'):
    
    # first get postgres configs
    dbname, dbuser, dbpass, dbport = get_postgres_configs(dbname)
    
    # connect to the database
    with get_conn(dbname,dbuser,dbpass) as conn:
        df = pd.read_sql(sql_query, conn)

    return df


def show_all_tables_in_database(dbname):
    """Show the name of all tables in given database.
    
    Example:
    ========
    from util_database import show_all_tables_in_database
    show_all_tables_in_database('dvdrental')
    
    """

    sql_query = r"""SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
AND TABLE_CATALOG='{}'
and TABLE_NAME  not like 'pg_%'
and TABLE_NAME  not like 'sql_%'""".format(dbname)
    #print(execute_query(sql_query, dbname))
    
    # first get postgres configs
    dbname, dbuser, dbpass, dbport = get_postgres_configs(dbname)
    
    # connect to the database
    with get_conn(dbname,dbuser,dbpass) as conn:
        df = pd.read_sql(sql_query, conn)

    print(df['table_name'].values.tolist())
    
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

def get_pandas_dataframe(dbname, tablename):
    # first get postgres configs
    dbname, dbuser, dbpass, dbport = get_postgres_configs(dbname)

    # connect to the database
    sql_query = "select * from {}".format(tablename)
    with get_conn(dbname,dbuser,dbpass) as conn:
        df = pd.read_sql(sql_query, conn)
        
    return df

def show_pandas_dataframes_list(tables_names):
    dataframes_lst = ["{0} = get_pandas_dataframe(dbname, '{0}')".format(i)
            for i in tables_names ]
    
    dataframes_str = '\n'.join(dataframes_lst)
    df_tables = 'df_tables = [' + ', '.join(tables_names) + ' ]'
    cmds = dataframes_str + '\n\n' + df_tables
    
    print(cmds)
    
def show_df_tables_first_value_and_dtype(df_tables, num=0,
                               tables_names=None,
                               style=True):
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