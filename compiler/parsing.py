import abc
import io
from architecture import Architecture, Operation

from logzero import logger

from pyparsing import *
from pyparsing.diagram import to_railroad, railroad_to_html

# Do not treat newlines as whitespace
ParserElement.set_default_whitespace_chars(' \t')

def make_keyword(operation: Operation):
    return Keyword(operation.name).set_parse_action(lambda: operation)

def make_operations(arch: Architecture):
    return Or([make_keyword(op) for op in arch.operations])


class ParserBase(abc.ABC):
    def __init__(self, parser):
        self.parser = parser
        logger.debug('Parser: %s', self.parser)

    def parse(self, input: io.TextIOBase):
        tokens = self.parser.parse_file(input, parse_all=True)
        for i, token in enumerate(tokens):
            logger.debug('Parsed line:\n[%d]: %s', i+1, token.dump())
        return tokens

    def write_diagram(self, output: io.TextIOBase):
        railroad = to_railroad(self.parser)
        html = railroad_to_html(railroad)
        output.write(html)
    
    def run_tests(self, tests:str):
        self.parser.run_tests(tests)