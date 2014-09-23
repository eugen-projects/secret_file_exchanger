import argparse


def upload(files=[], remote_ip_address=None, remote_port=None, **unused):
    print files, remote_ip_address, remote_port


def download(local_directory=None, local_port=None, **unused):
    print local_directory, local_port


def main():
    parser = argparse.ArgumentParser(prog="Secret File Exchange")
    parser.add_argument('--version', action='version', version='%(prog)s 0.0.1')
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
    args.func(**args.__dict__)


if __name__ == "__main__":
    main()