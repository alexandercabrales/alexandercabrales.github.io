#include <iostream>

using namespace std;

int main ()
{
   const double COMM_RATE = 0.1;
   double sales = 0.0;
   double commission= 0.0;
  
 
   cout << "Enter sales amount: \n";
   cin >> sales;
   commission = sales * COMM_RATE;
   
   cout << "Commission: $" << commission << endl; 
return 0;
}