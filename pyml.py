import sys
import yaml
import ast
import io
import argparse


def first_dict_item(d: dict) -> tuple:
    return next(iter(d.items()))


class ASTDumper(yaml.dumper.SafeDumper):
    def represent_undefined(dumper, data):
        if isinstance(data, ast.AST):
            field_dict = dict((k, v) for k, v in ast.iter_fields(data) if v != None)
            return dumper.represent_dict(
                {"$" + str(data.__class__.__name__): field_dict}
            )
        return super(PrettyYAMLDumper, dumper).represent_undefined(data)


ASTDumper.add_representer(None, ASTDumper.represent_undefined)


def dump_tree(tree):
    yaml_buf = io.BytesIO()
    yaml.dump(
        tree,
        yaml_buf,
        Dumper=ASTDumper,
        default_flow_style=False,
        allow_unicode=True,
        encoding="utf-8",
    )
    yaml_data = yaml_buf.getvalue().decode()
    return yaml_data


def walk_tree(tree):
    def walk_node(node):
        if isinstance(node, dict):
            if len(node) == 1:
                name, body = first_dict_item(node)
                if name[0] == "$":
                    node_cls = getattr(ast, name[1:])
                    return node_cls(**walk_node(body))
            return {k: walk_node(v) for (k, v) in node.items()}
        if isinstance(node, list):
            return [walk_node(i) for i in node]
        elif isinstance(node, (int, str)):
            return node
        print("??", node, file=sys.stderr)
        return node

    root = walk_node(tree)
    ast.fix_missing_locations(root)
    return root


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dump", action="store_true")
    ap.add_argument("-x", "--execute", action="store_true")
    ap.add_argument("file", type=argparse.FileType(), default=sys.stdin)
    args = ap.parse_args()
    if args.dump:
        tree = ast.parse(args.file.read())
        yaml_data = dump_tree(tree)
        print(yaml_data)
    elif args.execute:
        parsed_yaml = yaml.safe_load(args.file)
        root = walk_tree(parsed_yaml)
        x = compile(root, "<string>", "exec")
        exec(x)
    else:
        ap.error("nothing to do (-d or -x)")


if __name__ == "__main__":
    main()
