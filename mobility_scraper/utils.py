def write_df_to_csv_and_excel(df, paths):
    """Write Pandas Dataframe to CSV and Excel

    Args:
        df (DataFrame): dataframe which needs to be written
        paths (dict): dictionary where keys are extensions, values are paths
    """
    df.to_csv(paths[".csv"], index=False)
    df.to_excel(paths[".xlsx"], index=False, sheet_name="Data", engine="xlsxwriter")


def exception_handler(name):
    """Decorator for handling exceptions during data processing

    Args:
        name (str): name of data provider
    """

    def decorator(function):
        def wrapper(*args, **kwargs):
            try:
                result = function(*args, **kwargs)
                return result
            except Exception as e:
                print(name, ": Update failed.")
                print(e)

        return wrapper

    return decorator