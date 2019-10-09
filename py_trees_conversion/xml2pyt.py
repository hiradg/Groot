import xml.etree.ElementTree as ET
import py_trees
import time

"""---------- INIT ----------"""
# Parse XML file
xml_tree = ET.parse('bt.xml')
xml_root = xml_tree.getroot()
# Set the root for bt 
bt_xml_root = xml_root[0][0]

def py_trees_node_conversion(bh_str):
    if bh_str == 'Sequence':
        return py_trees.composites.Sequence()
    elif bh_str == 'Fallback':
        return py_trees.composites.Selector()
    elif bh_str == 'Parallel':
        return py_trees.composites.Parallel()
    #elif bh_str == 'RetryUntilSuccesful':
        #return py_trees.decorators.FailureIsRunning()
    elif bh_str == 'AlwaysFailure':
        return py_trees.behaviours.Failure()
    elif bh_str == 'AlwaysSuccess':
        return py_trees.behaviours.Success()
    else:
        return py_trees.behaviours.Dummy()

def gen_pyt_bt(xml_bt_root_node):
    # Make an equivalent py_trees object
    pyt_current = py_trees_node_conversion(xml_bt_root_node.tag)
    # Check if the object is a leaf node
    if xml_bt_root_node.getchildren() == []:
        return pyt_current
    # Add the child nodes to the py_trees object
    for child in xml_bt_root_node:
        subtree = gen_pyt_bt(child)
        pyt_current.add_child(subtree)

    return pyt_current

"""---------- GENERATE BEHAVIOUR TREE ----------"""

# Convert py_trees BT from XML BT
root = gen_pyt_bt(bt_xml_root)

# Render bt in png, do and svg
py_trees.display.render_dot_tree(root)

behaviour_tree = py_trees.trees.BehaviourTree(root)
snapshot_visitor = py_trees.visitors.SnapshotVisitor()
behaviour_tree.visitors.append(snapshot_visitor)

"""---------- RUN BEHAVIOUR TREE ----------"""
for ii in range(3):
    print("******* %i ********" % ii)
    behaviour_tree.tick()
    unicode_tree = py_trees.display.unicode_tree(behaviour_tree.root,
                                             visited=snapshot_visitor.visited,
                                             previously_visited=snapshot_visitor.visited)
    print(unicode_tree)
    time.sleep(1)