from pcs import pcsd, usage
from pcs.cli.common.errors import raise_command_removed
from pcs.cli.common.routing import create_router

pcsd_cmd = create_router(
    {
        "help": lambda lib, argv, modifiers: print(usage.pcsd(argv)),
        "accept_token": pcsd.accept_token_cmd,
        "deauth": pcsd.pcsd_deauth,
        "certkey": lambda lib, argv, modifiers: raise_command_removed(
            pcs_version="1.0"
        ),
        "status": pcsd.pcsd_status_cmd,
        "sync-certificates": lambda lib, argv, modifiers: raise_command_removed(
            pcs_version="1.0"
        ),
    },
    ["pcsd"],
)
