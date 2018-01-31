import os
import time
import urllib.parse
import requests
from bs4 import BeautifulSoup
import argparse

base_url = ""
directory = ""
is_directory_specified = False


def crawl_all_files(url):
    global base_url
    global directory
    global is_directory_specified

    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        file = link.attrs.get('href')

        # If the file is a directory
        if file.endswith('/'):
            print("\"" + file + "\", directory")
            crawl_all_files(url + file)
        # Else, the file is not a directory
        else:
            print("\"" + file + "\", file")
            print(url + file)
            parse_result = urllib.parse.urlparse(url + file)
            # If the directory to store the files is specified
            if is_directory_specified:
                file_path = directory + \
                            urllib.parse.unquote(parse_result.path, encoding='UTF-8') \
                                .replace('/', os.sep)
            # Else, use the default directory
            else:
                file_path = parse_result.netloc.replace(':', '_') + \
                            urllib.parse.unquote(parse_result.path, encoding='UTF-8') \
                                .replace('/', os.sep)

            # Get the file in stream mode
            file_request = requests.get(url + file, stream=True)

            # Get the size of the file
            file_size = int(file_request.headers.get('Content-Length'))

            parent_directory_path = os.path.abspath(os.path.join(file_path, os.pardir))
            # If the parent directory does not exist
            if not os.path.exists(parent_directory_path):
                os.makedirs(parent_directory_path)

            # Download the file
            chunk_size = 128
            start = time.time()
            with open(file_path, 'wb') as fd:
                downloaded_size = 0
                for chunk in file_request.iter_content(chunk_size=chunk_size):
                    downloaded_size += chunk_size
                    print(str(downloaded_size) + " bytes, " +
                          str(downloaded_size * 100 / file_size) + "%")
                    fd.write(chunk)
            end = time.time()
            print(str(file_size) + " bytes downloaded in {interval}s."
                  .format(interval=str(end - start)))
            print("File path: " + file_path)

            file_request.close()

    r.close()

    return


def main():
    global base_url
    global directory
    global is_directory_specified

    # Parse the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="The full url of the server.")
    parser.add_argument("-d", "--directory", type=str, help="The target directory.")
    args = parser.parse_args()

    # For the positional argument "url"
    print("Starting crawling files from " + args.url + "...")
    base_url = args.url

    # For the optional argument "directory"
    if args.directory is not None:
        is_directory_specified = True
        print("directory = \"" + args.directory + "\"")
        directory = args.directory
    else:
        parse_result = urllib.parse.urlparse(base_url)
        directory = parse_result.netloc.replace(':', '_')
        print("Directory is not specified. The files will be stored into ")

    # Make the root directory
    os.makedirs(directory)

    crawl_all_files(base_url)

    return


if __name__ == "__main__":
    main()
