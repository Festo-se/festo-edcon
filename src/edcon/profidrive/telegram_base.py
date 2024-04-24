"""Contains code that is related to PROFIDRIVE telegram base class"""

from dataclasses import fields


class TelegramBase:
    """Holds the base implementation of PROFIDRIVE telegrams"""

    def __post_init__(self):
        """Post initialization hook"""
        # Convert any attributes of type int to the correct type
        for item in fields(self):
            if isinstance(getattr(self, item.name), int):
                setattr(
                    self,
                    item.name,
                    item.default_factory().from_int(getattr(self, item.name)),
                )

            if not isinstance(getattr(self, item.name), type(item.default_factory())):
                raise ValueError(f"Invalid value type of {item.name}")

    def __len__(self):
        len_list = [len(getattr(self, item.name)) for item in fields(self)]
        return sum(len_list)

    def __repr__(self):
        """Implements a nicer representation for TelegramBase class"""
        attrs = [(item.name, getattr(self, item.name)) for item in fields(self)]
        val_str = ", ".join(
            [
                f"{n.upper()}=0x"
                f"{int.from_bytes(v.to_bytes(), 'little'):0{len(v) * 2}X}"
                for n, v in attrs
            ]
        )

        return f"{type(self).__name__}({val_str})"

    def reset(self):
        """Clears all attributes to default values."""
        for item in fields(self):
            setattr(
                self,
                item.name,
                item.default_factory(),
            )

    def inputs(self):
        """Returns list of input words"""
        raise NotImplementedError

    def outputs(self):
        """Returns list of output words"""
        raise NotImplementedError

    def input_bytes(self, data: bytes):
        """Sets the input words from provided byte data"""
        pos = 0
        for inp in self.inputs():
            inp_name = type(inp).__name__.lower().replace("_pm", "").replace("_sm", "")
            setattr(
                self,
                inp_name,
                inp.from_bytes(data[pos : pos + inp.byte_size]),
            )
            pos += inp.byte_size

    def output_bytes(self) -> bytes:
        """Returns the byte representation of the output words"""
        out_bytes = b""
        for outp in self.outputs():
            out_bytes += outp.to_bytes()
        return out_bytes
