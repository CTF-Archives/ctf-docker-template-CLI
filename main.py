from tabulate import tabulate
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import clear
from core import core_srclist, core_docker


def print_banner():
    BANNER = r"""
          ____ _____ _____       _             _     _                
         / ___|_   _|  ___|     / \   _ __ ___| |__ (_)_   _____  ___ 
        | |     | | | |_ _____ / _ \ | '__/ __| '_ \| \ \ / / _ \/ __|
        | |___  | | |  _|_____/ ___ \| | | (__| | | | |\ V /  __/\__ \
         \____| |_| |_|      /_/   \_\_|  \___|_| |_|_| \_/ \___||___/
    
                        
                        https://github.com/CTF-Archives
         此 ctf-docker-template-CLI 目前仅为雏形，基于 Python 3.10 编写
       可帮助出题人规划题目整体框架，完成自动化题目构建，题目测试环境一键搭建等等
                 请与 ctf-docker-template 项目搭配使用，效果更佳
    
    """
    print(BANNER)


def convert_bytes(size):
    # 可用的单位
    units = {0: "B", 1: "KB", 2: "MB", 3: "GB", 4: "TB", 5: "PB"}
    unit = 0
    # 将字节数转换为指定单位
    while size >= 1000 and unit != "PB":
        size /= 1000
        unit += 1

    # 格式化结果
    return f"{size:.2f} {units[unit]}"


def interpreter(input: str):
    input = input.strip().split(" ")
    if len(input) == 1 and input[0] == "":
        return 0
    match input[0]:
        case "show":
            try:
                print(core_srclist.format_list(input[1]))
            except:
                print(core_srclist.format_list("all"))
        case "use":
            try:
                message[4] = ("class:path", "/{}/{}".format(input[1], input[2]))
            except:
                print("Invalid Template: {}".format(str(input[0:])))
        case "docker":
            try:
                match input[1]:
                    case "connect":
                        try:
                            match input[2]:
                                case "local":
                                    client = core_docker.connect("local")
                        except:
                            print("Operation Failed, need argument 1: connect mode")
                    case "containers":
                        try:
                            match input[2]:
                                case "list":
                                    print(
                                        tabulate(
                                            [
                                                [
                                                    container.id[0:12],
                                                    "<service> "+container.name.split(".")[0]
                                                    if "." in container.name
                                                    else container.name,
                                                    container.image.tags[0],
                                                    container.status,
                                                ]
                                                for container in core_docker.get_containers()
                                            ],
                                            headers=["容器ID", "容器名称", "容器tag", "容器状态"],
                                            tablefmt="fancy_grid",
                                        )
                                    )
                        except:
                            print("Operation Failed, need argument 1: containers operation")
                    case "images":
                        try:
                            match input[2]:
                                case "list":
                                    print(
                                        tabulate(
                                            [
                                                [
                                                    image.id.split(":")[1][0:12],
                                                    image.tags,
                                                    convert_bytes(image.attrs["Size"]),
                                                ]
                                                for image in core_docker.get_images()
                                            ],
                                            headers=["镜像ID", "标签", "镜像大小"],
                                            tablefmt="fancy_grid",
                                        )
                                    )
                        except:
                            print("Operation Failed, need argument 1: images operation")
            except:
                print("Operation Failed, need argument 1: operation")
        case "about":
            print_banner()
        case "clear":
            clear()
        case "exit":
            exit()
        case _:
            print("{module}: command not found".format(module=input[0]))


style = Style.from_dict(
    {
        "username": "#ED8E29",
        "at": "#00aa00",
        "colon": "#0000aa",
        "pound": "#00aa00",
        "host": "#ED8E29",
        "path": "#76C3A5",
    }
)

message = [
    ("class:username", "Randark"),
    ("class:at", "@"),
    ("class:host", "CTF-Archives"),
    ("class:colon", ":"),
    ("class:path", "/"),
    ("class:pound", "# "),
]


if __name__ == "__main__":
    session = PromptSession()
    completer = NestedCompleter.from_nested_dict(
        {
            "show": {
                "all": None,
                "crypto": None,
                "misc": None,
                "pwn": None,
                "reverse": None,
                "web": None,
            },
            "use": {
                "crypto": dict.fromkeys([i[1] for i in core_srclist.get_list(mode="crypto")]),
                "misc": dict.fromkeys([i[1] for i in core_srclist.get_list(mode="misc")]),
                "pwn": dict.fromkeys([i[1] for i in core_srclist.get_list(mode="pwn")]),
                "reverse": dict.fromkeys([i[1] for i in core_srclist.get_list(mode="reverse")]),
                "web": dict.fromkeys([i[1] for i in core_srclist.get_list(mode="web")]),
            },
            "docker": {
                "connect": {"local": None, "remote": None},
                "containers": {"list": None},
                "images": {"list": None},
            },
            "about": None,
            "clear": None,
            "exit": None,
        }
    )
    clear()
    while True:
        try:
            text = str(session.prompt(message, style=style, completer=completer))
            interpreter(text.lower())
        except:
            print("\n{}\n".format(" >> Terminal Exit << "))
            exit()
