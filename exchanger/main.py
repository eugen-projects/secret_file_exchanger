import argparse
import logging
import os

logging.basicConfig(format="%(asctime)-15s: %(name)s - %(message)s", level=logging.INFO)


class TerminateProgram(Exception):
    pass


class Session(object):
    pass


class DownloadSession(Session):
    pass


class UploadSession(Session):
    def __init__(self):
        self.logger = logging.getLogger("UPLOADER")

    def _get_file_sizes(self, filenames):
        try:
            result = {}
            for filename in filenames:
                with open(filename):
                    result[filename] = os.path.getsize(filename)
            self.logger.info("Files have following sizes: %s", result)
            return result
        except IOError as ioe:
            self.logger.error("%s: '%s'. Please check if file exists at that location.", ioe.strerror, os.path.abspath(ioe.filename))
            raise TerminateProgram()


def upload(files=[], remote_ip_address=None, remote_port=None, **unused):
    print files, remote_ip_address, remote_port


def download(local_directory=None, local_port=None, **unused):
    print local_directory, local_port


def power_of_two(arg):
    """
    >>> power_of_two(4)
    4
    >>> power_of_two(52)
    32
    >>> power_of_two(-1)
    Traceback (most recent call last):
      ?
    AssertionError: block size argument must be a positive integer
    """
    assert arg > 0, 'block size argument must be a positive integer'
    result = 1
    while result * 2 <= arg:
        result *= 2
    return result


def main():
    parser = argparse.ArgumentParser(prog="Secret File Exchange")
    parser.add_argument('--version', action='version', version='%(prog)s 0.0.1')
    parser.add_argument('--block-size', type=power_of_two, default=4096, help="block size to split files into")
    subparsers = parser.add_subparsers(title='Mode of Operation arguments')
    upload_parser = subparsers.add_parser('upload', help="Upload mode command")
    upload_parser.add_argument('-ip', '--remote-ip-address', type=str, required=True)
    upload_parser.add_argument('-port', '--remote-port', type=int, default=3065)
    upload_parser.set_defaults(func=upload)
    upload_parser.add_argument('-f', '--files', type=str, nargs='+', help='file(s) to upload')
    download_parser = subparsers.add_parser('download', help="Download mode parser")
    download_parser.add_argument('-port', '--local-port', type=int, default=3065, help='port to listen for incoming connections')
    download_parser.add_argument('-d', '--local-directory', type=str, default='.', help='folder where to store downloaded files')
    download_parser.set_defaults(func=download)
    args = parser.parse_args()
    try:
        args.func(**args.__dict__)
    except TerminateProgram:
        pass

if __name__ == "__main__":
    main()