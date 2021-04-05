import zipfile as zp


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


def convert_file_to_zip(zip_path, file_path, file_name):
    """Convert file to zip archive and delete it

    Args:
        zip_path: path to the resulting zip file
        file_path: path to the file
        file_name: filename (with extension)
    """
    with zp.ZipFile(zip_path, "w", zp.ZIP_DEFLATED) as zf:
        zf.write(file_path, file_name)