
class Acl(object):
    def __init__(self):
        #: Set of defined roles
        self._roles = set()

        #: Resources & Resources mapped to sets of permissions
        self._structure = {}

        #: Grants: { role: { resource: set(permissions) } }
        self._grants = {}

    #region Create

    def add_role(self, *roles):
        """ Define roles.

            :type roles: list
            :param roles: Roles to define
                Any hashable objects will do

            :rtype: Acl

            Existing roles are not overwritten nor duplicated.
        """
        for role in roles:
            self._roles.add(role)
        return self

    def add_resource(self, *resources):
        """ Define resources.

            :type roles: list
            :param roles: Resources to define. For now, they will have empty set of permissions

            Existing resources are not overwritten nor duplicated
        """
        for res in resources:
            if res not in self._structure:
                self._structure[res] = set()
        return self

    #endregion

    #region Delete

    def del_role(self, *roles):
        """ Remove roles and their grants.

            :type roles: list
            :param roles: Roles to remove

            :rtype: Acl
        """
        for role in roles:
            self._roles.discard(role)
        return self

    def del_resource(self, *resources):
        """ Remove resources along with their grants and permissions

            :type resources: list
            :param resources: Resources to remove

            :rtype: Acl
        """
        for res in resources:
            if res in self._structure:
                del self._structure[res]
        return self

    #endregion

    #region List

    def list_roles(self):
        """ Get the list of defined roles.

            :rtype: list
        """
        return list(self._roles)

    def list_resources(self):
        """ Get the list of defines resources

            :rtype: list
        """
        return self._structure.keys()

    #endregion
