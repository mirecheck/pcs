import shutil

from tornado.httpserver import HTTPServer
from tornado.netutil import bind_sockets, bind_unix_socket

from pcs.daemon import log
from pcs.daemon.ssl import PcsdSSL
from pcs.lib.auth.const import ADMIN_GROUP


class HttpsServerManageException(Exception):
    pass


class HttpsServerManage:
    """
    Instance of HttpsServerManage encapsulates the construction of an HTTPServer
    """

    # This object encapsulates creation and lifecycle of the HTTPServer,
    # including SSL certificate handling and socket management.

    def __init__(
        self,
        make_app,
        port,
        bind_addresses,
        ssl: PcsdSSL,
        unix_socket_path,
    ):
        self.__make_app = make_app
        self.__port = port
        self.__bind_addresses = bind_addresses
        self.__tcp_server = None
        self.__ssl = ssl
        self.__unix_socket_path = unix_socket_path
        self.__unix_socket_server = None
        self.__server_is_running = False

    @property
    def server_is_running(self):
        return self.__server_is_running

    def stop(self):
        self.__tcp_server.stop()
        self.__unix_socket_server.stop()
        self.__server_is_running = False

    def start(self):
        self.__ssl.guarantee_valid_certs()

        log.pcsd.info("Starting server...")

        app = self.__make_app()
        self.__tcp_server = HTTPServer(
            app,
            ssl_options=self.__ssl.create_context(),
        )
        self.__unix_socket_server = HTTPServer(app)

        # It is necessary to bind sockets for every new HTTPServer since
        # HTTPServer.stop calls sock.close() inside.
        sockets = []
        for address in self.__bind_addresses:
            log.pcsd.info(
                "Binding socket for address '%s' and port '%s'",
                address if address is not None else "*",
                self.__port,
            )
            sockets.extend(bind_sockets(self.__port, address))

        self.__tcp_server.add_sockets(sockets)
        self.__unix_socket_server.add_socket(
            bind_unix_socket(self.__unix_socket_path, mode=0o660)
        )
        shutil.chown(self.__unix_socket_path, 0, ADMIN_GROUP)

        log.pcsd.info("Server is listening")
        self.__server_is_running = True
        return self
