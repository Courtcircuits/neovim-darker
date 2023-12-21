from fabric import Connection


def directory_exists(connection: Connection, path: str) -> bool:
    """
    Check if a directory exists on the remote server. Might throw an exception.
    """
    return connection.run(f"test -d {path}", warn=True).ok


def upload_file(connection: Connection, local_path: str, remote_path: str) -> None:
    """
    Send a file on a specific path in th/e remote server. Might throw an exception.
    """
    if not directory_exists(connection, remote_path):
        connection.run(f"mkdir -p {remote_path}")

    connection.put(local_path, remote=remote_path)


def download_file(connection: Connection, local_path: str, remote_path: str) -> None:
    """
    Receive a file on a specific path from the remote server. Might throw an exception.
    """
    # check if there is a file like remote_path.enc or remote_path.tar.gz
    files = connection.run(f"ls {remote_path}.*", warn=True).stdout.split("\n")
    if len(files) == 0:
        raise Exception(f"Error: no file found on {remote_path}")
    for file in files:
        file_name = file.split("/")[-1]
        if file_name.endswith(".enc"):
            connection.get(file, local=local_path)
            return
    connection.get(remote_path, local=local_path)

def main():
    with Connection("bbronsin@162.38.112.136") as c:
        upload_file(c, "/toto.txt", "/home/bbronsin/")
        download_file(c, "/home/baptiste/", "/home/bbronsin/toto1.txt")


if __name__ == '__main__':
    main()
