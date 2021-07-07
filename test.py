import CCashPythonClient as CCash

## Test server, values subject to change
server = CCash.CCash("https://wtfisthis.tech/")
admin  = CCash.User("Admin", "AdminPassword")
user1  = CCash.User("ClientTest1", "01234")
user2  = CCash.User("ClientTest2", "56789")

print(server.del_user(user1) == 200,                        "del_user")
print(server.admin_del_user(admin, user2.name) == 200,      "admin_del_user")

print(server.new_user(user1) == 200,                        "new_user")
print(server.admin_new_user(admin, user2, 10000) == 200,    "admin_new_user")

print(server.impact_bal(admin, user2.name, -5000) == 200,   "impact_bal")
print(server.get_bal(user2.name) == 5000,                   "get_bal")
print(server.set_bal(admin, user2.name, 10000) == 200,      "set_bal")

print(server.change_passwd(user2, "01234") == 200,          "change_passwd")
user2.passwd = "01234"
print(server.verify_passwd(user2) == 200,                   "verify_passwd")
