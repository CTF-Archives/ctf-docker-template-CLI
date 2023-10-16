from tabulate import tabulate
import docker


class SrcList:
    def __init__(self) -> None:
        pass

    def get_list(self, mode: str = "all"):
        with open("./src-list.txt", "r") as f:
            src = f.read()
            src = src.split("\n")
            src = [
                i[47:]
                for i in src
                if i.split(" ")[9].split("-")[0] in ["crypto", "misc", "pwn", "reverse", "web"]
            ]
            src = [i.split("-", maxsplit=1) for i in src]
            src.sort()
        match mode:
            case "all":
                return src
            case "crypto":
                return [i for i in src if i[0] == "crypto"]
            case "misc":
                return [i for i in src if i[0] == "misc"]
            case "pwn":
                return [i for i in src if i[0] == "pwn"]
            case "reverse":
                return [i for i in src if i[0] == "reverse"]
            case "web":
                return [i for i in src if i[0] == "web"]
            case _:
                return src

    def format_list(self, mode: str):
        return tabulate(
            self.get_list(mode=mode),
            headers=["Category", "Template"],
            tablefmt="fancy_grid",
        )


class DockerManger(docker.DockerClient):
    def __init__(self):
        super().__init__()

    def connect(self, mode: str):
        match mode:
            case "local":
                self.client = docker.from_env()
            case "remote-plain":
                pass
            case "remote-tls":
                pass

    def get_images(self):
        images = self.images.list()
        return images

    def get_containers(self):
        containers = self.client.containers.list()
        return containers


core_srclist = SrcList()
core_docker = DockerManger()

if __name__ == "__main__":
    core_docker = DockerManger(mode="local")
