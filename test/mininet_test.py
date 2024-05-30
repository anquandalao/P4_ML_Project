# mininet_test.py
import os


def deploy_p4_program():
    os.system(
        'p4c --target bmv2 --arch v1model ../src/p4_program/decision_tree.p4 -o ../src/p4_program/decision_tree.json')
    os.system('simple_switch --log-console ../src/p4_program/decision_tree.json &')


def test_mininet():
    os.system('sudo mn --topo single,3 --mac --switch ovsk --controller remote')
    os.system('h1 ping h2')
    os.system('h1 iperf -s &')
    os.system('h2 iperf -c h1')


if __name__ == "__main__":
    deploy_p4_program()
    test_mininet()
