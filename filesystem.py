import time

class Node:
    def __init__(self, name, is_file=False):
        self.name = name
        self.is_file = is_file
        self.content = "" if is_file else None
        self.children = {} if not is_file else None
        self.created = time.time()

class FileSystem:
    def __init__(self):
        self.root = Node("/")
        self.current = self.root
    
    def _get_node(self, path):
        if path == "/":
            return self.root
        parts = path.strip("/").split("/")
        node = self.root
        for part in parts:
            if not node.children or part not in node.children:
                return None
            node = node.children[part]
        return node
    
    def mkdir(self, path):
        parts = path.strip("/").split("/")
        node = self.root
        for part in parts:
            if part not in node.children:
                node.children[part] = Node(part)
            node = node.children[part]
        return f"Directory created: {path}"
    
    def touch(self, path):
        parts = path.strip("/").split("/")
        node = self.root
        for part in parts[:-1]:
            if part not in node.children:
                return "Path not found"
            node = node.children[part]
        node.children[parts[-1]] = Node(parts[-1], is_file=True)
        return f"File created: {path}"
    
    def write(self, path, content):
        node = self._get_node(path)
        if node and node.is_file:
            node.content = content
            return "Written successfully"
        return "File not found"
    
    def read(self, path):
        node = self._get_node(path)
        if node and node.is_file:
            return node.content
        return "File not found"
    
    def ls(self, path="/"):
        node = self._get_node(path)
        if not node:
            return []
        if node.is_file:
            return [node.name]
        return list(node.children.keys())

if __name__ == "__main__":
    fs = FileSystem()
    print(fs.mkdir("/home/user"))
    print(fs.touch("/home/user/file.txt"))
    print(fs.write("/home/user/file.txt", "Hello World"))
    print(fs.read("/home/user/file.txt"))
    print("Contents of /home/user:", fs.ls("/home/user"))
