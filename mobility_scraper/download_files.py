from pathlib import Path

import requests
import urllib.request


def download_files(directory, URLs, file_names):
    """Download files from URLs

    Args:
        directory (str): directory to which files will be downloaded. If directory doesn't exist, it will be created
        URLs (iterable or str): URLs of files
        file_names (iterable or str): file names of downloaded files

    Returns:
        new_files (bool): flag indicating whether or not new files have been downloaded
    """
    new_files = False

    # create directory if it doesn't exist
    directory_path = Path(directory)
    if directory != "":
        if not directory_path.is_dir():
            directory_path.mkdir()
    # if URLs and filenames have an str type, convert them to tuples
    if isinstance(URLs, str):
        URLs = (URLs,)
    if isinstance(file_names, str):
        file_names = (file_names,)
    # build a dictionary with matching file names and URLs
    file_links = dict(zip(file_names, URLs))
    # update all files
    for file_name in file_names:
        file_path = directory_path / file_name
        link = file_links[file_name]
        old_size = file_path.stat().st_size if file_path.is_file() else 0
        urllib.request.urlretrieve(link, file_path)
        new_size = file_path.stat().st_size
        # mark update by file size
        if old_size != new_size:
            new_files = True

    return new_files


def update_status_message(name, status):
    """Create an update status message

    Args:
        name (str): name of data provider
        status (bool): flag indicating whether or not new files have been downloaded

    Returns:
        str: update_status_message
    """
    if status:
        return name + ": Update available"
    else:
        return name + ": No updates"
