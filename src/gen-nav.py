import shutil
import sys
import pathlib
import yaml


def read_yaml(fname: str) -> list | dict:
    with open(fname, "r") as f:
        config = yaml.safe_load(f)
    return config


def write_yaml(fname: str, obj: dict) -> None:
    with open(fname, "w") as f:
        yaml.dump(obj, f)


def append_yaml(fname: str, obj: dict) -> None:
    with open(fname, "a") as f:
        yaml.dump(obj, f)


def description(file_or_dir: pathlib.Path) -> str:
    return file_or_dir.stem


def to_fname(file: pathlib.Path) -> str:
    return file.relative_to("docs").as_posix()


def convert(file_or_dir: pathlib.Path) -> dict:
    if file_or_dir.is_file():
        return {description(file_or_dir): to_fname(file_or_dir)}
    return {
        description(file_or_dir): sorted(
            ({description(file): to_fname(file)} for file in file_or_dir.glob("*.md")),
            key=lambda d: next(iter(d.keys())),
        )
    }


def main():
    fnames_and_dirnames = read_yaml("nav.yml")
    # print(fnames_and_dirnames)
    nav = [
        convert(pathlib.Path("docs") / fname_or_dirname)
        for fname_or_dirname in fnames_and_dirnames
    ]
    # # print(nav)
    # mkdocs = read_yaml("mkdocs.yml.orig")
    # mkdocs["nav"] = nav
    # # print(mkdocs)
    # write_yaml("mkdocs.yml", mkdocs)
    shutil.copy("mkdocs.yml.orig", "mkdocs.yml")
    append_yaml("mkdocs.yml", {"nav": nav})


if __name__ == "__main__":
    sys.exit(main())
