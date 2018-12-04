import subprocess
import logging
import signal


class Ganache:
    accounts = [
        "0x90f8bf6a479f320ead074411a4b0e7944ea8c9c1",
        "0xffcf8fdee72ac11b5c542428b35eef5769c409f0",
        "0x22d491bde2303f2f43325b2108d26f1eaba1e32b",
        "0xe11ba2b4d45eaed5996cd0823791e0c93114882d",
        "0xd03ea8624c8c5987235048901fb614fdca89b117",
        "0x95ced938f7991cd0dfcb48f0a06a40fa1af46ebc",
        "0x3e5e9111ae8eb78fe1cc3bb8915d5d461f3ef9a9",
        "0x28a8746e75304c0780e011bed21c72cd78cd535e",
        "0xaca94ef8bd5ffee41947b4585a84bda5a3d3da6e",
        "0x1df62f291b2e969fb0849d99d9ce41e2f137006e",
    ]

    private_keys = [
        "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d",
        "0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1",
        "0x6370fd033278c143179d81c5526140625662b8daa446c22ee2d73db3707e620c",
        "0x646f1ce2fdad0e6deeeb5c7e8e5543bdde65e86029e2fd9fc169899c440a7913",
        "0xadd53f9a7e588d003326d1cbf9e4a43c061aadd9bc938c843a79e7b4fd2ad743",
        "0x395df67f0c2d2d9fe1ad08d1bc8b6627011959b79c53d7dd6a3536a33ab8a4fd",
        "0xe485d098507f54e7733a205420dfddbe58db035fa577fc294ebd14db90767a52",
        "0xa453611d9419d0e56f499079478fd72c37b251a94bfde4d19872c44cf65386e3",
        "0x829e924fdf021ba3dbbc4225edfece9aca04b929d6e75613329ca6f1d31c0bb4",
        "0xb0057716d5917badaf911b193b12b910811c1497b5bada8d7711f758981c3773",
    ]

    def __init__(
        self,
        # Sandbox
        internal_host="localhost",
        internal_port=9545,
        deterministic=True,
        gas_price=1,
        # Blockchain to fork
        rpc=None,
        block_number=None,
        # Misc
        verbosity=logging.NOTSET,
    ):
        # Blockchain to fork
        self.rpc = rpc
        self.block_number = block_number

        # Where to start the sandbox
        self.internal_host = internal_host
        self.internal_port = internal_port
        self.internal_rpc = "http://{host}:{port}".format(
            host=self.internal_host, port=self.internal_port
        )

        # Gas price
        self.gas_price = gas_price

        # Account settings
        self.deterministic = deterministic

        # Verbosity
        self.verbosity = verbosity

        self.logger = logging.getLogger("Ganache")
        self.logger.setLevel(self.verbosity)

        # Building ganache-cli args
        self.logger.debug("Setting up ganache-cli args")
        args = ["ganache-cli"]

        # Host
        if self.internal_host is not None:
            args.extend(["-h", self.internal_host])

        # Port
        if self.internal_port is not None:
            args.extend(["-p", str(self.internal_port)])

        # Deterministic
        if self.deterministic:
            args.append("-d")

        # Gas price
        args.extend(["-g", str(self.gas_price)])

        # Fork blockchain
        if self.rpc is not None:
            if self.block_number is not None:
                args.extend(
                    [
                        "-f",
                        "{rpc}@{block_number}".format(
                            rpc=self.rpc, block_number=block_number
                        ),
                    ]
                )
            else:
                args.extend(["-f", "{rpc}".format(rpc=self.rpc)])

        self.logger.debug("Starting ganache with\n{}".format(" ".join(args)))
        self.process = subprocess.Popen(
            args, shell=False, universal_newlines=True, stdout=subprocess.PIPE
        )
        self.logger.debug(self.process.args)
        for l in self.process.stdout:
            self.logger.debug(l)
            # Wait for boot
            if "Listening on" in str(l):
                self.logger.debug(l)
                break

    def stop(self):
        self.process.send_signal(signal.SIGTERM)


class GanacheBaseException(Exception):
    pass


class ReceiverInvalidException(GanacheBaseException):
    pass
