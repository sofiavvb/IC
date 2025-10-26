#include <gurobi_c++.h>
#include <iostream>
#include <vector>
using namespace std;


int main() {
    try {
        //criar o env e modelo
        GRBEnv env = GRBEnv(true);    
        env.set("LogFile", "diet_problem.log");  
        env.start();

        GRBModel model = GRBModel(env);  
        model.set(GRB_StringAttr_ModelName, "diet");

        vector<string> nutrients = { "calories", "protein", "fat", "sodium" };
        vector<string> foods =  { "hamburger", "chicken", "hot dog", "fries", "macaroni", "pizza", "salad", "milk", "ice cream" };};
        vector<double> min_nutrient =  { 1800, 91, 0, 0 };
        vector<double> max_nutrient = { 2200, GRB_INFINITY, 65, 1779 };
        vector<double> cost = { 2.49, 2.89, 1.50, 1.89, 2.09, 1.99, 2.49, 0.89, 1.59 };
        vector<vector<double>> nutrient_amount = {
            { 410, 24, 26, 730 },   // hamburger
            { 420, 43, 10, 1190 },  // chicken
            { 560, 20, 32, 1160 },  // hot dog
            { 380, 4, 19, 270 },    // fries
            { 320, 12, 10, 930 },   // macaroni
            { 320, 15, 12, 820 },   // pizza
            { 320, 31, 12, 1230 },  // salad
            { 170, 8, 5, 125 },     // milk
            { 330, 5, 10, 180 }     // ice cream
        };

        // definir variaveis
        vector<GRBVar> nutrient_vars(nutrients.size()) = model.addVars(min_nutrient, max_nutrient, 0, 0, nutrients);

        vector<GRBVar> food_vars(foods.size());
        food_vars = model.addVars(0, 0, cost, GRB_CONTINUOUS, foods);
        model.update();
        
        model.set(GRB_IntAttr_ModelSense, GRB_MINIMIZE);

        for(int j = 0; j < nutrients.size(); j++) {
            GRBLinExpr expr = 0;
            for(int i = 0; i < foods.size(); i++) {
                expr += nutrient_amount[i][j] * food_vars[i];
            }
            model.addConstr(expr == nutrient_vars[j], nutrients[j]);
        }

        // otimizar
        model.optimize();
        printSolution(model, nutrients.size(), foods.size(), food_vars.data(), nutrient_vars.data());

    } catch (GRBException e) {
        cerr << "Error code = " << e.getErrorCode() << endl;
        cerr << e.getMessage() << endl;
    } catch (...) {
        cerr << "Unknown exception during optimization" << endl;
    
    }
}


void printSolution(GRBModel& model, int nCategories, int nFoods,
                   GRBVar* buy, GRBVar* nutrition)
{
  if (model.get(GRB_IntAttr_Status) == GRB_OPTIMAL)
  {
    cout << "\nCost: " << model.get(GRB_DoubleAttr_ObjVal) << endl;
    cout << "\nBuy:" << endl;
    for (int j = 0; j < nFoods; ++j)
    {
      if (buy[j].get(GRB_DoubleAttr_X) > 0.0001)
      {
        cout << buy[j].get(GRB_StringAttr_VarName) << " " <<
        buy[j].get(GRB_DoubleAttr_X) << endl;
      }
    }
    cout << "\nNutrition:" << endl;
    for (int i = 0; i < nCategories; ++i)
    {
      cout << nutrition[i].get(GRB_StringAttr_VarName) << " " <<
      nutrition[i].get(GRB_DoubleAttr_X) << endl;
    }
  }
  else
  {
    cout << "No solution" << endl;
  }
}
