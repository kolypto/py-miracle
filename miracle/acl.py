from collections import defaultdict, Iterable


class Acl(object):
    def __init__(self):
        #: Set of defined roles
        self._roles = set()

        #: Resources & Permissions: { resource: set(permission) }
        self._structure = defaultdict(set)

        #: Grants: set( (role, resource, permission) )
        self._grants = set()

    #region Add

    def add_role(self, role):
        """ Define a role.

            :param role: Role to define.
                Any hashable object will do
            :rtype: Acl

            Existing roles are not overwritten nor duplicated.
        """
        self._roles.add(role)
        return self

    def add_roles(self, roles):
        """ Define multiple roles

            :param roles: The roles to define
            :rtype: Acl
        """
        self._roles.update(set(roles))
        return self

    def add_resource(self, resource):
        """ Define a resource.

            :param resource: Resource to define.
                For now, it will have an empty set of permissions
            :rtype: Acl

            Existing resources are not overwritten nor duplicated
        """
        if resource not in self._structure:
            self._structure[resource] = set()
        return self

    def add_permission(self, resource, permission):
        """ Define permission on a resource

            :param resources: Resource to define the permission on.
            :param permission: Permission to define.
            :rtype: Acl

            The resource is created if missing.
            Existing permissions are not overwritten nor duplicated
        """
        self._structure[resource].add(permission)
        return self

    def add(self, structure):
        """ Define the whole structure of resources and permissions

            :type structure: dict
            :param structure: A dict {resource: [permissions]}
            :rtype: Acl
        """
        for resource, permissions in structure.items():
            for permission in permissions:
                self._structure[resource].add(permission)
        return self

    #endregion

    #region Delete

    def clear(self):
        """ Clear the Acl completely

            This removes all roles, resources, permissions ans grants
        """
        self._roles.clear()
        self._structure.clear()
        self._grants.clear()
        return self

    def del_role(self, role):
        """ Remove a role. The grants remain.

            :param roles: Role to remove
            :rtype: Acl

            Undefined roles are silently ignored
        """
        self._roles.discard(role)
        self._grants = set([x for x in self._grants if x[0] != role])
        return self

    def del_resource(self, resource):
        """ Remove a resource and its permissions. The grants remain.

            :param resource: Resource to remove
            :rtype: Acl

            Undefined resources are silently ignored
        """
        if resource in self._structure:
            del self._structure[resource]
        self._grants = set([x for x in self._grants if x[1] != resource])
        return self

    def del_permission(self, resource, permission):
        """ Remove a permission from the resource. The grants remain.

            :param resource: The resource to remove the permission from
            :param permission: Permission to remove
            :rtype: Acl

            Undefined resources and permissions are silently ignored
        """
        if resource in self._structure:
            self._structure[resource].discard(permission)
        self._grants = set([x for x in self._grants if x[2] != permission])
        return self

    #endregion

    #region Get

    def get_roles(self):
        """ Get the list of roles.

            :rtype: list
        """
        return set(self._roles)

    def get_resources(self):
        """ Get the list of resources

            :rtype: list
        """
        return set(self._structure.keys())

    def get_permissions(self, resource):
        """ Get the list of permissions on a resource

            :param resource: The resource to list the permissions for
            :rtype: list
        """
        if resource not in self._structure:
            return set()
        return set(self._structure[resource])

    def get(self):
        """ Get the whole structure of resources and permissions

            Returns { resource: set(permission) }

            :rtype: dict
        """
        ret = {}
        for resource, permissions in self._structure.items():
            ret[resource] = set(permissions)
        return ret

    #endregion

    #region Grant Permissions

    def grant(self, role, resource, permission):
        """ Grant a permission over resource to the role.

            Missing entities are added to the structure

            :param role: The role to grant the access to
            :param resource: The resource to grant the access over
            :param permission: The permission to grant with
            :rtype: Acl
        """
        self.add_role(role)
        self.add_resource(resource)
        self.add_permission(resource, permission)
        self._grants.add((role, resource, permission))
        return self

    def grants(self, grants):
        """ Add a structure of grants to the Acl

            Input: { role: { resource: set(permissions) } }

            :param grants: Grants structure to add
            :rtype: Acl
        """
        for role, gs in grants.items():
            self.add_role(role)
            for resource, permissions in gs.items():
                self.add_resource(resource)
                for permission in permissions:
                    self.add_permission(resource, permission)
                    self._grants.add((role, resource, permission))
        return self

    def revoke(self, role, resource, permission):
        """ Revoke a permission over a resource from the specified role.

            :param role: The role to modify
            :param resource: The resource to modify
            :param permission: The permission to revoke
            :rtype: Acl
        """
        self._grants.discard((role, resource, permission))
        return self

    def revoke_all(self, role, resource=None):
        """ Revoke all permissions from the specified role [over the specified resource]

            :param role: The role to revoke all permissions from
            :param resource: The resource to revoke the permissions from. Optional: revokes from all resources
            :rtype: Acl
        """
        self._grants = { g for g in self._grants if not (g[0] == role and (resource is None or g[1] == resource)) }
        return self

    #endregion

    #region Check

    def check(self, role, resource, permission):
        """ Test whether the given role has access to the resource with the specified permission.

            :param role: The role to check the access for
            :param resource: The resource to check the access for
            :param permission: The permission to check the access with
            :rtype: bool
        """
        return (role, resource, permission) in self._grants

    def check_any(self, roles, resource, permission):
        """ Test whether ANY of the given roles have access to the resource with the specified permission.

            :param roles: Roles collection to check the access for
            :param resource: The resource to check the access for
            :param permission: The permission to check the access with
            :rtype: bool
        """
        # No roles
        if not roles or not isinstance(roles, Iterable):
            return False

        # Any
        for role in roles:
            if (role, resource, permission) in self._grants:
                return True
        return False

    def check_all(self, roles, resource, permission):
        """ Test whether ALL of the given roles have access to the resource with the specified permission.

            :param roles: Roles collection to check the access for
            :param resource: The resource to check the access for
            :param permission: The permission to check the access with
            :rtype: bool
        """
        # No roles
        if not roles or not isinstance(roles, Iterable):
            return False

        # all
        for role in roles:
            if not (role, resource, permission) in self._grants:
                return False
        return True

    #endregion

    #region Show Grants

    def which(self, role):
        """ Collect grants that the provided role has

            Returns: { resource: set(permission) }

            :param role: The role to show the grants for
            :rtype: dict
        """
        ret = defaultdict(set)
        for (r, resource, permission) in filter(lambda x: x[0] == role, self._grants):
            ret[resource].add(permission)
        return dict(ret)

    def which_any(self, roles):
        """ Collect grants that ANY of the provided roles have

            Returns: { resource: set(permission) }

            :param roles: The roles to show the grants for
            :rtype: dict
        """
        # No roles
        if not roles or not isinstance(roles, Iterable):
            return {}

        # Union
        ret = defaultdict(set)
        for (r, resource, permission) in filter(lambda x: x[0] in roles, self._grants):
            ret[resource].add(permission)
        return dict(ret)

    def which_all(self, roles):
        """ Collect grants that ALL of the provided roles have

            Returns: { resource: set(permission) }

            :param roles: The roles to show the grants for
            :rtype: dict
        """
        # No roles
        if not roles or not isinstance(roles, Iterable):
            return {}

        # Collect grants for each role
        grants = {role: self.which(role) for role in roles}

        # Start with the first one
        if not grants:
            return dict()
        ret = grants.popitem()[1]

        # Intersect them
        for role, gs in grants.items():
            for resource in list(ret.keys()):
                if resource in gs:
                    ret[resource] &= gs[resource]
                else:
                    del ret[resource]

        # Finish
        return dict(ret)

    def show(self):
        """ Show all current grants

            Returns: { role: { resource: set(permission) } }

            :rtype: dict
        """
        ret = defaultdict(lambda: defaultdict(set))
        for (role, resource, permission) in self._grants:
            ret[role][resource].add(permission)
        return dict(ret)

    #endregion

    #region Export & Import

    def __getstate__(self):
        return {
            'roles': self.get_roles(),
            'struct': self.get(),
            'grants': self.show()
        }

    def __setstate__(self, state):
        self.add_roles(state['roles'])
        self.add(state['struct'])
        self.grants(state['grants'])
        return self

    #endregion
