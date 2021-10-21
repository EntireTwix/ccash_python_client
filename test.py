import ccash_python_client as ccash


def bold(val: str) -> str:
    return f"\x1b[1m{val}\x1b[m"


def success(val: bool) -> str:
    return f"\x1b[1m\x1b[3{chr(ord('1') + int(val))}m{str(val)}" \
            "\x1b[m"

def expect(name: str, code: int, val) -> None:
    print(f"{name} {success(code == val.status_code)}")
    print(f"Expects {bold(code)}," \
            f" returned {bold(val.status_code)}.\n")

    print("Request data:")
    print(val.request.headers)

    body = str(val.request.body)[2:-1]
    if body:
        print(body, end="\n\n")
    else:
        print("No meaningful body data.\n\n")

    print("Response data:")
    print(val.headers)

    content = str(val.content)[2:-1]
    if content != "" and content != None:
        print(content, end="\n\n\n")
    else:
        print("No meaningful body data.\n\n")


def main():
    ## Test server, values subject to change
    server = ccash.CCash("https://wtfisthis.tech/", 5)
    admin  = ccash.User("admin", "AdminPassword")
    user1  = ccash.User("clienttest1", "01234")
    user2  = ccash.User("clienttest2", "56789")
    
    expect("del_user", 204, server.del_user(user1))
    expect("admin_del_user", 204, 
            server.admin_del_user(admin, user2.name))
    
    expect("new_user", 204, server.new_user(user1))
    expect("admin_new_user", 204, 
            server.admin_new_user(admin, user2, 10000))

    expect("user_exists", 204, server.user_exists(user1.name))
    expect("verify_passwd", 204, server.verify_passwd(user1))
    expect("verify_admin", 204, server.verify_admin(admin))

    expect("change_passwd", 204, 
            server.change_passwd(user1, "56789"))
    expect("admin_change_passwd", 204, 
            server.admin_change_passwd(admin, user2.name, "01234"))

    user1.passwd = "56789"
    user2.passwd = "01234"

    expect("get_bal", 200, server.get_bal(user2.name))
    expect("set_bal", 204, server.set_bal(admin, user1.name, 10000))
    expect("impact_bal", 200, 
            server.impact_bal(admin, user2.name, -5000))

    expect("send", 200, server.send(user2, user1.name, 5000))
    expect("get_logs", 200, server.get_logs(user2))
    expect("prune", 200, server.prune(admin, 120, 0))

    ## Changing passwords back for next test cycle
    expect("change_passwd", 204, 
            server.change_passwd(user1, "01234"))
    expect("admin_change_passwd", 204, 
            server.admin_change_passwd(admin, user2.name, "56789"))


if __name__ == "__main__":
    main()
