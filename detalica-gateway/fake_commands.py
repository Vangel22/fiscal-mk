from dataclasses import dataclass
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

@dataclass
class PrinterCommand:
    command_type: str
    context: "Context"


@dataclass
class Context:
    vendor: str
    items: list["Item"]


@dataclass
class Item:
    idx: int
    name: str
    quantity: float
    price: int


def main():
    fake_command = PrinterCommand(
        command_type="ECRPrint",
        context=Context(
            vendor="Accent",
            items=[
                Item(idx=0, name="Smoki", quantity=1, price=10)
            ]
        )
    )

    if fake_command.context.vendor == "Accent":
        with TemporaryDirectory() as tmp_dir:
            in_file = generate_in_file(fake_command, Path(tmp_dir))
            execute_accent_dll(in_file)

        return

    else:
        raise RuntimeError("Unsupported Vendor")


def generate_in_file(command: PrinterCommand, working_dir: Path) -> Path:
    in_file = working_dir / "ecrprint.in"

    initializers = [
        "01,0000,1"
    ]
    rows = [
        f"#{item.idx}{item.name} >{item.price}*{item.quantity}"
        for item in command.context.items
    ]
    finalizers = [
        "&5",
        "%8"
    ]


    with in_file.open("w") as fp:
        for row in [*initializers, *rows, *finalizers]:
            fp.write(f"{row}\n")

    return in_file


def execute_accent_dll(in_file: Path) -> None:
    try:
        subprocess.run(["./fake_accent.exe", f"{in_file.as_posix()}"])
    except Exception:
        raise RuntimeError()

if __name__ == "__main__":
    main()