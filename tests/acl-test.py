import unittest
import miracle

class TestAclStructure(unittest.TestCase):
    def test_roles(self):
        """ add_role(), list_roles(), del_role() """
        acl = miracle.Acl()

        acl.add_role('root')
        acl.add_role('superadmin')
        acl.add_role('superadmin')
        acl.add_role('user')
        acl.add_role('poweruser')
        acl.add_role('n00b')

        self.assertListEqual(
            sorted(acl.list_roles()),
            sorted(['root','superadmin','user','poweruser','n00b'])
        )

        acl.del_role('poweruser')
        acl.del_role('poweruser')
        acl.del_role('n00b')

        self.assertListEqual(
            sorted(acl.list_roles()),
            sorted(['root','superadmin','user'])
        )

    def test_resources(self):
        """ add_resource(), list_resource(), del_resource() """
        acl = miracle.Acl()

        acl.add_resource('user')
        acl.add_resource('page')
        acl.add_resource('page')
        acl.add_resource('news')
        acl.add_resource('blog')

        self.assertListEqual(
            sorted(acl.list_resources()),
            sorted(['user', 'page', 'news', 'blog'])
        )

        acl.del_resource('news')
        acl.del_resource('news')
        acl.del_resource('blog')

        self.assertListEqual(
            sorted(acl.list_resources()),
            sorted(['user', 'page'])
        )
