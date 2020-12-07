import pandas as pd 

def wide_date_conv(df, repivot_col=None):


    # force column headers to datetime, all non-dates will be NaT
    numeric_col_df = df.copy()
    numeric_col_df.columns = pd.to_datetime(numeric_col_df.columns, errors = 'coerce')

    # idenify column header values to keep
    columns_to_keep = numeric_col_df.columns.dropna()

    # get index values for column headers that are numeric
    date_cols_idx = numeric_col_df.columns.get_indexer_for(columns_to_keep)

    # select only the columns that have date-like formats by found indexes
    date_cols = df.iloc[:,date_cols_idx].columns

    # select non date columns
    non_date_cols = df.columns[~df.columns.isin(date_cols)]

    # unpivot dates / periods
    long_df = pd.melt(df, id_vars=non_date_cols, var_name="period", value_name="value")

    if repivot_col != None:

        # get the index cols for pivot
        index_cols = long_df.columns.to_list()

        # remove the repivot_col and the value column
        index_cols.remove(repivot_col)
        index_cols.remove("value")

        # repivot to the provided repivot col
        long_df = long_df.pivot_table(index=index_cols, columns='Description', values='value', aggfunc='mean').reset_index()
        
        # get rid of the column name
        long_df.columns.name = None

    return long_df
