import unittest
import miracle

class TestAclStructure(unittest.TestCase):
    def test_roles(self):
        """ add_role(), list_roles(), del_role() """
        acl = miracle.Acl()

        acl.add_role('root')
        acl.add_role('superadmin')
        acl.add_role('superadmin') # does not replace or fail
        acl.add_role('user')
        acl.add_role('poweruser')
        acl.add_role('n00b')

        self.assertListEqual(
            sorted(acl.list_roles()),
            sorted(['root','superadmin','user','poweruser','n00b'])
        )

        acl.del_role('poweruser')
        acl.del_role('poweruser') # does not fail
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
        acl.add_resource('page') # does not replace or fail
        acl.add_resource('news')
        acl.add_resource('blog')

        self.assertListEqual(
            sorted(acl.list_resources()),
            sorted(['user', 'page', 'news', 'blog'])
        )

        acl.del_resource('news')
        acl.del_resource('news') # does not fail
        acl.del_resource('blog')

        self.assertListEqual(
            sorted(acl.list_resources()),
            sorted(['user', 'page'])
        )

    def test_permissions(self):
        """ add_permission(), list_permissions(), del_permission() """
        acl = miracle.Acl()

        acl.add_permission('user', 'create') # silently creates a resource
        acl.add_permission('user', 'create') # does not replace or fail
        acl.add_permission('user', 'read')
        acl.add_permission('user', 'write')
        acl.add_permission('post', 'read')
        acl.add_permission('post', 'create')
        acl.add_permission('log', 'delete')

        self.assertListEqual(
            sorted(acl.list_resources()),
            sorted(['user', 'post', 'log'])
        )

        self.assertListEqual(
            sorted(acl.list_permissions('404')), # empty ok
            sorted([])
        )

        self.assertEqual(
            sorted(acl.list_permissions('user')),
            sorted(['create','read','write'])
        )

        self.assertEqual(
            sorted(acl.list_permissions('post')),
            sorted(['read', 'create'])
        )

        self.assertEqual(
            sorted(acl.list_permissions('log')),
            sorted(['delete'])
        )

        acl.del_permission('user', 'write')
        acl.del_permission('post', 'create')
        acl.del_permission('post', 'create') # does not fail

        self.assertListEqual(
            sorted(acl.list_resources()),
            sorted(['user', 'post', 'log'])
        )

        self.assertListEqual(
            sorted(acl.list_permissions('404')), # empty ok
            sorted([])
        )

        self.assertEqual(
            sorted(acl.list_permissions('user')),
            sorted(['create', 'read'])
        )

        self.assertEqual(
            sorted(acl.list_permissions('post')),
            sorted(['read'])
        )

        self.assertEqual(
            sorted(acl.list_permissions('log')),
            sorted(['delete'])
        )
