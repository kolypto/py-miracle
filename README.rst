|Build Status|

Miracle
=======

Miracle is an ACL for Python that was designed to be well-structuted,
simple yet exhaustive. It uses *permissions* defined on *resources*, and
*roles* are granted with the access to them.

To be a universal tool, it does not include any special cases, does not
force you to persist and does not insist on any formats or conventions.

Maximum flexibility and total control. Enjoy! :)

Highlights:

-  Inspired by `miracle <https://github.com/kolypto/nodejs-miracle/>`__
   for NodeJS ;
-  Simple core
-  No restrictions on authorization entities
-  Unit-tested

Table of Contents
=================

-  Define The Structure

   -  Acl
   -  Create

      -  add\_role(role)
      -  add\_roles(roles)
      -  add\_resource(resource)
      -  add\_permission(resource, permission)
      -  add(structure)

   -  Remove

      -  remove\_role(role)
      -  remove\_resource(resource)
      -  remove\_permission(resource, permission)
      -  clear()

   -  Get

      -  get\_roles()
      -  get\_resources()
      -  get\_permissions(resource)
      -  get()

   -  Export and Import

-  Authorize

   -  Grant Permissions

      -  grant(role, resource, permission)
      -  grants(grants)
      -  revoke(role, resource, permission)
      -  revoke\_all(role[, resource])

   -  Check Permissions

      -  check(role, resource, permission)
      -  check\_any(roles, resource, permission)
      -  check\_all(roles, resource, permission)

   -  Show Grants

      -  which(role)
      -  which\_any(roles)
      -  which\_all(roles)
      -  show()

Define The Structure
====================

Acl
---

To start using miracle, instantiate the ``Acl`` object:

.. code:: python

    from acl import Acl
    acl = Acl()

The ``Acl`` object keeps track of your *resources* and *permissions*
defined on them, handles *grants* over *roles* and provides utilities to
manage them. When configured, you can check the access against the
defined state.

Create
------

Methods from this section allow you to build the *structure*: list of
roles, resources and permissions.

It's not required that you have the structure defined before you start
granting the access: the ``grant()`` method implicitly creates all
resources and permissions that were not previously defined.

Start with defining the *resources* and *permissions* on them, then you
can grant a *role* with the access to some permissions on a resource.

For roles, resources & permissions, any hashable objects will do.

``add_role(role)``
~~~~~~~~~~~~~~~~~~

Define a role.

-  ``role``: the role to define.

The role will have no permissions granted, but will appear in
``get_roles()``.

.. code:: python

    acl.add_role('admin')
    acl.get_roles()  # -> {'admin'}

``add_roles(roles)``
~~~~~~~~~~~~~~~~~~~~

Define multiple roles

-  ``roles``: An iterable of roles

.. code:: python

    acl.add_roles(['admin', 'root'])
    acl.get_roles()  # -> {'admin', 'root'}

``add_resource(resource)``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Define a resource.

-  ``resources``: the resource to define.

The resource will have no permissions defined but will appear in
``get_resources()``.

.. code:: python

    acl.add_resource('blog')
    acl.get_resources()  # -> {'blog'}

``add_permission(resource, permission)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Define a permission on a resource.

-  ``resource``: the resource to define the permission on. Is created if
   was not previously defined.
-  ``permission``: the permission to define.

The defined permission is not granted to anyone, but will appear in
``get_permissions(resource)``.

.. code:: python

    acl.add_permission('blog', 'post')
    acl.get_permissions('blog')  # -> {'post'}

``add(structure)``
~~~~~~~~~~~~~~~~~~

Define the whole resource/permission structure with a single dict.

-  ``structure``: a dict that maps resources to an iterable of
   permissions.

.. code:: python

    acl.add({
        'blog': ['post'],
        'page': {'create', 'read', 'update', 'delete'},
    })

Remove
------

``remove_role(role)``
~~~~~~~~~~~~~~~~~~~~~

Remove the role and its grants.

-  ``role``: the role to remove.

.. code:: python

    acl.remove_role('admin')

``remove_resource(resource)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Remove the resource along with its grants and permissions.

-  ``resource``: the resource to remove.

.. code:: python

    acl.remove_resource('blog')

``remove_permission(resource, permission)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Remove the permission from a resource.

-  ``resource``: the resource to remove the permission from.
-  ``permission``: the permission to remove.

