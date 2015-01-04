
import unittest
from pygraph.classes.digraph import digraph as pydigraph
from pagerank_weighted import pagerank_weighted as pagerank


class TestPagerankWeighted(unittest.TestCase):

    def setUp(self):
        pass

    @unittest.skip("Not working at the moment")
    def test_pagerank_run_on_empty_graph(self):
        graph = pydigraph()
        result = pagerank(graph)
        self.assertIsNotNone(result)

    def test_pagerank_run_on_graph_with_a_single_vertex(self):
        graph = pydigraph()
        graph.add_node("TEST_LINE")
        result = pagerank(graph)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()

