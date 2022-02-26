#include <iostream>

using namespace std;

int main () 
{

int price = 0;
int age = 0;


cout << "Age (years): ";
cin >> age;



if (age <= 0)
	price = 0;
          else if (age >=8)
                 price = 9;
	            else if (age < 8)
                            price = 6;


         
if (age != -1)

cout << "Price: $" << price <<endl;
else 
 cout << "Invalid age" << endl;


return 0;
}