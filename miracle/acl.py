from copy import copy

class Acl(object):
    def __init__(self):
        #: Set of defined roles
        self._roles = set()

        #: Resources & Permissions: { resource: set(permission) }
        self._structure = {}

        #: Grants: { role: { resource: set(permissions) } }
        self._grants = {}

    #region Create

    def add_role(self, role):
        """ Define a role.

            :param role: Role to define.
                Any hashable object will do
            :rtype: Acl

            Existing roles are not overwritten nor duplicated.
        """
        self._roles.add(role)
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
        self.add_resource(resource)
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
                self.add_permission(resource, permission)
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
        """ Remove a role and its grants.

            :param roles: Role to remove
            :rtype: Acl

            Undefined roles are silently ignored
        """
        self._roles.discard(role)
        return self

    def del_resource(self, resource):
        """ Remove a resource along with its grants and permissions

            :param resource: Resource to remove
            :rtype: Acl

            Undefined resources are silently ignored
        """
        if resource in self._structure:
            del self._structure[resource]
        return self

    def del_permission(self, resource, permission):
        """ Remove a permission from the resource, along with its grants

            :param resource: The resource to remove the permission from
            :param permission: Permission to remove
            :rtype: Acl

            Undefined resources and permissions are silently ignored
        """
        if resource in self._structure:
            self._structure[resource].discard(permission)
        return self

    #endregion

    #region List

    def list_roles(self):
        """ Get the list of roles.

            :rtype: list
        """
        return list(self._roles)

    def list_resources(self):
        """ Get the list of resources

            :rtype: list
        """
        return self._structure.keys()

    def list_permissions(self, resource):
        """ Get the list of permissions on a resource

            :rtype: list
        """
        if resource not in self._structure:
            return []
        return list(self._structure[resource])

    def list(self):
        """ Get the whole structure of resources and permissions

            Returns { resource: set(permission) }

            :rtype: dict
        """
        ret = {}
        for resource, permissons in self._structure.items():
            ret[resource] = set(permissons)
        return ret

    #endregion
