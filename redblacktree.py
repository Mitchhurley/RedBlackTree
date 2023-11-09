import tkinter as tk
class RedBlackTree:
    """
    Red black tree object that maintains a balanced tree by adhering to certain rules on node placements
    """
    class Node:
        def __init__(self, key, value, color):
            #TODO organize helper methods
            """
            Class that represents the nodes of the red-black tree
            :param key: The key that sorts the
            :param value:
            :param color:
            """
            self.key = key
            self.value = value
            #True is black, False is red
            self.color = color
            self.subtree_size = 1
            #Node relation initialized as None because they haven't been placed yet
            self.left = None
            self.right = None
            self.parent = None

    def __init__(self):
        """
        The central red black tree object that self balances by maintaining black balance and other requirements
        """
        self.root = None
        self.debug = False
        self.total_size = 0
        self.unwinding = False
        self.last_del = None

    def __len__(self):
        return self.total_size

    def put(self, key, value):
        """
        Places a node into it's place in the red black tree and then balances the tree recursively
        :param key: the key for the node to be inserted
        :param value: the value of the node to be inserted
        """
        # Calls the helper method to insert a new key-value pair while maintaining Red-Black Tree properties
        self.root = self.__putRecursive(self.root, key, value)
        self.total_size += 1
        self.__update_subtree_size(self.root)
        self.root.color = True  # Ensure root is black, can't affect any properties negatively

    def __putRecursive(self, node, key, value):
        #no root node case
        if node is None:

            self.unwinding = True
            # Creates a new node to be the root
            return self.Node(key, value, False)

        # Recursive insertion
        #case where key is already
        if key == node.key:
            node.value = value
            #counteract the bump
            self.total_size -= 1
            return node
        if key < node.key:
            node.left = self.__putRecursive(node.left, key, value)
        elif key > node.key:
            node.right = self.__putRecursive(node.right, key, value)
        if self.unwinding:
            self.unwinding = False
            if self.debug: self.display_tree()
        # Check and enforce Red-Black Tree properties after insertion
        if self.__is_red(node.right) and not self.__is_red(node.left):
            node = self.__rotate_left(node)
        if self.__is_red(node.left) and self.__is_red(node.left.left):
            node = self.__rotate_right(node)
        if self.__is_red(node.left) and self.__is_red(node.right):
            self.__flip_colors(node)

        #call the update subtree size method to make it so the subtree size values are correct post rotation
        self.__update_subtree_size(node)

        #returns the updated node
        return node

    def __is_red(self, node):
        # Helper method that checks if a node is red
        if node is None:
            return False
        return not node.color

    def __is_black(self, node):
        # Helper method that checks if a node is black
        if node is None:
            return False
        return node.color

    def __rotate_left(self, node):
        #Left rotation in a Red-Black Tree. Used to balance the tree after an insertion or as part of other tree operations.

        x = node.right
        node.right = x.left
        x.left = node
        x.color = x.left.color
        x.left.color = False
        self.__update_subtree_size(node)
        self.__update_subtree_size(x.left)


        return x

    def __rotate_right(self, node):
        # Left rotation in a Red-Black Tree. Used to balance the tree after an insertion or as part of other tree operations.

        x = node.left
        node.left = x.right
        x.right = node
        x.color = x.right.color
        x.right.color = False
        self.__update_subtree_size(node)
        self.__update_subtree_size(x.right)

        return x

    def __flip_colors(self, node):
        """
        Flips the colors of a "family" of nodes, maintaining black balance
        :param node: The parent node of the "family"
        """
        node.color = not node.color
        node.left.color = not node.left.color
        node.right.color = not node.right.color

    def get(self, key):
        """
        Returns the value corresponding to the given key, or None if the key is not present
        :param key: the key to be searched for
        """
        node = self.root
        while node is not None and (node.right is not None or node.left is not None or self.size == 1):
            #check if we found the right key
            if node.key == key:
                return node.value
            #if not go left or right
            if node.key > key and node.left is not None:
                node = node.left
            elif node.key < key and node.right is not None:
                node = node.right
        if node.key == key: return node.value
        return None
        """
        Removes a key-value pair, returning the deleted value
        Returns None if the key wasn't present
        :param key: the key to be deleted
        :return:
        """

    def delete(self, key):
        self.last_del = None  # Initialize last_del to None
        if self.root is None:
            return None

        self.root.color = False  # Set the root node color to red

        self.root = self.__delete_recursively(self.root, key)

        if self.root is not None:
            self.root.color = True  # Ensure the root is black after deletion
        return self.last_del  # Return the value of the deleted node

    def __delete_recursively(self, node, key):
        if key < node.key:
            if node.left is not None:
                if not self.__is_red(node.left) and not self.__is_red(node.left.left):
                    node = self.__move_red_left(node)
                node.left = self.__delete_recursively(node.left, key)
        else:
            if self.__is_red(node.left):
                node = self.__rotate_right(node)
            if key == node.key and node.right is None:
                self.last_del = node.value
                self.total_size -= 1
                return None  # This node will be deleted
            if node.right is not None:
                if not self.__is_red(node.right) and not self.__is_red(node.right.left):
                    node = self.__move_red_right(node)
                if key == node.key:
                    min_node = self.__min(node.right)
                    # Capture node data in temp variables
                    deleted_node = RedBlackTree.Node(node.key, node.value, node.color)
                    # Replace node values with min_node values
                    node.value, node.key, node.color = min_node.value, min_node.key, min_node.color
                    # Delete the minimum node recursively
                    node.right = self.__delete_min(node.right)
                    self.last_del = deleted_node.value
                else:
                    node.right = self.__delete_recursively(node.right, key)
        # Return the node after calling the balancing method
        node = self.__fix_up(node)
        self.__update_subtree_size(node)  # Update the size of the subtree

        return node

    def __delete_min(self, node):
        # Delete the minimal key in the subtree rooted at the given node
        if node.left is None:
            return None  # This node will be deleted
        if not self.__is_red(node.left) and not self.__is_red(node.left.left):
            node = self.__move_red_left(node)
        node.left = self.__delete_min(node.left)
        return self.__fix_up(node)

    def __move_red_left(self, node):
        # Move a red node from the left to the right
        self.__flip_colors(node)
        if self.__is_red(node.right.left):
            node.right = self.__rotate_right(node.right)
            node = self.__rotate_left(node)
            self.__flip_colors(node)
        return node

    def __move_red_right(self, node):
        # Move a red node from the right to the left
        self.__flip_colors(node)
        if self.__is_red(node.left.left):
            node = self.__rotate_right(node)
            self.__flip_colors(node)
        return node

    def __fix_up(self, node):
        # Post deletion method to fix red black tree properties -- no Idea if this works right
        if self.__is_red(node.left) and self.__is_red(node.right):
            self.__flip_colors(node)
        if self.__is_red(node.right):
            node = self.__rotate_left(node)
        if self.__is_red(node.left) and self.__is_red(node.left.left):
            node = self.__rotate_right(node)
        #Do a second check for a color flip
        if self.__is_red(node.left) and self.__is_red(node.right):
            self.__flip_colors(node)

        self.__update_subtree_size(node)
        return node

    def __min(self, node):
        # Helper method to find the minimal key for deletion
        while node.left is not None:
            node = node.left
        return node

    def __update_subtree_size(self, node):
        if node is not None:
            node.subtree_size = 1 + self.__get_subtree_size(node.left) + self.__get_subtree_size(node.right)

    def __get_subtree_size(self, node):
        if node is None:
            return 0
        return node.subtree_size


    def contains_key(self, key):
        """
        Returns true if the key is present
        :param key:
        :return:
        """
        if self.root is not None:
            curr = self.root
            if curr.key == key: return True
        else:
            # If the root is none, then the tree is empty so we return false
            return False
        while (curr.left is not None or curr.right is not None):
            if curr.key > key:
                if curr.left is not None:
                    curr = curr.left
                #If the key larger but there is no node, we know it isnt in the tree
                else: return False
            elif curr.key < key:
                if curr.right is not None:
                    curr = curr.right
                # If the key is smaller but there is no node, we know it isnt in the tree
                else: return False
            if curr.key == key:
                return True
        return False

    def contains_value(self, value):
        """
        Returns true if the value is present
        :param value: The value to search for
        """
        # Returns true if the value is present
        if self.root is not None:
            curr = self.root
        else:
            # If the root is none, then the tree is (hopefully) empty so we return none
            return False
        if curr.value == value:
            return True
        return self.__recursive_value_search(curr.left, value) or self.__recursive_value_search(curr.right, value)

    def __recursive_value_search(self,node, value):
        #helper method for the value search
        if node is None:
            return False
        if node.value == value:
            return True
        else:
            return self.__recursive_value_search(node.left, value) or self.__recursive_value_search(node.right, value)



    def is_empty(self):
        """
        Returns true if the tree is empty
        """
        return self.total_size == 0

    def size(self):
        """
        Returns the number of key-value pairs in the tree
        """
        return self.total_size

    def reverse_lookup(self, value):
        """
        Finds the first key that maps to the value within the red black tree,
        Returns None if there is none
        """
        # Finds a key that maps to the given value
        #
        return self.__reverseLookupHelper(self.root, value)

    def __reverseLookupHelper(self, node, value):
        if node is None:
            return None

        if node.value == value:
            return node.key

        # Check left and right subtrees
        left_result = self.__reverseLookupHelper(node.left, value)
        if left_result:
            return left_result

        right_result = self.__reverseLookupHelper(node.right, value)
        if right_result:
            return right_result

        return None

    def find_first_key(self):
        """
        Returns the key that is less than all the others
        """
        #Confirm the root is not None, so we can assign curr to it safely
        if self.root is not None: curr = self.root

        else:
            # If the root is none, then the tree is (hopefully) empty so we return none
            return None
        while (curr.left is not None):
            curr = curr.left
        return curr.key

    def find_last_key(self):
        """
        Returns the key that is less than all the others
        """
        # Confirm the root is not None, so we can assign curr to it safely
        if self.root is not None:
            curr = self.root
        else:
            # If the root is none, then the tree is empty so we return none
            return None
        while (curr.right is not None):
            curr = curr.right
        return curr.key

    def get_root_key(self):
        """
        Returns the key contained in the root
        """
        # Confirm the root is not None, so we can access it safely
        if self.root is not None:
            return self.root.key
        else:
            # If the root is none, then the tree is (hopefully) empty so we return none
            return None

    def find_predecessor(self, key):
        #
        """
        Returns the predecessor of the given key
        Returns None if the key is not present or has no predecessor
        :param key:
        """
        if self.root is not None:
            curr = self.root
        else:
            # If the root is none, then the tree is empty so we return false
            return None
        #Keep track of last time we went right
        last = self.root
        while (curr.left is not None or curr.right is not None):

            if curr.key > key:
                if curr.left is not None:
                    curr = curr.left
                #If the key larger but there is no node, we know it isnt in the tree
                else: return None
            elif curr.key < key:
                if curr.right is not None:
                    #update last because we went right.
                    last = curr
                    curr = curr.right
                # If the key is smaller but there is no node, we know it isnt in the tree
                else: return None
            if curr.key == key:
                #once we find the key, we check to see if we can find the predecessor in the left subtree
                if curr.left is not None:
                    curr = curr.left
                    while curr.right is not None:
                        curr = curr.right
                    return curr
                #if not, then we have to grab the parent
                return last
        #Traverse tree to find key
        return None

    def find_successor(self, key):
        """
        Returns the successor of the given key or returns None if the key is not present or has no successor
        :param key: the key to find the successor of
        """
        if self.root is not None:
            curr = self.root
        else:
            # If the root is none, then the tree is empty so we return false
            return None
        #Keep track of last time we went left
        last = self.root
        while (curr.left is not None or curr.right is not None):
            if curr.key > key:
                if curr.left is not None:
                    last = curr
                    curr = curr.left
                #If the key larger but there is no node, we know it isnt in the tree
                else: return None
            elif curr.key < key:
                if curr.right is not None:
                    curr = curr.right
                # If the key is smaller but there is no node, we know it isnt in the tree
                else: return None
            if curr.key == key:
                #once we find the key, we check to see if we can find the predecessor in the left subtree
                if curr.right is not None:
                    curr = curr.right
                    while curr.left is not None:
                        curr = curr.left
                    return curr
                #if not, then we have to grab the parent
                return last
        #Traverse tree to find key
        return None


    def find_rank(self, key):
        """
        Returns the rank of the given key, or returns -1 if the key is not present
        :param key: the key to find the rank of
        """
        if self.root is not None:
            curr = self.root
        else:
            # If the root is none, then the tree is empty so we return false
            return -1
        total = 0
        while (curr.left is not None or curr.right is not None):
            if curr.key > key:
                if curr.left is not None:
                    curr = curr.left
                #If the key larger but there is no node, we know it isnt in the tree
                else: return -1
            elif curr.key < key:
                if curr.right is not None:
                    total += curr.left.subtree_size + 1
                    curr = curr.right
                # If the key is smaller but there is no node, we know it isnt in the tree
                else: return -1
            if curr.key == key:
                if curr.left is None:
                    return total
                return total + curr.left.subtree_size
        return -1

    def select(self, rank):
        """
        Returns the key with the given rank
        Returns None when the rank is invalid
        :param rank: The rank of the object to be found
        """
        if self.root is not None:
            curr = self.root
        else:
            return None

        # Avoiding searching for a rank out of bounds
        if rank >= self.size() or rank < 0:
            return None

        while True:
            left_size = 0 if curr.left is None else curr.left.subtree_size
            if rank < left_size:
                curr = curr.left
            elif rank == left_size:
                return curr.key
            elif curr.right is not None:
                # Go right and adjust the rank to look in the right subtree
                rank -= (left_size + 1)
                curr = curr.right
        return None

    def count_red_nodes(self):
        """
        Returns the number of red nodes in the tree
        """
        #
        if self.root is None:
            return 0
        return self.__recursive_count_red_nodes(self.root)

    def __recursive_count_red_nodes(self, node):
        if node is None:
            return 0
        count = self.__recursive_count_red_nodes(node.left) + self.__recursive_count_red_nodes(node.right)
        if not node.color:
            count += 1
        return count

    def calc_height(self):
        """
        Returns the height of the tree from the root through the longest chain
        """


        if self.root is None:
            return 0
        else:
            # Subtract 1 as the root node is at height 1
            return self.__recursive_calc_height(self.root) - 1

    def __recursive_calc_height(self, node):
        if node is None:
            # we've reached a leaf/end
            return 0

        # Calculate the height of the left and right subtrees
        left_height = self.__recursive_calc_height(node.left)
        right_height = self.__recursive_calc_height(node.right)

        # Return the maximum height plus one for the current node
        return max(left_height, right_height) + 1


    def calc_black_height(self):
        """
        Returns the black height of the tree, or 0 for an empty tree
        :return:
        """
        curr = self.root
        total = 0
        while curr is not None:
            #if the current node is black, increment the counter by 1
            if self.__is_black(curr):
                total +=1
            if curr.left is not None:
                curr = curr.left
            elif curr.right is not None:
                curr = curr.right
            else: return total

    def calc_average_depth(self):
        """
        Returns the average distance of all nodes to the root
        """
        if self.root is not None:
            return self.__recursive_average_depth(self.root, 0) / self.size()
        else:
            return float('nan')

    def __recursive_average_depth(self, node, depth):
        if node is None:
            return 0

        # If the node is a leaf node, return its depth
        if node.left is None and node.right is None:
            return depth

        # Calculate the sum of depths for both left and right subtrees
        left_depth = self.__recursive_average_depth(node.left, depth + 1)
        right_depth = self.__recursive_average_depth(node.right, depth + 1)

        return left_depth + right_depth

    def display_tree(self):
        #Method I made for looking at small (>100) trees, definately could modify to work for bigger but I'm lazy

        def __plot_tree(node, x, y, dx):
            if node is not None:
                radius = 10
                color = "black" if node.color else "red"
                canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)
                canvas.create_text(x, y, text=str(node.key))
                canvas.create_text(x + 30, y, text=str(node.value))

                if node.left:
                    x_left = x - dx
                    y_left = y + 25
                    canvas.create_line(x, y + radius, x_left, y_left - radius)
                    __plot_tree(node.left, x_left, y_left, dx / 2)

                if node.right:
                    x_right = x + dx
                    y_right = y + 25
                    canvas.create_line(x, y + radius, x_right, y_right - radius)
                    __plot_tree(node.right, x_right, y_right, dx / 2)

        if self.root is not None:
            root_window = tk.Tk()
            root_window.title("Red-Black Tree Visualization")



            tree_width = self.__get_tree_width(self.root) * 20  # Calculate tree width
            x_root = tree_width // 2  # Center x coordinate
            y_root = 50  # Y coordinate

            canvas = tk.Canvas(root_window, width=tree_width * 200, height=600)
            canvas.pack()

            __plot_tree(self.root, x_root, y_root, x_root // 2)  # Use x_root as starting x-coordinate

            root_window.mainloop()

    def __get_tree_width(self, node):
        if node is None:
            return 0
        return 1 + self.__get_tree_width(node.left) + self.__get_tree_width(node.right)

