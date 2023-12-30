from orgparse import load, loads, node

def merge_org_files(file1_path, file2_path, output_path):
    # Load org files
    org1 = load(file1_path)
    org2 = load(file2_path)
    # Merge org nodes
    merged_root = merge_nodes(org1.children, org2.children)
    # Create a new org file with the merged content
    with open(output_path, 'w') as output_file:
        output_file.write(str(merged_root))

def merge_nodes(nodes1, nodes2):
    """
    Recursively merge two org nodes.
    """
    intersection_nodes = [node for node in nodes1 if node not in nodes2] + [node for node in nodes2 if node not in nodes1]
    merged_node = node.OrgNode(node.OrgEnv())

    print(node1.body)
    print(node2.body)
    # Merge body content
    # merged_node.body = node1.body + node2.body

    # Recursively merge child nodes
    for child1, child2 in zip(node1.children, node2.children):
        merged_child = merge_nodes(child1, child2)
        merged_node.append_child(merged_child)

    return merged_node

if __name__ == "__main__":
    file1_path = "/home/roland/first.org"
    file2_path = "/home/roland/second.org"
    output_path = "/home/roland/merged_file.org"

    merge_org_files(file1_path, file2_path, output_path)
