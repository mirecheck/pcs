from unittest import TestCase


class CheckReachability(TestCase):
    """
    tested in:
        pcs_test.tier0.lib.command.status
    """


class GetOnlineTargets(TestCase):
    """
    tested in:
        pcs_test.tier0.lib.commands.sbd.test_enable_sbd
    """


class RemoveNodesFromCib(TestCase):
    """
    tested in:
        pcs_test.tier0.lib.commands.cluster.test_remove_nodes.{
            RemoveNodesFailureFromCib
            RemoveNodesSuccessMinimal
        }
    """
