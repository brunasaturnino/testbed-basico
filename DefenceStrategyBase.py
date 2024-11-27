import os
from datetime import datetime
import iptc
import json

class DefenceStrategyBase:
    def __init__(self, dir):
        base_path = os.path.join(dir, os.pardir, os.pardir)
        self.configuration = json.loads(open(os.path.join(base_path, 'configuration.json'), 'r').read())
        self.dir = dir

    def get_configuration(self):
        return self.configuration

    def get_firewall_state(self, srcip):
        state = {}
        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
        for rule in chain.rules:
            if srcip in rule.src:
                state["srcip"] = srcip
                state["target"] = rule.target.name
        return state

    def block_ip(self, ip):
        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
        rule = iptc.Rule()
        rule.src = ip
        rule.target = iptc.Target(rule, "DROP")
        chain.insert_rule(rule)
