#include <gurobi_c++.h>
#include <iostream>
using namespace std;
// https://docs.gurobi.com/projects/optimizer/en/current/reference/parameters.html

/* Tutorial de compilação:
        g++ -O3 -std=c++17 -Werror -Wall \
        -I/Library/gurobi1203/macos_universal2/include \
        -L/Library/gurobi1203/macos_universal2/lib \
        -lgurobi_c++ -lgurobi120 \
        tutorial.cpp -o tutorial
*/


// maximize	x	+	y	+	2 z	 	 
// subject to	x	+	2 y	+	3 z	<=	4
//  	x	+	y	 	 	>=	1
//  	x, y, z binary

int main() {
    try {
        //criar o env e modelo
        GRBEnv env = GRBEnv(true);    
        env.set("LogFile", "tutorial.log");  
        env.start();

        GRBModel model = GRBModel(env);  

        // definir variaveis
        GRBVar x = model.addVar(0.0, 1.0, 0.0, GRB_BINARY, "x");
        GRBVar y = model.addVar(0.0, 1.0, 0.0, GRB_BINARY, "y");
        GRBVar z = model.addVar(0.0, 1.0, 0.0, GRB_BINARY, "z");

        // restricoes
        model.addConstr(x + 2 * y + 3 * z <= 4, "c0");
        model.addConstr(x + y >= 1, "c1");

        // setar objetivo
        model.setObjective(x + y + 2 * z, GRB_MAXIMIZE);

        // otimizar
        model.optimize();

        //resultados
        cout << x.get(GRB_StringAttr_VarName) << " "
            << x.get(GRB_DoubleAttr_X) << endl;
        cout << y.get(GRB_StringAttr_VarName) << " "
            << y.get(GRB_DoubleAttr_X) << endl;
        cout << z.get(GRB_StringAttr_VarName) << " "
            << z.get(GRB_DoubleAttr_X) << endl;

        cout << "Obj: " << model.get(GRB_DoubleAttr_ObjVal) << endl;

        
    } catch (GRBException e) {
        cerr << "Error code = " << e.getErrorCode() << endl;
        cerr << e.getMessage() << endl;
    } catch (...) {
        cerr << "Unknown exception during optimization" << endl;
    }

    return 0;
}

// int main() {
//     // Create an environment
//     GRBEnv env = GRBEnv(true);

//     // Create a model
//     GRBModel model = GRBModel(env);
//     model.set(GRB_IntParam_Cuts, -1);
//     model.set(GRB_DoubleParam_TimeLimit, 600.0);

//     // Create variables
//     //                      lb , ub          ,coef, tipo         , nome
//     map<string, GRBVar> vars;
//     vars["x"] = model.addVar(0.0, GRB_INFINITY, 0.0, GRB_CONTINUOUS, "x");

//     model.update();

//     // Constraints
//     map<string, GRBConstr> constrs;
//     GRBLinExpr expr = 0;
//     expr += vars["x"];
//     constrs["c0"] = model.addConstr(expr <= 10.0, "c0");

//     model.optimize();

//     // Print the solution
//     double res = vars["x"].get(GRB_DoubleAttr_X);

//     return 0;
// }
