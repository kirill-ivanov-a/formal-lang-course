from antlr4 import InputStream, CommonTokenStream

from project.gql_grammar.GraphQueryLanguageLexer import GraphQueryLanguageLexer
from project.gql_grammar.GraphQueryLanguageParser import GraphQueryLanguageParser

__all__ = ["accept", "parse"]


def parse(text: str) -> GraphQueryLanguageParser:
    input_stream = InputStream(text)
    lexer = GraphQueryLanguageLexer(input_stream)
    lexer.removeErrorListeners()
    stream = CommonTokenStream(lexer)
    parser = GraphQueryLanguageParser(stream)

    return parser


def accept(text: str) -> bool:
    parser = parse(text)
    parser.removeErrorListeners()
    _ = parser.prog()
    return parser.getNumberOfSyntaxErrors() == 0
