from ldap3 import Server, Connection, SUBTREE, ALL_ATTRIBUTES

SEARCH_BASE = 'ou=users,dc=,dc=com'


class LDAPAuth(object):

    def __init__(self, host, admin_user, admin_password):
        ldap_server_pool = Server(host)
        self.search_base = SEARCH_BASE

        conn = Connection(ldap_server_pool, user=admin_user, password=admin_password, check_names=True, lazy=False,
                          raise_exceptions=False)
        conn.open()
        conn.bind()
        self.conn = conn

    def search(self, username=None):
        """
        username 必须是 用户姓名的拼音, 即 ldap 登记用名.

        name: obj[1][sAMAccountName][0]
        name_cn: obj[1][name][0]
        email: obj[1][email][0]
        """
        self.conn.search(
            search_base=self.search_base,
            search_filter=f'(uid={username})',
            # search_filter=f'(objectclass=person)',
            search_scope=SUBTREE,
            # attributes = ['cn', 'givenName', 'mail', 'sAMAccountName','department','manager'],
            # ALL_ATTRIBUTES：获取所有属性值
            attributes=ALL_ATTRIBUTES,
            paged_size=5
        )

        return self.conn.response[0]

    def list_ad_users(self, search_base=SEARCH_BASE):
        result = self.conn.extend.standard.paged_search(
            search_base=search_base,
            # search_base='ou=users,dc=,dc=com',
            # search_base=self.search_base,
            # search_filter=f'(&(objectClass=person))',
            search_filter=f'(objectClass=inetOrgPerson)',
            search_scope=SUBTREE,
            # attributes = ['cn', 'givenName', 'mail', 'sAMAccountName','department','manager'],
            # ALL_ATTRIBUTES：获取所有属性值
            attributes=ALL_ATTRIBUTES,
            # size_limit=10000,
            # time_limit=10,
            # paged_size=5,
            # generator=False,
            get_operational_attributes=True
        )
        return result

    def test_list(self):
        total_entries = 0
        c = self.conn
        c.search(search_base=SEARCH_BASE,
                 search_filter='(objectClass=inetOrgPerson)',
                 search_scope=SUBTREE,
                 attributes=['cn', 'givenName'],
                 paged_size=5)
        total_entries += len(c.response)
        for entry in c.response:
            print(entry['dn'], entry['attributes'])
        cookie = c.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
        while cookie:
            print(total_entries)
            c.search(search_base=SEARCH_BASE,
                     search_filter='(objectClass=inetOrgPerson)',
                     search_scope=SUBTREE,
                     attributes=['cn', 'givenName'],
                     paged_size=5,
                     paged_cookie=cookie)
            total_entries += len(c.response)
            cookie = c.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
            for entry in c.response:
                print(entry['dn'], entry['attributes'])
        print(total_entries)


if __name__ == '__main__':
    cli = LDAPAuth('', '', '')
    # cli.test_list()
    # r = cli.search('chenpuyu')
    r = cli.list_ad_users()


    print(r)
    # print(set(engineer_usernames).difference(set(usernames)))
