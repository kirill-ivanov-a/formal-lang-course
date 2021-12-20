import pytest
import os

from project.parsing_utils import generate_dot
from antlr4.error.Errors import ParseCancellationException


def test_write_dot(tmpdir):
    text = """g = load graph "hello";
g = set start of (set final of g to (select vertices from g)) to {1..100};
l1 = "l1" | "l2";
q1 = ("type" | l1)*;
q2 = "subclass_of" . q;
res1 = g & q1;
res2 = g & q2;
s = select start vertices from g;
vertices1 = filter (fun v: v in s) (map (fun ((u_g,u_q1),l,(v_g,v_q1)): u_g) (select edges from res1));
vertices2 = filter (fun v: v in s) (map (fun ((u_g,u_q2),l,(v_g,v_q1)): u_g) (select edges from res2));
vertices3 = vertices1 & vertices2;

print vertices3;
"""
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.sep.join([root_path, "tests", "data", "example.dot"])
    file = tmpdir.mkdir("test_dir").join("two_cycles.dot")

    generate_dot(text, file)

    with open(path, "r") as file1:
        with open(file, "r") as file2:
            assert file1.read() == file2.read()


def test_incorrect_text():
    text = """g = load graph "skos";
common_labels = (select lables from g) & (select labels from (load graph "graph.txt"));

print common_labels;"""
    with pytest.raises(ParseCancellationException):
        generate_dot(text, "test")
