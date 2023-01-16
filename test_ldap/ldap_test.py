import ldap3

server = ldap3.Server('messenger.com')
conn = ldap3.Connection(server, user='cn=admin,dc=messenger,dc=com', password='tekup')
conn.bind()

schema = conn.server.schema
