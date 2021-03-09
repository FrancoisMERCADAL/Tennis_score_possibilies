class Node:
    def __init__(self, score, depth, winner_won_sets_nb, sets_possibilities_normal_match, sets_possibilities_grand_slam, parent_node):
        self.depth = depth
        self.score = score
        self.winner_won_sets_nb = winner_won_sets_nb
        if depth == 5:
            self.nb_children = 0
        else:
            if depth == 4:
                self.nb_children = len(sets_possibilities_grand_slam)
            else:
                self.nb_children = len(sets_possibilities_normal_match)
        self.children_nodes = []
        self.parent_node = parent_node
        return
    
    def Is_divisible(self):
        divisible = True
        if self.depth == 5 or self.winner_won_sets_nb >= 3:
            divisible = False
        return divisible
    
    def Is_leaf(self):
        is_leaf = False
        if self.children_nodes == []:
            is_leaf = True
        return is_leaf
    
    def To_String(self):
        score = "Score: " + self.score
        depth = "\nDepth: " + str(self.depth)
        winner_won_sets_nb = "\nWinner won sets nb: " + str(self.winner_won_sets_nb)
        nb_children = "\nNb children: " + str(self.nb_children)
        print(score + depth + winner_won_sets_nb + nb_children)
        for i in range(self.nb_children):
            try:
                print("Child " + str(i+1) + ": " + str(self.children_nodes[i].depth))
            except:
                continue
    
    def To_String_Tree_View(self):
        offset = "          " * self.depth
        string = offset + "Score: " + str(self.score) + "\n" + offset + "Depth: " + str(self.depth) + "\n" + offset + "Winner won sets nb: " + str(self.winner_won_sets_nb) + "\n" + offset + "Nb children: " + str(self.nb_children) + "\n"
        return string   
    
def make_tree(node, sets_possibilities_normal_match, sets_possibilities_grand_slam):
    divisible = node.Is_divisible()
    if divisible == True:
        special_case = False
        if node.depth == 2 and node.winner_won_sets_nb == 0:
            sets_possibilities_normal_match = sets_possibilities_normal_match[0:int(len(sets_possibilities_normal_match)/2)]
            node.nb_children = int(node.nb_children/2)
            special_case = True
        if node.depth == 3 and node.winner_won_sets_nb == 1 and node.parent_node.winner_won_sets_nb == 0:
            special_case = True
        else:
            if node.depth == 3 and node.winner_won_sets_nb == 1:
                sets_possibilities_normal_match = sets_possibilities_normal_match[0:int(len(sets_possibilities_normal_match)/2)]
                node.nb_children = int(node.nb_children/2)
                special_case = True
        if node.depth == 4 and node.winner_won_sets_nb == 2:
            node.nb_children = len(sets_possibilities_grand_slam)
        for i in range(node.nb_children):
            if node.depth == 4:
                node.children_nodes.append(Node(sets_possibilities_grand_slam[i], node.depth+1,
                                                node.winner_won_sets_nb+1, sets_possibilities_normal_match,
                                                sets_possibilities_grand_slam, node))
            else:
                if special_case == True:
                    node.children_nodes.append(Node(sets_possibilities_normal_match[i], node.depth+1,
                                                    node.winner_won_sets_nb+1, sets_possibilities_normal_match,
                                                    sets_possibilities_normal_match, node))
                else:
                    if i < node.nb_children/2:
                        node.children_nodes.append(Node(sets_possibilities_normal_match[i], node.depth+1,
                                                        node.winner_won_sets_nb+1, sets_possibilities_normal_match,
                                                        sets_possibilities_normal_match, node))
                    else:
                        node.children_nodes.append(Node(sets_possibilities_normal_match[i], node.depth+1,
                                                        node.winner_won_sets_nb, sets_possibilities_normal_match,
                                                        sets_possibilities_grand_slam, node))
            make_tree(node.children_nodes[i], sets_possibilities_normal_match, sets_possibilities_grand_slam)
            
def Tree_to_file(node, file):
    file.write(node.To_String_Tree_View())
    if node.Is_leaf() == False:
        for i in range(node.nb_children):
            Tree_to_file(node.children_nodes[i], file)
            
def Write_file(file_name, tree):
    file = open(file_name,"w")
    Tree_to_file(root, file)
    file.close()

def Get_matches_score_combinations(root, winner_won_sets_nb, max_depth, array):
    if root.depth < max_depth and root.winner_won_sets_nb != winner_won_sets_nb:
        for i in range(len(root.children_nodes)):
            Get_matches_score_combinations(root.children_nodes[i], winner_won_sets_nb, max_depth, array)
    else:
        if root.depth <= max_depth and root.winner_won_sets_nb == winner_won_sets_nb:
            string = ""
            while(root.parent_node != None):
                string += root.score + "-"
                root = root.parent_node
            string = string[:-1]
            tab = string.split('-')[::-1]
            string = ""
            for score in tab:
                string += score + '-'
            array.append(string[:-1])

file_name = "Tennis_Score_Tree.txt"
sets_possibilities_normal_match = ["6/0", "6/1", "6/2", "6/3", "6/4", "7/5", "7/6", "0/6", "1/6", "2/6", "3/6", "4/6", "5/7", "6/7"]
sets_possibilities_grand_slam = ["6/0", "6/1", "6/2", "6/3", "6/4", "7/5", "8/6", "9/7", "10/8", "11/9", "12/10", "13/11", "14/12", "15/13", "16/14", "17/15", "18/16", "19/17", "20/18"]
root = Node("0", 0, 0, sets_possibilities_normal_match, sets_possibilities_grand_slam, None)
make_tree(root, sets_possibilities_normal_match, sets_possibilities_grand_slam)
Write_file(file_name, root)

## Normal matches
array = []
Get_matches_score_combinations(root, 2, 3, array)

## Grand Slam Matches
array2 = []
Get_matches_score_combinations(root, 3, 5, array2)

## Unify the 2 arrays and make a file
final_array = array + array2
final_file_name = "Tennis_Scores_Combinations.txt"
file = open(final_file_name, 'w')
for score in final_array:
    file.write(score + "\n")
file.close()