The resource is not implicitly removed: it remains with an empty set of
permissions.

.. code:: python

    acl.remove_permission('blog', 'post')

``clear()``
~~~~~~~~~~~

Remove all roles, resources, permissions and grants.

Get
---

``get_roles()``
~~~~~~~~~~~~~~~

Get the set of defined roles.

.. code:: python

    acl.get_roles()  # -> {'admin', 'anonymous', 'registered'}

``get_resources()``
~~~~~~~~~~~~~~~~~~~

Get the set of defined resources, including those with empty permissions
set.

.. code:: python

    acl.get_resources()  # -> {'blog', 'page', 'article'}

``get_permissions(resource)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get the set of permissions for a resource.

-  ``resource``: the resource to get the permissions for.

.. code:: python

    acl.get_permissions('page')  # -> {'create', 'read', 'update', 'delete'}

``get()``
~~~~~~~~~

Get the *structure*: hash of all resources mapped to their permissions.

Returns a dict: ``{ resource: set(permission,...), ... }``.

.. code:: python

    acl.get()  # -> { blog: {'post'}, page: {'create', ...} }

Export and Import
-----------------

The ``Acl`` class is picklable:

.. code:: python

    acl = miracle.Acl()
    save = acl.__getstate__()

    #...

    acl = miracle.Acl()
    acl.__setstate__(save)

Authorize
=========

Grant Permissions
-----------------

``grant(role, resource, permission)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Grant a permission over resource to the specified role.

-  ``role``: The role to grant the access to
-  ``resource``: The resource to grant the access over
-  ``permission``: The permission to grant with

Roles, resources and permissions are implicitly created if missing.

.. code:: python

    acl.grant('admin', 'blog', 'delete')
    acl.grant('anonymous', 'page', 'view')

``grants(grants)``
~~~~~~~~~~~~~~~~~~

Add a structure of grants to the Acl.

-  ``grants``: A hash in the following form:
   ``{ role: { resource: set(permission) } }``.

.. code:: python

    acl.grants({
        'admin': {
            'blog': ['post'],
        },
        'anonymous': {
            'page': ['view']
        }
    })

``revoke(role, resource, permission)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Revoke a permission over a resource from the specified role.

.. code:: python

    acl.revoke('anonymous', 'page', 'view')
    acl.revoke('user', 'account', 'delete')

``revoke_all(role[, resource])``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Revoke all permissions from the specified role for all resources. If the
optional ``resource`` argument is provided - removes all permissions
from the specified resource.

.. code:: python

    acl.revoke_all('anonymous', 'page')  # revoke all permissions from a single resource
    acl.revoke_all('anonymous')  # revoke permissions from all resources

Check Permissions
-----------------

``check(role, resource, permission)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test whether the given role has access to the resource with the
specified permission.

-  ``role``: The role to check
-  ``resource``: The protected resource
-  ``permission``: The required permission

Returns a boolean.

.. code:: python

    acl.check('admin', 'blog') # True
    acl.check('anonymous', 'page', 'delete') # -> False

``check_any(roles, resource, permission)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test whether *any* of the given roles have access to the resource with
the specified permission.

-  ``roles``: An iterable of roles.

When no roles are provided, returns False.

``check_all(roles, resource, permission)``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test whether *all* of the given roles have access to the resource with
the specified permission.

-  ``roles``: An iterable of roles.

When no roles are provided, returns False.

Show Grants
-----------

``which(role)``
~~~~~~~~~~~~~~~

Collect grants that the provided role has:

.. code:: python

    acl.which('admin')  # -> { blog: {'post'} }

``which_any(roles)``
~~~~~~~~~~~~~~~~~~~~

Collect grants that any of the provided roles have (union).

.. code:: python

    acl.which(['anonymous', 'registered'])  # -> { page: ['view'] }

``which_all(roles)``
~~~~~~~~~~~~~~~~~~~~

Collect grants that all of the provided roles have (intersection):

.. code:: python

    acl.which(['anonymous', 'registered'])  # -> { page: ['view'] }

``show()``
~~~~~~~~~~

Get all current grants.

Returns a dict ``{ role: { resource: set(permission) } }``.

.. code:: python

    acl.show()  # -> { admin: { blog: ['post'] } }

.. |Build Status| image:: https://travis-ci.org/kolypto/py-miracle.png?branch=master
   :target: https://travis-ci.org/kolypto/py-miracle
