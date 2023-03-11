import pandas as pd
import zipfile as zp


def write_df_to_csv_and_excel(df, paths):
    """Write Pandas Dataframe to CSV and Excel

    Args:
        df (DataFrame): dataframe which needs to be written
        paths (dict): dictionary where keys are extensions, values are paths
    """
    df.to_csv(paths[".csv"], index=False)
    if len(df) < 1048576:
        df.to_excel(paths[".xlsx"], index=False, sheet_name="Data", engine="xlsxwriter")
    else:
        # split data by years
        df.loc[:, "date"] = pd.to_datetime(df.loc[:, "date"])
        writer = pd.ExcelWriter(  # pylint: disable=abstract-class-instantiated
            paths[".xlsx"],
            engine="xlsxwriter",
            datetime_format="yyyy-mm-dd",
        )
        for year in pd.DatetimeIndex(  # pylint: disable=E1101
            df.loc[:, "date"]
        ).year.unique():
            df.loc[df.date.dt.year == year].to_excel(
                writer,
                index=False,
                sheet_name=str(year),
            )
        writer.save()


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