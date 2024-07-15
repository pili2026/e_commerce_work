import argparse

from commerce_server import CommerceServer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="args to start up the Web Server.")
    parser.add_argument("--config_path", help="The config path of the Web Server", required=False)
    args = parser.parse_args()
    config_path = args.config_path if args.config_path else "/etc/app_config.yml"

    server = CommerceServer(config_path)
    server.start()
