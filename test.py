import CCashPythonClient as CCash

## Test server, values subject to change
server = CCash.CCash("https://wtfisthis.tech/")
admin = CCash.User("Admin", "AdminPassword")
user = CCash.User("PythonClientTest", "123456")

status = server.del_user(user)
print(status)

status = server.new_user("PythonClientTest", "123456")
print(status)
