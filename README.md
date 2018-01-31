# Crawl Everything: Crawl all the files from your server

## Why This Tiny Tool ?
  The other day I wanted to move a folder from my old Windows to my new
  Manjaro laptop. I compressed the folder along with all the files it contains
  into a `.zip` file. Then I moved the `.zip` file onto my Manjaro using
  a portable USB drive. I tried to extract the compressed `.zip` file
  but failed. For there exists non-ASCII characters, the extraction
  operation failed due to the encoding of file names containing
  non-ASCII characters. The extracted files with messy codes are really
  annoying.

  It's not convenient to use the USB drive either. Usually I prefer
  to use the `http server` utility provided by `Python` to transfer files
  between computers when they are connected to the same WiFi router.
  However, there are too many files for me to download manually. So I
  wrote this tiny Python script to crawl all the files from the
  `http server` and store them on the client computer, with the exactly
  the same folder structure.

  Of course, if you have a remote server, you can still use python to set up a 
  simple http server and use this tiny tool to **crawl all the files**.

## Getting Started

1. On the server computer
```bash
cd path_to_the_folder
python -m http.server 8000
```

2. On the client computer
  Assume that the IP address of the server computer is `192.168.0.106`.

```bash
python crawl_everything http://192.168.0.106:8000/
```

You can also specify the target directory
```bash
python crawl_everything http://192.168.0.106:8000/ -d folder_from_server
```

## Dependencies
- [Beautiful Soup 4](https://www.crummy.com/software/BeautifulSoup/)
- [Requests](https://github.com/requests/requests)


