from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from pcs.cli.common.errors import CmdLineInputError
from pcs.cli.common.parse_args import group_by_keywords


DEFAULT_BOOTH_NAME = "booth"

def config_setup(lib, arg_list, modifiers):
    """
    create booth config
    """
    booth_configuration = group_by_keywords(
        arg_list,
        set(["sites", "arbitrators"]),
        keyword_repeat_allowed=False
    )
    lib.booth.config_setup(booth_configuration, modifiers["force"])

def config_show(lib, arg_list, modifiers):
    """
    print booth config
    """
    booth_configuration = lib.booth.config_show()
    authfile_lines = []
    if booth_configuration["authfile"]:
        authfile_lines.append(
            "authfile = {0}".format(booth_configuration["authfile"])
        )

    line_list = (
        ["site = {0}".format(site) for site in booth_configuration["sites"]]
        +
        [
            "arbitrator = {0}".format(arbitrator)
            for arbitrator in booth_configuration["arbitrators"]
        ]
        + authfile_lines +
        [
            'ticket = "{0}"'.format(ticket)
            for ticket in booth_configuration["tickets"]
        ]
    )
    for line in line_list:
        print(line)

def config_ticket_add(lib, arg_list, modifiers):
    """
    add ticket to current configuration
    """
    if len(arg_list) != 1:
        raise CmdLineInputError
    lib.booth.config_ticket_add(arg_list[0])

def config_ticket_remove(lib, arg_list, modifiers):
    """
    add ticket to current configuration
    """
    if len(arg_list) != 1:
        raise CmdLineInputError
    lib.booth.config_ticket_remove(arg_list[0])

def get_create_in_cluster(resource_create, resource_group):
    #TODO resource_create and resource_group is provisional hack until resources
    #are not moved to lib
    def create_in_cluster(lib, arg_list, modifiers):
        if len(arg_list) != 2 or arg_list[0] != "ip":
            raise CmdLineInputError()
        ip = arg_list[1]
        name = (
            modifiers["name"] if modifiers["name"]
            else DEFAULT_BOOTH_NAME
        )
        lib.booth.create_in_cluster(name, ip, resource_create, resource_group)
    return create_in_cluster

def get_remove_from_cluster(resource_remove):
    #TODO resource_remove is provisional hack until resources are not moved to
    #lib
    def remove_from_cluster(lib, arg_list, modifiers):
        if arg_list:
            raise CmdLineInputError()

        name = (
            modifiers["name"] if modifiers["name"]
            else DEFAULT_BOOTH_NAME
        )
        lib.booth.remove_from_cluster(name, resource_remove)

    return remove_from_cluster


def sync(lib, arg_list, modifiers):
    if arg_list:
        raise CmdLineInputError()
    lib.booth.config_sync(
        DEFAULT_BOOTH_NAME,
        skip_offline_nodes=modifiers["skip_offline_nodes"]
    )


def enable(lib, arg_list, modifiers):
    if arg_list:
        raise CmdLineInputError()
    lib.booth.enable(DEFAULT_BOOTH_NAME)


def disable(lib, arg_list, modifiers):
    if arg_list:
        raise CmdLineInputError()
    lib.booth.disable(DEFAULT_BOOTH_NAME)


def start(lib, arg_list, modifiers):
    if arg_list:
        raise CmdLineInputError()
    lib.booth.start(DEFAULT_BOOTH_NAME)


def stop(lib, arg_list, modifiers):
    if arg_list:
        raise CmdLineInputError()
    lib.booth.stop(DEFAULT_BOOTH_NAME)


def pull(lib, arg_list, modifiers):
    if len(arg_list) != 1:
        raise CmdLineInputError()
    lib.booth.pull(arg_list[0], DEFAULT_BOOTH_NAME)


def status(lib, arg_list, modifiers):
    if arg_list:
        raise CmdLineInputError()
    booth_status = lib.booth.status(DEFAULT_BOOTH_NAME)
    if booth_status.get("ticket"):
        print("TICKETS:")
        print(booth_status["ticket"])
    if booth_status.get("peers"):
        print("PEERS:")
        print(booth_status["peers"])
    if booth_status.get("status"):
        print("DAEMON STATUS:")
        print(booth_status["status"])
