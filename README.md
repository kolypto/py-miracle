[![Build Status](https://travis-ci.org/kolypto/py-miracle.png?branch=master)](https://travis-ci.org/kolypto/py-miracle)

Miracle
=======

Miracle is an ACL for Python that was designed to be well-structuted,
simple yet exhaustive. It uses *permissions* defined on *resources*, and *roles* are granted with the access to them.

To be a universal tool, it does not include any special cases,
does not force you to persist and does not insist on any formats or conventions.

Maximum flexibility and total control. Enjoy! :)

Is a port of [miracle](https://github.com/kolypto/nodejs-miracle/) for NodeJS.






Table of Contents
=================






Reference
=========

Define The Structure
--------------------

### Acl
To start using miracle, instantiate the `Acl` object:

```js
from acl import Acl
acl = Acl()
```

The `Acl` object keeps track of your *resources* and *permissions* defined on them, handles *grants* over *roles* and
provides utilities to manage them. When configured, you can check the access against the defined state.

### Create

Methods from this section allow you to build the *structure*: list of roles, resources and permissions.

It's not required that you have the structure defined before you start granting the access: the `grant()` method
implicitly creates all resources and permissions that were not previously defined.

Start with defining the *resources* and *permissions* on them, then you can grant a *role* with the access to some
permissions on a resource.

For roles, resources & permissions, any hashable object will do.

#### `add_role(role)`
Define a role.

* `role`: the role to define.

The role will have no permissions granted, but will appear in `list_roles()`.

```js
acl.add_role('admin')
acl.list_roles() // -> ['admin']
```

#### `add_resource(resource)`
Define a resource.

* `resources`: the resource to define.

The resource will have no permissions defined but will list in `list_resources()`.

```js
acl.add_resource('blog')
acl.list_resources() // -> ['blog']
```

#### `add_permission(resource, permission)`
Define a permission on a resource.

* `resource`: the resource to define the permission on.
    Is created if was not previously defined.
* `permission`: the permission to define.

The defined permission is not granted to anyone, but will appear in `list_permissions(resource)`.

```js
acl.add_permission('blog', 'post')
acl.list_permissions('blog') // -> ['post']
```

#### `add(structure)`
Define the whole resource/permission structure with a single object.

* `structure`: an object that maps resources to an iterable of permissions.

```js
acl.add({
    'blog': ['post'],
    'page': {'create', 'read', 'update', 'delete'},
})
```

### Remove
#### `remove_role(role)`
Remove the role and its grants.

* `role`: the role to remove.

```js
acl.remove_role('admin')
```

#### `remove_resource(resource)`
Remove the resource along with its grants and permissions.

* `resource`: the resource to remove.

```js
acl.remove_resource('blog')
```

#### `remove_permission(resource, permission)`
Remove the permission from a resource.

* `resource`: the resource to remove the permission from.
* `permission`: the permission to remove.

The resource is not implicitly removed: it remains with an empty set of permissions.

```js
acl.remove_permission('blog', 'post')
```

### List

#### `list_roles()`
Get the list of defined roles.

```js
acl.list_roles() // -> ['admin', 'anonymous', 'registered']
```

#### `list_resources()`
Get the list of defined resources, including those with empty permissions list.

```js
acl.list_resources() // -> ['blog', 'page', 'article']
```

#### `list_permissions(resource)`
Get the list of permissions for a resource.

* `resources`: resource[s] to get the permissions for. Optional.

```js
acl.list_permissions('page') // -> ['create', 'read', 'update', 'delete']
```

#### `list()`
Get the *structure*: hash of all resources mapped to their permissions.

Returns an object: `{ resource: set(permission,...), ... }`.

```js
acl.list(); // -> { blog: {'post'}, page: {'create', ...} }
```

### Export and Import

There's no single 'export everything' method: instead, you sequentially export the list of roles,
the structure (resources and permissions), and the grants:

```js
var miracle = require('miracle');

var acl = new miracle.Acl();

// Export
var save = {
    roles: acl.listRoles(),
    struct: acl.list(),
    grants: acl.show()
};

// Import
acl.addRole(save.roles);
acl.add(save.struct);
acl.grant(save.grants);
```

Note: As the `grant()` method creates resources and roles implicitly, it's usually enough to export the grants.
  You'll only lose roles & resources with empty grants.



Grant Permissions
-----------------

### grant(roles, resources, permissions)
Grant permission[s] over resource[s] to the specified role[s].

Has multiple footprints:

* `grant(roles, resources, permissions)` - grant the listed roles with permissions
    to the listed resources ;
* `grant(roles, grants)` - grant permissions using a grant object that maps
    a list of permissions to a resource: `{ resource: [perm, ...] }`.

Roles, resources and permissions are implicitly created if missing.

```js
acl.grant(['admin', 'manager'], 'blog', ['create', 'update']);
acl.grant('anonymous', { page: ['view'] });
```

### revoke(roles[, resources[, permissions]])
Revoke permission[s] over resource[s] from the specified role[s].

Has multiple footprints:

* `revoke(roles)` remove grants from all resources ;
* `revoke(roles, resources)` remove all grants from the listed resources ;
* `revoke(roles, resources, permissions)` remove specific grants
    from the listed resources ;
* `revoke(roles, grants)` - revoke grants using a grant object that maps
    a list of permissions to a resource: `{ resource: [perm, ...], ... }`.

No roles, resources or permissions are removed implicitly.

```js
acl.revoke('anonymous');
acl.revoke(['admin', 'manager'], 'blog', ['create', 'update']);
acl.revoke('anonymous', { page: ['view'] });
```



Authorize
---------

### check(roles[, resources[, permissions]])
Check whether the named role[s] have access to resource[s] with permission[s].

Has multiple footprints:

* `check(roles, resources)`: check whether the role[s] have any access to the
    named resource[s].
* `check(roles, resources, permissions)`: check with a specific set of
    permissions.
* `check(roles, grants)`: check using a grants object.

In order to pass the test, all roles must have access to all resources.

Returns a boolean.

```js
acl.check('admin', 'blog'); // -> true
acl.check(['anonymous'], 'blog', 'read'); // -> true
acl.check('registered', { page: ['update', 'delete'] });
```

### checkAny(roles[, resources[, permissions]])

Same as `check`, but the united permissions are checked.

In order to pass the test, any role having access to any resource is sufficient.

Also supports the `checkAny(roles, grants)` footprint.


Show Grants
-----------

### which(roles)
Collect grants that each of the provided roles have (intersection).

```js
acl.which('admin'); // -> { blog: ['post'] }
```

### whichAny(roles)
Collect grants that any of the provided roles have (union).

```js
acl.which(['anonymous', 'registered']); // -> { page: ['view'] }
```

### show([roles])
Get all grants for the specified roles.

* `roles`: role[s] to get the grants for.

Returns an object `{ role: { resource: [perm, ...] } }`.
Roles that were not defined are not mentioned in the result.

```js
acl.show(); // -> { admin: { blog: ['post'] } }
acl.show('admin');
acl.show(['admin', 'anonymous']);
```
