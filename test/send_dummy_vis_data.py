import time
import logging
import simplejson as json

import requests

logging.basicConfig(level=logging.INFO)


DUMMY_LINK_DATA = {
    "Stats": {
        "sent_bytes_second": "50000",
        "rem_addr": "10.24.95.100:53468"
    },
    "IceRole": "CONTROLLED",
    "Type": "DummyVal",
    "Status": "Writeable"
}

DUMMY_NODE_DATA = {
    "TapName": "ipop_tap0",
    "VIP4": "2.3.4.5",
    "IP4PrefixLen": 16,
    "MAC": "FF:FF:FF:FF:FF"
}

N1 = "N1"
N2 = "N2"
N3 = "N3"
N4 = "N4"

NODES = [N1, N2, N3, N4]

OVRL1 = "Ovrl1"


def get_link_data(node_id, peer_id):
    link_id = "{}{}{}".format("L", node_id, peer_id)
    link_data = {link_id: DUMMY_LINK_DATA}
    link_data[link_id]["PeerId"] = peer_id

    return link_data


def get_req_data_template(ovrl_id, node_id):
    req_data_template = {
        "Data": {
            ovrl_id: {
                "LinkManager": {
                }
            }
        },
        "NodeId": node_id
    }

    return req_data_template


def gen_node_req_data_with_neighbours(node_id, neighbours):
    node_req_data = get_req_data_template(OVRL1, node_id)
    node_req_data["Data"][OVRL1]["LinkManager"][node_id] = \
        dict(NodeData=DUMMY_NODE_DATA, Links=dict())

    link_data = node_req_data["Data"][OVRL1]["LinkManager"][node_id]["Links"]
    for n in neighbours:
        link_data.update(get_link_data(node_id, n))

    return node_req_data


