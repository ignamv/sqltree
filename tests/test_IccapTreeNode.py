from . import *
import string

from sqltree.model import IccapTreeNode

def recursive_create(nlevels, nchildren, prefix='', add_to_session=None):
    ''' Return TreeNode with nlevels-1 generations under it

    Each child is named after its parent + an uppercase letter

    Example
    =======

    >>> root = recursive_create(3, 3, 'A'))
    '''
    children = []
    if nlevels > 1:
        for ii, letter in enumerate(string.ascii_uppercase[:nchildren]):
            name = prefix + letter
            children.append(recursive_create(nlevels - 1, nchildren, name))
    if add_to_session is not None:
        add_to_session.add_all(children)
    return IccapTreeNode(name=prefix, children=children)

def tree_count(levels, children):
    '''Number of nodes in a tree'''
    if children == 1:
        return levels
    else:
        return (children ** levels - 1) // (children - 1)

class TestIccapTreeNode(DatabaseTest):
    def node_count(self):
        return self.session.query(IccapTreeNode).count()

    def test_orphan(self):
        orphan = IccapTreeNode(type='MODEL', name='orphan')
        self.session.add(orphan)
        self.session.commit()
        self.assertEqual(self.node_count(), 1)

    def test_chain(self):
        '''Insert linear chain of nodes'''
        nodes = []
        for ii in range(100):
            nodes.append(IccapTreeNode(name='name{}'.format(ii), children=nodes[-1:]))
        self.session.add_all(nodes)
        self.session.commit()
        self.assertEqual(self.node_count(), len(nodes))

    def test_tree(self):
        '''Insert tree of nodes'''
        self.session.add(recursive_create(3, 3, 'name'))
        self.session.commit()
        self.assertEqual(self.node_count(), tree_count(3, 3))

    @unittest.skip('10 second test')
    def test_hugetree(self):
        '''Insert huge tree of nodes'''
        self.session.add(recursive_create(5, 10, 'name'), self.session)
        self.session.commit()
        self.assertEqual(self.node_count(), tree_count(5, 10))

    def test_child(self):
        parent = IccapTreeNode(name='parent')
        child = IccapTreeNode(name='child', parent=parent)
        self.session.add(parent)
        self.session.commit()
        self.assertIs(parent.child('child'), child)
