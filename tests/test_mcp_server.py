"""The MCP server: lists the tools and each tool returns a text result."""
import unittest

from pacland import mcp_server


class TestMcpServer(unittest.TestCase):
    def test_initialize(self):
        result = mcp_server.handle({"method": "initialize"})
        self.assertEqual(result["serverInfo"]["name"], "sextant")

    def test_tools_list_has_the_five_tools(self):
        result = mcp_server.handle({"method": "tools/list"})
        names = {t["name"] for t in result["tools"]}
        self.assertEqual(names, {"sextant_verify", "sextant_claims", "sextant_graph",
                                 "sextant_deficit", "valiant_status"})

    def test_sextant_graph_returns_mechanisms(self):
        result = mcp_server.handle({"method": "tools/call",
                                    "params": {"name": "sextant_graph", "arguments": {}}})
        text = result["content"][0]["text"]
        self.assertIn("Reusable mechanisms", text)

    def test_sextant_claims_lists_verdicts(self):
        result = mcp_server.handle({"method": "tools/call",
                                    "params": {"name": "sextant_claims", "arguments": {}}})
        text = result["content"][0]["text"]
        self.assertIn("FORCED", text)

    def test_sextant_deficit_unknown_domain(self):
        result = mcp_server.handle({"method": "tools/call",
                                    "params": {"name": "sextant_deficit",
                                               "arguments": {"domain": "nope"}}})
        self.assertIn("unknown domain", result["content"][0]["text"])


if __name__ == "__main__":
    unittest.main()
