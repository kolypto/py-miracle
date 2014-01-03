import unittest
import miracle


class TestAclStructure(unittest.TestCase):
    def test_roles(self):
        """ add_role(), add_roles(), list_roles(), del_role() """
        acl = miracle.Acl()

        # Add roles
        acl.add_role('root')
        acl.add_role('superadmin')
        acl.add_role('superadmin') # does not replace or fail
        acl.add_role('user')
        acl.add_role('poweruser')
        acl.add_roles(['n00b', 'poweruser'])

        # Test roles
        self.assertSetEqual(acl.get_roles(), {'root','superadmin','user','poweruser','n00b'})

        # Del roles
        acl.del_role('poweruser')
        acl.del_role('poweruser') # does not fail
        acl.del_role('n00b')

        # Test roles
        self.assertSetEqual(acl.get_roles(), {'root','superadmin','user'})

    def test_resources(self):
        """ add_resource(), list_resource(), del_resource() """
        acl = miracle.Acl()

        # Add resources
        acl.add_resource('user')
        acl.add_resource('page')
        acl.add_resource('page') # does not replace or fail
        acl.add_resource('news')
        acl.add_resource('blog')

        # Test resources
        self.assertSetEqual(acl.get_resources(), {'user', 'page', 'news', 'blog'})

        # Delete resources
        acl.del_resource('news')
        acl.del_resource('news') # does not fail
        acl.del_resource('blog')

        # Test resources
        self.assertSetEqual(acl.get_resources(), {'user', 'page'})

    def test_permissions(self):
        """ add_permission(), list_permissions(), del_permission() """
        acl = miracle.Acl()

        # Add permissions
        acl.add_permission('user', 'create') # silently creates a resource
        acl.add_permission('user', 'create') # does not replace or fail
        acl.add_permission('user', 'read')
        acl.add_permission('user', 'write')
        acl.add_permission('post', 'read')
        acl.add_permission('post', 'create')
        acl.add_permission('log', 'delete')

        # Test resources
        self.assertSetEqual(acl.get_resources(), {'user', 'post', 'log'})

        # Test permissions on resources
        self.assertSetEqual(acl.get_permissions('404'), set()) # empty ok
        self.assertSetEqual(acl.get_permissions('user'), {'create','read','write'})
        self.assertSetEqual(acl.get_permissions('post'), {'read', 'create'})
        self.assertSetEqual(acl.get_permissions('log'), {'delete'})

        # Del permissions
        acl.del_permission('user', 'write')
        acl.del_permission('post', 'create')
        acl.del_permission('post', 'create') # does not fail

        # Test resources
        self.assertSetEqual(acl.get_resources(), {'user', 'post', 'log'})

        # Test permissions on resources
        self.assertSetEqual(acl.get_permissions('404'), set())
        self.assertSetEqual(acl.get_permissions('user'), {'create', 'read'})
        self.assertSetEqual(acl.get_permissions('post'), {'read'})
        self.assertSetEqual(acl.get_permissions('log'), {'delete'})

    def test_structure(self):
        """ add(), list() """
        acl = miracle.Acl()

        # Add
        acl.add({
            '/article': {'create','edit'},
            '/profile': ['edit'],
        })
        acl.add({
            '/article': ['vote'],
        })

        # list()
        self.assertDictEqual(
            acl.get(),
            {
                '/article': {'create','edit','vote'},
                '/profile': {'edit'}
            }
        )

        # lit() must produce a copy
        l = acl.get()
        l['/lol'] = 'a'
        l['/article'].add('lol')

        # Test: should not be modified
        self.assertDictEqual(
            acl.get(),
            {
                '/article': {'create', 'edit', 'vote'},
                '/profile': {'edit'}
            }
        )

        # Test resources
        self.assertSetEqual(acl.get_resources(), {'/article', '/profile'})

        # Test permissions on resources
        self.assertSetEqual(acl.get_permissions('/article'), {'create', 'edit', 'vote'}) # empty ok
        self.assertSetEqual(acl.get_permissions('/profile'), {'edit'}) # empty ok

    def test_grant(self):
        """ grant(), grants(), revoke(), show() """
        acl = miracle.Acl()
        acl.grant('root', '/admin', 'enter')
        acl.grant('root', '/admin', 'enter') # dupe
        acl.grant('root', '/article', 'edit')
        acl.grants({
            'user': {
                '/article': ['view'],
                '/admin': ['kill']
            }
        })
        acl.revoke('user', '/admin', 'kill')
        acl.revoke('user', '/admin', 'kill') # dupe

        # Structure
        self.assertSetEqual(acl.get_roles(), {'root', 'user'})
        self.assertDictEqual( acl.get(), {
            '/admin': {'enter','kill'}, # 'kill' remains, though revoked
            '/article': {'view','edit'}
        })

        # Grants
        self.assertDictEqual(acl.show(), {
            'root': {
                '/admin': {'enter'},
                '/article': {'edit'}
            },
            'user': {
                '/article':{'view'}
            }
        })

    def test_check(self):
        """ check(), check_any(), check_all() ; which(), which_any(), which_all() """
        acl = miracle.Acl()
        acl.grant('root',   '/admin',   'enter')
        acl.grant('admin',  '/admin',   'enter')
        acl.grant('root',   '/user',    'edit')
        acl.grant('root',   '/user',    'delete')
        acl.grant('root',   '/user',    'show')
        acl.grant('admin',  '/user',    'show')
        acl.grant('admin',  '/user',    'edit')
        acl.grant('user',   '/user',    'show')
        acl.add_role('nobody')

        # which()
        self.assertDictEqual(acl.which('root'), {
            '/admin': {'enter'},
            '/user': {'show','edit','delete'}
        })
        self.assertDictEqual(acl.which('admin'), {
            '/admin': {'enter'},
            '/user': {'show','edit'}
        })
        self.assertDictEqual(acl.which('user'), {
            '/user': {'show'}
        })
        self.assertDictEqual(acl.which('nobody'), {
        })

        # which_any()
        self.assertDictEqual(acl.which_any(True), {})
        self.assertDictEqual(acl.which_any([]), {})
        self.assertDictEqual(acl.which_any(['root', 'user']), acl.which('root'))
        self.assertDictEqual(acl.which_any(['admin', 'user']), acl.which('admin'))
        self.assertDictEqual(acl.which_any(['user']), acl.which('user'))
        self.assertDictEqual(acl.which_any(['user', 'nobody']), acl.which('user'))

        # which_all()
        self.assertDictEqual(acl.which_all(True), {})
        self.assertDictEqual(acl.which_all([]), {})
        self.assertDictEqual(acl.which_all(['root', 'admin']), acl.which('admin'))
        self.assertDictEqual(acl.which_all(['admin', 'user']), acl.which('user'))
        self.assertDictEqual(acl.which_all(['root', 'nobody']), acl.which('nobody'))
        self.assertDictEqual(acl.which_all(['user', 'root', 'nobody']), acl.which('nobody'))

        # check()
        self.assertTrue(acl.check('root', '/admin', 'enter'))
        self.assertFalse(acl.check('???', '/admin', 'enter')) # unknown role
        self.assertFalse(acl.check('root', '/???', 'enter')) # unknown resource
        self.assertFalse(acl.check('root', '/admin', '???')) # unknown permission
        self.assertTrue(acl.check('user', '/user', 'show'))

        # check_any()
        self.assertFalse(acl.check_any(True, '/user', 'show'))
        self.assertFalse(acl.check_any([], '/user', 'show'))
        self.assertTrue(acl.check_any(['root'], '/user', 'show'))
        self.assertTrue(acl.check_any(['root','user'], '/user', 'show'))
        self.assertTrue(acl.check_any(['root','user'], '/admin', 'enter'))
        self.assertTrue(acl.check_any(['root','user'], '/user', 'delete'))
        self.assertFalse(acl.check_any(['admin','user'], '/user', 'delete'))

        # check_all()
        self.assertFalse(acl.check_all(True, '/user', 'show'))
        self.assertFalse(acl.check_all([], '/user', 'show'))
        self.assertTrue(acl.check_all(['root','user'], '/user', 'show'))
        self.assertFalse(acl.check_all(['root','user'], '/admin', 'enter'))
        self.assertFalse(acl.check_all(['root','user'], '/user', 'delete'))
        self.assertFalse(acl.check_all(['root','user'], '/user', 'delete'))
        self.assertFalse(acl.check_all(['root','admin'], '/user', 'delete'))
        self.assertTrue(acl.check_all(['root','admin'], '/user', 'edit'))

    def test_pickle(self):
        """ __getstate__(), __setstate__() """
        acl = miracle.Acl()
        acl.grant('root',   '/admin',   'enter')
        acl.grant('user',   '/user',   'show')
        acl.grant('author',   '/article',   'post')

        self.assertDictEqual(acl.__getstate__(), {
            'roles': {'root','user','author'},
            'struct': {
                '/admin': {'enter'},
                '/user': {'show'},
                '/article': {'post'}
            },
            'grants': {
                'root': { '/admin': {'enter'} },
                'user': { '/user': {'show'} },
                'author': { '/article': {'post'} }
            }
        })

        acl2 = miracle.Acl()
        acl2.__setstate__(acl.__getstate__())

        self.assertDictEqual(
            acl .__getstate__(),
            acl2.__getstate__(),
        )

    def test_del(self):
        """ del_*() does not remove grants """
        acl = miracle.Acl()
        acl.grant('root', 'a', 'anything')
        acl.grant('root', 'b', 'everything')
        acl.grant('admin', 'b', 'something')
        acl.grant('nobody', 'a', 'nothing')
        acl.grant('nobody', 'c', 'nothing')

        acl.del_permission('a', 'anything')
        acl.del_role('root')
        acl.del_resource('c')

        self.assertDictEqual(acl.show(), {
            'root': {
                'a': {'anything'},
                'b': {'everything'},
            },
            'admin': {
                'b': {'something'},
            },
            'nobody': {
                'a': {'nothing'},
                'c': {'nothing'}
            }
        })
