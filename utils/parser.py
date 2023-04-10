import configargparse as cfargparse
import os
import warnings


class ArgumentParser(cfargparse.ArgumentParser):
    def __init__(
        self,
        config_file_parser_class=cfargparse.YAMLConfigFileParser,
        formatter_class=cfargparse.ArgumentDefaultsHelpFormatter,
        **kwargs
    ):
        super(ArgumentParser, self).__init__(
            config_file_parser_class=config_file_parser_class,
            formatter_class=formatter_class,
            **kwargs
        )

    @classmethod
    def defaults(cls, *args):
        """Get default arguments added to a parser by all ``*args``."""
        dummy_parser = cls()
        for callback in args:
            callback(dummy_parser)
        defaults = dummy_parser.parse_known_args([])[0]
        return defaults
