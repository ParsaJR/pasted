from app.utils.manage import create_super_admin

asciiart = r"""
 ____              _       _
| __ )  ___   ___ | |_ ___| |_ _ __ __ _ _ __
|  _ \ / _ \ / _ \| __/ __| __| '__/ _` | '_ \
| |_) | (_) | (_) | |_\__ \ |_| | | (_| | |_) |
|____/ \___/ \___/ \__|___/\__|_|  \__,_| .__/
                                        |_|

"""


def main():
    print(asciiart, "\n")
    try:
        create_super_admin()
    except Exception as e:
        print(f"Something went wrong: {e}")
        return

    print("Done!")


if __name__ == "__main__":
    main()
