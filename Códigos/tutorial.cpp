#include <gurobi_c++.h>
// https://docs.gurobi.com/projects/optimizer/en/current/reference/parameters.html
/* Tem o tutorial de instalar
dib_model:
        g++ -O3 -std=c++17 -Werror -Wall \
        -I/Library/gurobi1103/macos_universal2/include \
        -L/Library/gurobi1103/macos_universal2/lib \
        -lgurobi_c++ -lgurobi110 \
        main.cpp -o main
*/

int main() {
    // Create an environment
    GRBEnv env = GRBEnv(true);

    // Create a model
    GRBModel model = GRBModel(env);
    model.set(GRB_IntParam_Cuts, -1);
    model.set(GRB_DoubleParam_TimeLimit, 600.0);

    // Create variables
    //                      lb , ub          ,coef, tipo         , nome
    map<string, GRBVar> vars;
    vars["x"] = model.addVar(0.0, GRB_INFINITY, 0.0, GRB_CONTINUOUS, "x");

    model.update();

    // Constraints
    map<string, GRBConstr> constrs;
    GRBLinExpr expr = 0;
    expr += vars["x"];
    constrs["c0"] = model.addConstr(expr <= 10.0, "c0");

    model.optimize();

    // Print the solution
    double res = vars["x"].get(GRB_DoubleAttr_X);

    return 0;
}
