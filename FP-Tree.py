
import itertools
class node:
    def __init__(self,name="",c=0,p=None):
        self.itemname=name
        self.count=c
        self.parent=p
        self.childs=[]
        self.next=None

def fpgrowth(T,L):
	#Creating a null root node
    tree_root=node()
    ref=[]
    for i in range(len(L)):
        ref.append(None)
    tree_list=[L,ref]
    #sort each transaction and insert it into tree
    for transaction in T:
        ordered_transaction=[]
        for item in L:
            if(item in transaction):
                ordered_transaction.append(item)
        modify_tree(tree_root,ordered_transaction,tree_list)
    tree_list.append(tree_root)
    return tree_list
   
def modify_tree(root,transaction,tree_list):
    currentnode=root
    for item in transaction:
        found=False
        #check if item is already a child of current node 
        for n in currentnode.childs:
            if n.itemname==item:
                #if already there increment its count 
                found=True
                currentnode=n
                currentnode.count=1+currentnode.count
        if found==False:
            #if item is not a child of currentnode the create new node 
            # whose parent is current node
            #add this node to current node's childs list
            n=node(item,1,currentnode)
            currentnode.childs.append(n)
            currentnode=n
            i=tree_list[0].index(item)
            #print("i:",i)
            #print(currentnode.next)
            ##make pointer from last node of item to new node of same item
            if tree_list[1][i]==None:
                tree_list[1][i]=currentnode
                #print(tree_list[1][i].itemname)
            else:
                start=tree_list[1][i]
                while start.next!=None:
                    start=start.next
                start.next=currentnode
            

def printTree(root):
    if root.itemname!="":
	    print("Node Name : "+ root.itemname)
	    print("Count : ",root.count)
	    print("Parent Node Name : "+root.parent.itemname)
	    print("No. of Childs : ",len(root.childs))
	    print("")
	else:
	    print("Node Name : NULL")
	    print("Count : ",root.count)
	    print("No. of Childs : ",len(root.childs))
	    print("")
    for c in root.childs:
        printTree(c)
    
def findsubsets(S):
    itemsets=[]
    for i in range(1,len(S)+1):
        for item in itertools.combinations(S,i):
            itemsets.append(item)
    return itemsets    
def extractitemsets(tree,supcount):
    itemsets={}
    treelist=tree[0:2]
    root=tree[2]
    for i in range(len(treelist[0])-1,-1,-1):
        #print(treelist[0][i])
        suffix=treelist[1][i]
        paths=[]
        while suffix!=None:
            path=[]
            p=suffix.parent
            while p.itemname!="":
                path.append(p.itemname)
                p=p.parent
            path.append(suffix.count)
            #print(path)
            paths.append(path)
            suffix=suffix.next
        #print("paths:",paths)
        for p in range(len(paths)-1,-1,-1):
            path = paths[p]
            l=len(path)
            for itemset in findsubsets(path[0:l-1]):
                itemset_count=path[l-1]
                #print("for itemset:",itemset," ",itemset_count)
                for bpath in range(len(paths)):
                    if paths[bpath]!=path and all(item in paths[bpath] for item in itemset):
                        itemset_count+=paths[bpath][-1]
                if(itemset_count>=supcount):
                    #print(itemset_count)
                    #print(treelist[0][i])
                    itemset=list(itemset)
                    itemset.append(treelist[0][i]) #or make item set a list and use append
                    #print(itemset)
                    itemsets.update({tuple(itemset):itemset_count})
    #print(itemsets)
    return itemsets
        
    
"""prompt user to enter support and confidence values in percent"""
support = int(input("Please enter support value in %: "))

"""Compute candidate 1-itemset"""
C1 = {}
"""total number of transactions contained in the file"""
transactions = 0
D = []
T = []
with open("DataSet5.txt", "r") as f:
    for line in f:
        T = []
        transactions += 1
        for word in line.split():
            T.append(word)
            if word not in C1.keys():
                C1[word] = 1
            else:
                count = C1[word]
                C1[word] = count + 1
        D.append(T)
print("-------------------------TEST DATASET----------------------------")
for trans in D:
	print(trans)
print("-----------------------------------------------------------------")

"""Compute frequent 1-itemset"""
L1 = []
c1=sorted(C1,key=C1.get,reverse=True)
c2={}
for i in c1:
    c2[i]=C1[i]
C1=c2
#print(C1)
for key in C1:
    if (100 * C1[key]/transactions) >= support:
        L1.append(key)
print("----------------------FP-Tree(DFS)-------------------------")
#print(L1)
Tree=fpgrowth(D,L1)
printTree(Tree[2])
print("----------------------FREQUENT ITEMSETS-------------------------")
frequent_itemsets=extractitemsets(Tree,support*len(D)/100)
for itemset in L1:
    frequent_itemsets.update({tuple([itemset]):C1[itemset]}) #######modify from here
print(frequent_itemsets)
#printTree(root)
print("-----------------------------------------------------------------")
print("--------------------------------------------------------")

