from data import Account, Group, Manager


def setup_manager():
    mgr = Manager()
    g1 = Group('group1').add_account(Account('account1')).add_account(Account('account2'))
    g2 = Group('group2').add_account(Account('account3'))
    mgr.add_group(g1).add_group(g2)
    