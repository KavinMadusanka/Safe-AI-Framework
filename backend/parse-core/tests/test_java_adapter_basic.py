import os
import sys

# Add project root (parser-core) to sys.path so 'adapters' can be imported
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from adapters.java_adapter import JavaAdapter

def build_edges_set(cir_json):
    return {(e["src"], e["dst"], e["type"]) for e in cir_json["edges"]}

def test_inheritance_and_implements():
    code = """
    interface ICustomer {}

    class BaseCustomer implements ICustomer {}

    class VipCustomer extends BaseCustomer {}
    """
    adapter = JavaAdapter()
    graph = adapter.build_cir_graph_for_code(code)
    data = graph.to_debug_json()
    edges = build_edges_set(data)

    # resolve type IDs
    ids = {n["attrs"]["name"]: n["id"] for n in data["nodes"] if n["kind"] == "TypeDecl"}
    vip_id = ids["VipCustomer"]
    base_id = ids["BaseCustomer"]
    icust_id = ids["ICustomer"]

    assert (vip_id, base_id, "INHERITS") in edges
    assert (base_id, icust_id, "IMPLEMENTS") in edges
