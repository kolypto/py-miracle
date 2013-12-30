
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
        """ Define role[s].

            :type roles: list
            :param roles: list Role[s] to define
                Any hashable objects will do

            :rtype: Acl

            Existing roles are not overwritten nor duplicated.
        """
        for role in roles:
            self._roles.add(role)
        return self

    #endregion

    #region Delete

    def del_role(self, *roles):
        """ Remove role[s] and their grants.

            :type roles: list|str
            :param roles: list Role[s] to remove

            :rtype: Acl

            Existing roles are not overwritten nor duplicated.
        """
        for role in roles:
            self._roles.discard(role)
        return self

    #endregion

    #region List

    def list_roles(self):
        """ Get the list of defined roles.

            :rtype: list
        """
        return list(self._roles)

    #endregion
