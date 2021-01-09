def write_df_to_csv_and_excel(df, paths):
    """Write Pandas Dataframe to CSV and Excel

    Args:
        df (DataFrame): dataframe which needs to be written
        paths (dict): dictionary where keys are extensions, values are paths
    """
    df.to_csv(paths[".csv"], index=False)
    df.to_excel(paths[".xlsx"], index=False, sheet_name="Data", engine="xlsxwriter")
