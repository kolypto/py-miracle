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
var Acl = require('miracle').Acl;

var acl = new Acl();
```

The `Acl` object keeps track of your *resources* and *permissions* defined on them, handles *grants* over *roles* and
provides utilities to manage them. When configured, you can check the access against the defined state.

### Create

Methods from this section allow you to build the *structure*: list of roles, resources and permissions.

It's not required that you have the structure defined before you start granting the access: the `grant()` method
implicitly creates all resources and permissions that were not previously defined.

Start with defining the *resources* and *permissions* on them, then you can grant a *role* with the access to some
permissions on a resource.

#### `addRole(roles)`
Define role[s].

* `roles`: the role[s] to define.

The role will have no permissions granted, but will appear in `listRoles()`.

```js
acl.addRole('admin');
acl.addRole(['anonymous', 'registered']);

acl.listRoles(); // -> ['admin', 'anonymous', 'registered']
```

#### `addResource(resources)`
Define resource[s].

* `resources`: resource[s] to define.

The resource will have no permissions defined but will list in
`listResources()`.

```js
acl.addResource('blog');
acl.addResource(['page', 'article']);

acl.listResources(); // -> ['blog', 'page', 'article']
```

#### `addPermission(resources, permissions)`
Define permission[s] on resource[s].

* `resources`: resource[s] to define the permission on.
    Are created if were not previously defined.
* `permissions`: permission[s] to define.

The defined permissions are not granted to anyone, but will appear in
`listPermissions()`.

```js
acl.addPermission('blog', 'post');
acl.addPermission(['page', 'article'], ['create', 'read', 'update', 'delete']);

acl.listPermissions('page'); // -> ['create', 'read', 'update', 'delete']
```

#### `add(structure)`
Define the whole resource/permission structure with a single object.

* `structure`: an object that maps resources to an array of permissions.

```js
acl.add({
    blog: ['post'],
    page: ['create', 'read', 'update', 'delete'],
    article: ['create', 'read', 'update', 'delete'],
});
```

### Remove
#### `removeRole(roles)`
Remove role[s] and their grants.

* `roles`: role[s] to remove.

```js
acl.removeRole('admin');
acl.removeRole(['anonymous', 'registered']);
```

#### `removeResource(resources)`
Remove resource[s] along with their grants and permissions.

* `resources`: resource[s] to remove.

```js
acl.removeResource('blog');
acl.removeResource(['page', 'article']);
```

#### `removePermission(resources, permissions)`
Remove permission[s] from resource[s].

* `resources`: resource[s] to remove the permissions from.
* `permissions`: permission[s] to remove.

The resource is not implicitly removed: it remains with an empty set of permissions.

```js
acl.removePermissions('blog', 'post');
acl.removePermissions(['page', 'article'], ['create', 'update']);
```

### List

#### `listRoles()`
Get the list of defined roles.

```js
acl.listRoles(); // -> ['admin', 'anonymous', 'registered']
```

#### `listResources()`
Get the list of defined resources, including those with empty permissions list.

```js
acl.listResources(); // -> ['blog', 'page', 'article']
```

#### `listPermissions(resources)`
Get the list of permissions for a resource, or for multiple resources.

* `resources`: resource[s] to get the permissions for. Optional.

```js
acl.listPermissions('page'); // -> ['create', 'read', 'update', 'delete']
acl.listPermissions(['blog', 'page']); // -> ['post', 'create', ... ]
acl.listPermissions(); // -> [ ..all.. ]
```

#### `list([resources])`
Get the *structure*: list of resources mapped to their permissions.

* `resources`: resource[s] to get the structure for. Optional.

Returns an object: `{ resource: [perm, ...] }`.

```js
acl.list(); // -> { blog: ['post'], page: ['create', ...] }
acl.list('blog'); // -> { blog: ['post'] }
acl.list(['blog', 'page']); // -> { blog: ['post'], page: ['create', ...] }
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
