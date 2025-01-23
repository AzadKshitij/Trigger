import orjson as json
from collections import OrderedDict
from node_serializable import Serializable

from node_graphics_scene import QTRGraphicsScene
from node_node import Node
from node_edge import Edge
from node_scene_history import SceneHistory


class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []
        self.scene_width = 64000
        self.scene_height = 64000

        self.initUI()
        self.history = SceneHistory(self)

    def initUI(self):
        self.grScene = QTRGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        self.nodes.remove(node)

    def removeEdge(self, edge):
        self.edges.remove(edge)

    def clear(self):
        while len(self.nodes) > 0:
            self.nodes[0].remove()

    def saveToFile(self, filename):
        print("saveToFile")
        with open(filename, "w") as file:
            print("With Open saveToFile")
            file.write(json.dumps(self.serialize(), option=json.OPT_INDENT_2).decode("utf-8"))
        print("saving to", filename, "was successfull.")

    def loadFromFile(self, filename):
        # TODO: Add loading bar for file
        try:
            # Open and read the file
            with open(filename, "r") as file:
                raw_data = file.read()
                print("Got raw data!")
            # Parse JSON data
            data = json.loads(raw_data)
            print("Data:", data)
            # self.deserialize(data)
            # Deserialize the data
            if hasattr(self, "deserialize") and callable(self.deserialize):
                self.deserialize(data)
            else:
                raise AttributeError("The 'deserialize' method is not implemented or callable.")

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except json.JSONDecodeError as e:
            print(f"Error: Failed to decode JSON. {e}")
        except AttributeError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


    def serialize(self):
        print("Serialize Scene!!")
        nodes, edges = [], []
        for node in self.nodes:
            nodes.append(node.serialize())
        for edge in self.edges:
            edges.append(edge.serialize())
        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.scene_width),
            ('scene_height', self.scene_height),
            ('nodes', nodes),
            ('edges', edges),
        ])

    def deserialize(self, data, hashmap={}):
        self.clear()
        hashmap = {}

        # create nodes
        for node_data in data['nodes']:
            Node(self).deserialize(node_data, hashmap)

        # create edges
        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, hashmap)

        return True