"""
odd_tick_reqs = [
    {
        "Data": {
            "Ovrl1": {
                "LinkManager": {
                    "N1": {
                        "NodeData": {
                            "TapName": "ipop_tap0",
                            "VIP4": "2.3.4.5",
                            "IP4PrefixLen": 16,
                            "MAC":  "FF:FF:FF:FF:FF"
                        },
                        "Links": {
                            "LN1N2": {
                                "PeerId": "N2",
                                "Stats": {
                                    "sent_bytes_second": "50000",
                                    "rem_addr": "10.24.95.100:53468"
                                },
                                "IceRole": "CONTROLLED",
                                "Type": "DummyVal",
                                "Status": "Writeable"
                            },
                            "LN1N3": {
                                "PeerId": "N3",
                                "Stats": {
                                    "sent_bytes_second": "50000",
                                    "rem_addr": "10.24.95.100:53468"
                                },
                                "IceRole": "CONTROLLED",
                                "Type": "DummyVal",
                                "Status": "Writeable"
                            },
                            "LN1N4": {
                                "PeerId": "N4",
                                "Stats": {
                                    "sent_bytes_second": "50000",
                                    "rem_addr": "10.24.95.100:53468"
                                },
                                "IceRole": "CONTROLLED",
                                "Type": "DummyVal",
                                "Status": "Writeable"
                            }
                        }
                    }
                }
            }
        },
        "NodeName": "N1"
    },
]

even_tick_requs = [
{
    'Data': {
        'O1': {
            'LinkManager': {
                'LN1N2': {
                    'Stats': {
                        'sent_bytes_second': '50000',
                        'rem_addr': '10.24.95.100:53468'
                    },
                    'PeerId': 'N2'
                },
                #'LN1N3': {
                #    'Stats': {
                #        'sent_bytes_second': '50000',
                #        'rem_addr': '10.24.95.100:53468'
                #    },
                #    'PeerId': 'N3'
                #},
                'LN1N4': {
                    'Stats': {
                        'sent_bytes_second': '50000',
                        'rem_addr': '10.24.95.100:53468'
                    },
                    'PeerId': 'N4'
                },
            },
            'Topology': {
                'PrefixLen': 16,
                'GeoIP': '1.2.3.4',
                'MAC': 'FF:FF:FF:FF:FF',
                'VIP4': '2.3.4.5',
                'InterfaceName': 'ipop_tap0'
            }
        }
    },
    'NodeId': 'N1'
},
{
    'Data': {
        'O1': {
            'LinkManager': {
                'LN2N1': {
                    'Stats': {
                        'sent_bytes_second': '50000',
                        'rem_addr': '10.24.95.100:53468'
                    },
                    'PeerId': 'N1'
                },
                'LN2N3': {
                    'Stats': {
                        'sent_bytes_second': '50000',
                        'rem_addr': '10.24.95.100:53468'
                    },
                    'PeerId': 'N3'
                },
                #'LN2N4': {
                #    'Stats': {
                #        'sent_bytes_second': '50000',
                #        'rem_addr': '10.24.95.100:53468'
                #    },
                #    'PeerId': 'N4'
                #},
            },
            'Topology': {
                'PrefixLen': 16,
                'GeoIP': '1.2.3.4',
                'MAC': 'FF:FF:FF:FF:FF',
                'VIP4': '2.3.4.5',
                'InterfaceName': 'ipop_tap0'
            }
        }
    },
    'NodeId': 'N2'
},
{
    'Data': {
        'O1': {
            'LinkManager': {
                #'LN3N1': {
                #    'Stats': {
                #        'sent_bytes_second': '50000',
                #        'rem_addr': '10.24.95.100:53468'
                #    },
                #    'PeerId': 'N1'
                #},
                'LN3N2': {
                    'Stats': {
                        'sent_bytes_second': '50000',
                        'rem_addr': '10.24.95.100:53468'
                    },
                    'PeerId': 'N2'
                },
                #'LN3N4': {
                #    'Stats': {
                #        'sent_bytes_second': '50000',
                #        'rem_addr': '10.24.95.100:53468'
                #    },
                #    'PeerId': 'N4'
                #},
            },
            'Topology': {
                'PrefixLen': 16,
                'GeoIP': '1.2.3.4',
                'MAC': 'FF:FF:FF:FF:FF',
                'VIP4': '2.3.4.5',
                'InterfaceName': 'ipop_tap0'
            }
        }
    },
    'NodeId': 'N3'
},
{
    'Data': {
        'O1': {
            'LinkManager': {
                'LN4N1': {
                    'Stats': {
                        'sent_bytes_second': '50000',
                        'rem_addr': '10.24.95.100:53468'
                    },
                    'PeerId': 'N1'
                },
                #'LN4N2': {
                #    'Stats': {
                #        'sent_bytes_second': '50000',
                #        'rem_addr': '10.24.95.100:53468'
                #    },
                #    'PeerId': 'N2'
                #},
                #'LN4N3': {
                #    'Stats': {
                #        'sent_bytes_second': '50000',
                #        'rem_addr': '10.24.95.100:53468'
                #    },
                #    'PeerId': 'N3'
                #},
            },
            'Topology': {
                'PrefixLen': 16,
                'GeoIP': '1.2.3.4',
                'MAC': 'FF:FF:FF:FF:FF',
                'VIP4': '2.3.4.5',
                'InterfaceName': 'ipop_tap0'
            }
        }
    },
    'NodeId': 'N4'
}
]
"""

odd_tick_reqs = [
    gen_node_req_data_with_neighbours(N1, [N2, N3, N4]),
    gen_node_req_data_with_neighbours(N2, [N1, N3, N4]),
    gen_node_req_data_with_neighbours(N3, [N1, N2, N4]),
    gen_node_req_data_with_neighbours(N4, [N1, N2, N3]),
]

even_tick_reqs = [
    gen_node_req_data_with_neighbours(N1, [N2, N4]),
    gen_node_req_data_with_neighbours(N2, [N1, N3]),
    gen_node_req_data_with_neighbours(N3, [N2, N4]),
    gen_node_req_data_with_neighbours(N4, [N1, N3]),
]

if __name__ == '__main__':
    tick = 0
    while True:
        if tick % 2:
            reqs = odd_tick_reqs
            which = 'odd'
        else:
            reqs = even_tick_reqs
            which = 'even'

        for r in reqs:
            node_id = r['NodeId']
            logging.info('Making {} request for node_id {}'
                         .format(which, node_id))
            requests.put('http://localhost:5000/IPOP/nodes/' + node_id,
                         data=json.dumps(r), headers={'Content-Type':
                                                      'application/json'})

        tick += 1
        logging.info('Sleeping for 15...')
        time.sleep(15)
