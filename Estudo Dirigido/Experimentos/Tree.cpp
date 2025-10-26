#include <iostream>
#include <vector>

using namespace std;

//para essa formulação, consideramos uma árvore binária perfeita de profundidade d
class Tree{

    private: 
        int depth;
        vector<int> nodes;
        vector<int> leaves;

    public:
        //construtor
        Tree(int d) : depth(d) {
            //nós internos (de branch): [1, ..., 2^depth - 1]
            for (int i = 1; i <= (1 << depth) - 1; i++) {
                nodes.push_back(i);
            }
            //nós folha: [2^depth, ..., 2^(depth + 1) - 1]
            for (int i = (1 << depth); i <= (1 << (depth + 1)) - 1; i++) {
                leaves.push_back(i);
            }
        }

        int getDepth() {
            return depth;
        }

        int leftChild(int node) {
            return 2 * node;
        }

        int rightChild(int node) {
            return 2 * node + 1;
        }

        const vector<int>& getNodes() const {
            return nodes;
        }

        const vector<int>& getLeaves() const {
            return leaves;
        }
};