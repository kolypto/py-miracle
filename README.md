[![Build Status](https://travis-ci.org/kolypto/py-miracle.png?branch=master)](https://travis-ci.org/kolypto/py-miracle)

Miracle
=======

Miracle is an ACL for Python that was designed to be well-structuted,
simple yet exhaustive. It uses *permissions* defined on *resources*, and *roles* are granted with the access to them.

To be a universal tool, it does not include any special cases,
does not force you to persist and does not insist on any formats or conventions.

Maximum flexibility and total control. Enjoy! :)

Highlights:

* Inspired by [miracle](https://github.com/kolypto/nodejs-miracle/) for NodeJS ;
* Simple core
* No restrictions on authorization entities
* Unit-tested






Table of Contents
=================

* <a href="#define-the-structure">Define The Structure</a>
    * <a href="#acl">Acl</a>
    * <a href="#create">Create</a>
        * <a href="#add_rolerole">add_role(role)</a>
        * <a href="#add_rolesroles">add_roles(roles)</a>
        * <a href="#add_resourceresource">add_resource(resource)</a>
        * <a href="#add_permissionresource-permission">add_permission(resource, permission)</a>
        * <a href="#addstructure">add(structure)</a>
    * <a href="#remove">Remove</a>
        * <a href="#remove_rolerole">remove_role(role)</a>
        * <a href="#remove_resourceresource">remove_resource(resource)</a>
        * <a href="#remove_permissionresource-permission">remove_permission(resource, permission)</a>
    * <a href="#get">Get</a>
        * <a href="#get_roles">get_roles()</a>
        * <a href="#get_resources">get_resources()</a>
        * <a href="#get_permissionsresource">get_permissions(resource)</a>
        * <a href="#get-1">get()</a>
    * <a href="#export-and-import">Export and Import</a>
* <a href="#authorize">Authorize</a>
    * <a href="#grant-permissions">Grant Permissions</a>
        * <a href="#grantrole-resource-permission">grant(role, resource, permission)</a>
        * <a href="#revokerole-resource-permission">revoke(role, resource, permission)</a>
    * <a href="#check-permissions">Check Permissions</a>
        * <a href="#checkrole-resource-permission">check(role, resource, permission)</a>
        * <a href="#check_anyroles-resource-permission">check_any(roles, resource, permission)</a>
        * <a href="#check_allroles-resource-permission">check_all(roles, resource, permission)</a>
    * <a href="#show-grants">Show Grants</a>
        * <a href="#whichrole">which(role)</a>
        * <a href="#which_anyroles">which_any(roles)</a>
        * <a href="#which_allroles">which_all(roles)</a>
        * <a href="#show">show()</a> 






Define The Structure
====================

Acl
---
To start using miracle, instantiate the `Acl` object:

```python
from acl import Acl
acl = Acl()
```

The `Acl` object keeps track of your *resources* and *permissions* defined on them, handles *grants* over *roles* and
provides utilities to manage them. When configured, you can check the access against the defined state.

Create
------

Methods from this section allow you to build the *structure*: list of roles, resources and permissions.

It's not required that you have the structure defined before you start granting the access: the `grant()` method
implicitly creates all resources and permissions that were not previously defined.

Start with defining the *resources* and *permissions* on them, then you can grant a *role* with the access to some
permissions on a resource.

For roles, resources & permissions, any hashable objects will do.

### `add_role(role)`
Define a role.

* `role`: the role to define.

The role will have no permissions granted, but will appear in `get_roles()`.

```python
acl.add_role('admin')
acl.get_roles()  # -> {'admin'}
```

### `add_roles(roles)`
Define multiple roles

* `roles`: An iterable of roles

```python
acl.add_roles(['admin', 'root'])
acl.get_roles()  # -> {'admin', 'root'}
```

### `add_resource(resource)`
Define a resource.

* `resources`: the resource to define.

The resource will have no permissions defined but will appear in `get_resources()`.

```python
acl.add_resource('blog')
acl.get_resources()  # -> {'blog'}
```

### `add_permission(resource, permission)`
Define a permission on a resource.

* `resource`: the resource to define the permission on.
    Is created if was not previously defined.
* `permission`: the permission to define.

The defined permission is not granted to anyone, but will appear in `get_permissions(resource)`.

```python
acl.add_permission('blog', 'post')
acl.get_permissions('blog')  # -> {'post'}
```

### `add(structure)`
Define the whole resource/permission structure with a single dict.

* `structure`: a dict that maps resources to an iterable of permissions.

```python
acl.add({
    'blog': ['post'],
    'page': {'create', 'read', 'update', 'delete'},
})
```

Remove
------

### `remove_role(role)`
Remove the role and its grants.

* `role`: the role to remove.

```python
acl.remove_role('admin')
```

### `remove_resource(resource)`
Remove the resource along with its grants and permissions.

* `resource`: the resource to remove.

```python
acl.remove_resource('blog')
```

### `remove_permission(resource, permission)`
Remove the permission from a resource.

* `resource`: the resource to remove the permission from.
* `permission`: the permission to remove.

The resource is not implicitly removed: it remains with an empty set of permissions.

```python
acl.remove_permission('blog', 'post')
```

### `clear()`
Remove all roles, resources, permissions and grants.

Get
---

### `get_roles()`
Get the set of defined roles.

```python
acl.get_roles()  # -> {'admin', 'anonymous', 'registered'}
```

### `get_resources()`
Get the set of defined resources, including those with empty permissions set.

```python
acl.get_resources()  # -> {'blog', 'page', 'article'}
```

### `get_permissions(resource)`
Get the set of permissions for a resource.

* `resource`: the resource to get the permissions for.

```python
acl.get_permissions('page')  # -> {'create', 'read', 'update', 'delete'}
```

### `get()`
Get the *structure*: hash of all resources mapped to their permissions.

Returns a dict: `{ resource: set(permission,...), ... }`.

```python
acl.get()  # -> { blog: {'post'}, page: {'create', ...} }
```



Export and Import
-----------------
The `Acl` class is picklable:

```python
acl = miracle.Acl()
save = acl.__getstate__()

#...

acl = miracle.Acl()
acl.__setstate__(save)
```





Authorize
=========

Grant Permissions
-----------------

### `grant(role, resource, permission)`
Grant a permission over resource to the specified role.

* `role`: The role to grant the access to
* `resource`: The resource to grant the access over
* `permission`: The permission to grant with

Roles, resources and permissions are implicitly created if missing.

```python
acl.grant('admin', 'blog', 'delete')
acl.grant('anonymous', 'page', 'view')
```

### `grants(grants)`
Add a structure of grants to the Acl.

* `grants`: A hash in the following form: `{ role: { resource: set(permission) } }`.

```python
acl.grants({
    'admin': {
        'blog': ['post'],
    },
    'anonymous': {
        'page': ['view']
    }
})
```

### `revoke(role, resource, permission)`
Revoke a permission over a resource from the specified role.

```python
acl.revoke('anonymous', 'page', 'view')
acl.revoke('user', 'account', 'delete')
```



Check Permissions
-----------------

### `check(role, resource, permission)`
Test whether the given role has access to the resource with the specified permission.

* `role`: The role to check
* `resource`: The protected resource
* `permission`: The required permission

Returns a boolean.

```python
acl.check('admin', 'blog') # True
acl.check('anonymous', 'page', 'delete') # -> False
```

### `check_any(roles, resource, permission)`
Test whether *any* of the given roles have access to the resource with the specified permission.

* `roles`: An iterable of roles.

When no roles are provided, returns False.

### `check_all(roles, resource, permission)`
Test whether *all* of the given roles have access to the resource with the specified permission.

* `roles`: An iterable of roles.

When no roles are provided, returns False.



Show Grants
-----------

### `which(role)`
Collect grants that the provided role has:

```python
acl.which('admin')  # -> { blog: {'post'} }
```

### `which_any(roles)`
Collect grants that any of the provided roles have (union).

```python
acl.which(['anonymous', 'registered'])  # -> { page: ['view'] }
```

### `which_all(roles)`
Collect grants that all of the provided roles have (intersection):

```python
acl.which(['anonymous', 'registered'])  # -> { page: ['view'] }
```

### `show()`
Get all current grants.

Returns a dict  `{ role: { resource: set(permission) } }`.

```python
acl.show()  # -> { admin: { blog: ['post'] } }
```
