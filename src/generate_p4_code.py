# generate_p4_code.py
import joblib


def tree_to_p4(model, features):
    rules = []

    def traverse(node, depth):
        indent = '    ' * depth
        if model.tree_.feature[node] != -2:  # 非叶节点
            feature = features[model.tree_.feature[node]]
            threshold = model.tree_.threshold[node]
            rules.append(f"{indent}if (hdr.{feature} <= {threshold}) {{")
            traverse(model.tree_.children_left[node], depth + 1)
            rules.append(f"{indent}}} else {{")
            traverse(model.tree_.children_right[node], depth + 1)
            rules.append(f"{indent}}}")
        else:  # 叶节点
            action = "forward()" if model.tree_.value[node].argmax() == 1 else "drop()"
            rules.append(f"{indent}{action};")

    traverse(0, 1)
    return "\n".join(rules)


def save_p4_code(rules, output_path):
    p4_code = f"""
// P4 program generated from decision tree model
header_type ethernet_t {{
    fields {{
        dstAddr : 48;
        srcAddr : 48;
        etherType : 16;
    }}
}}

header ethernet_t ethernet;

header_type ipv4_t {{
    fields {{
        version : 4;
        ihl : 4;
        diffserv : 8;
        totalLen : 16;
        identification : 16;
        flags : 3;
        fragOffset : 13;
        ttl : 8;
        protocol : 8;
        hdrChecksum : 16;
        srcAddr : 32;
        dstAddr : 32;
    }}
}}

header ipv4_t ipv4;

header_type tcp_t {{
    fields {{
        srcPort : 16;
        dstPort : 16;
        seqNo : 32;
        ackNo : 32;
        dataOffset : 4;
        res : 3;
        ecn : 3;
        ctrl : 6;
        window : 16;
        checksum : 16;
        urgentPtr : 16;
    }}
}}

header tcp_t tcp;

parser start {{
    extract(ethernet);
    return parse_ipv4;
}}

parser parse_ipv4 {{
    extract(ipv4);
    return parse_tcp;
}}

parser parse_tcp {{
    extract(tcp);
    return ingress;
}}

action drop() {{
    drop();
}}

action forward() {{
    standard_metadata.egress_spec = 1; // 假设输出端口为1
}}

control ingress {{
    apply {{
        {rules}
    }}
}}

control egress {{
    apply {{ }}
}}

control verifyChecksum {{
    apply {{ }}
}}

control computeChecksum {{
    apply {{ }}
}}

control deparser {{
    apply {{
        emit(ethernet);
        emit(ipv4);
        emit(tcp);
    }}
}}

V1Switch(
    parser = start,
    verifyChecksum = verifyChecksum,
    ingress = ingress,
    egress = egress,
    computeChecksum = computeChecksum,
    deparser = deparser
) main;
"""
    with open(output_path, 'w') as f:
        f.write(p4_code)


if __name__ == "__main__":
    features = ['ipv4.srcAddr', 'ipv4.dstAddr', 'tcp.srcPort', 'tcp.dstPort', 'ipv4.protocol', 'ipv4.totalLen']
    dt_model = joblib.load('../models/decision_tree_model.pkl')
    p4_rules = tree_to_p4(dt_model, features)
    save_p4_code(p4_rules, '../src/p4_program/decision_tree.p4')
