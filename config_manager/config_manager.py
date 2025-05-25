"""Small program to manage config files"""

import argparse
from urllib.parse import urljoin

import requests


def run(config_url: str):
    # metadata should be something like:
    # {'config_endpoint': '/program/path/goes/here.txt'}
    # putting one set of data in multiple locations is not supported for now
    metadata = requests.get(config_url, timeout=10).json()

    print("Got config metadata: {metadata}")

    for endpoint, filesystem_location in metadata.items():
        data_url = urljoin(config_url, endpoint)
        print(f"{data_url}: fetching data")
        data = requests.get(data_url, timeout=10)
        print(f"{data_url}: writing data to {filesystem_location}")
        with open(filesystem_location, "w", encoding="utf-8") as writefile:
            writefile.write(data.text)
        print(f"{data_url}: complete")


def parse_args():
    main_parser = argparse.ArgumentParser(description="config_manager")
    main_parser.add_argument("-V", "--version", action="version", version="0.0.0")
    main_parser.set_defaults(run=lambda: print("Use a subparser!"))
    modes = main_parser.add_subparsers(title="Mode", metavar="")

    run_parser = modes.add_parser("run", help="Run the config manager")
    run_parser.add_argument("--config-url", type=str, required=True)
    run_parser.set_defaults(run=run)

    return main_parser.parse_args()


def main():
    args = parse_args()
    args.run(**{key: value for key, value in vars(args).items() if key != "run"})


if __name__ == "__main__":
    main()
