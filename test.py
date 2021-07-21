import CCashPythonClient as CCash


def bold(val: str):
    return f"\x1b[1m{val}\x1b[0m"


def expect(name: str, code: int, val) -> None:
    print(f"{name} {bold(code == val.status_code)}")
    print(f"Expects {bold(code)}, returned {bold(val.status_code)}.\n")

    print("Request data:")
    print(val.request.headers)
    print(val.request.body, end="\n\n")

    print("Response data:")
    print(val.headers)

    content = str(val.content)
    if content != "b''" and content != None:
        print(str(val.content)[2:-1], end="\n\n\n")
    else:
        print("No meaningful body data.\n\n")


def main():
    ## Test server, values subject to change
    server = CCash.CCash("https://wtfisthis.tech/")
    admin  = CCash.User("admin", "AdminPassword")
    user1  = CCash.User("clienttest1", "01234")
    user2  = CCash.User("clienttest2", "56789")
    
    expect("del_user", 204, server.del_user(user1))
    expect("admin_del_user", 204, server.admin_del_user(admin, user2.name))
    
    expect("new_user", 204, server.new_user(user1))
    expect("admin_new_user", 204, server.admin_new_user(admin, user2, 10000))


if __name__ == "__main__":
    main()
