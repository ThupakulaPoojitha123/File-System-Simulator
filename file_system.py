class FSNode:
    def __init__(self, name, is_dir=False, permissions="rwx"):
        self.name = name
        self.is_dir = is_dir
        self.children = {} if is_dir else None
        self.permissions = permissions
        self.size = 0

class FileSystem:
    def __init__(self, quota=1000):
        self.root = FSNode("/", is_dir=True)
        self.current = self.root
        self.quota = quota
        self.used = 0
    
    def _get_node(self, path):
        if path == "/":
            return self.root
        parts = path.strip("/").split("/")
        node = self.root
        for part in parts:
            if not node.is_dir or part not in node.children:
                return None
            node = node.children[part]
        return node
    
    def mkdir(self, name):
        if name in self.current.children:
            return f"Error: {name} already exists"
        self.current.children[name] = FSNode(name, is_dir=True)
        return f"Created directory: {name}"
    
    def cd(self, path):
        if path == "..":
            return "Changed to parent"
        node = self._get_node(path) if path.startswith("/") else self.current.children.get(path)
        if node and node.is_dir:
            self.current = node
            return f"Changed to: {path}"
        return f"Error: {path} not found"
    
    def ls(self):
        return list(self.current.children.keys())
    
    def touch(self, name, size=10):
        if self.used + size > self.quota:
            return "Error: Quota exceeded"
        if name in self.current.children:
            return f"Error: {name} already exists"
        self.current.children[name] = FSNode(name, is_dir=False)
        self.current.children[name].size = size
        self.used += size
        return f"Created file: {name}"
    
    def rm(self, name):
        if name not in self.current.children:
            return f"Error: {name} not found"
        node = self.current.children[name]
        if not node.is_dir:
            self.used -= node.size
        del self.current.children[name]
        return f"Removed: {name}"

if __name__ == "__main__":
    print("\n=== FILE SYSTEM SIMULATOR ===")
    quota = int(input("Enter disk quota (MB): "))
    fs = FileSystem(quota)
    
    while True:
        print("\n" + "="*40)
        print(f"Disk Usage: {fs.used}/{fs.quota} MB")
        print("1. mkdir (create directory)")
        print("2. touch (create file)")
        print("3. ls (list contents)")
        print("4. rm (remove)")
        print("5. cd (change directory)")
        print("6. Exit")
        choice = input("Enter choice: ")
        
        if choice == '1':
            name = input("Enter directory name: ")
            print(fs.mkdir(name))
        elif choice == '2':
            name = input("Enter file name: ")
            size = int(input("Enter file size (MB): "))
            print(fs.touch(name, size))
        elif choice == '3':
            contents = fs.ls()
            print(f"Contents: {contents if contents else 'Empty'}")
        elif choice == '4':
            name = input("Enter name to remove: ")
            print(fs.rm(name))
        elif choice == '5':
            path = input("Enter path: ")
            print(fs.cd(path))
        elif choice == '6':
            break