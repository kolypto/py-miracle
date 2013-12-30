import unittest
import miracle

class TestAclStructure(unittest.TestCase):
    def test_roles(self):
        """ add_role(), list_roles(), del_role() """
        acl = miracle.Acl()

        acl.add_role('root')
        acl.add_role('superadmin')
        acl.add_role('superadmin', 'user', 'poweruser')
        acl.add_role('root', 'n00b')

        self.assertListEqual(
            sorted(acl.list_roles()),
            sorted(['root','superadmin','user','poweruser','n00b'])
        )

        acl.del_role('poweruser')
        acl.del_role('poweruser', 'n00b')

        self.assertListEqual(
            sorted(acl.list_roles()),
            sorted(['root','superadmin','user'])
        )

if __name__ == '__main__':
    unittest.main()
