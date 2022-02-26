#include <iostream>
using namespace std;

int main ()
{

int productId = 0;
double price = 0.0;

cout << "Product ID (1, 2, 5, 7, 9, or 11): ";
cin >> productId;

switch (productId)
{
   case 1:
	price = 50.55;
	break;
   case 2:
   case 9: 
	price = 12.35;
	break;
   case 5:
   case 7: 
   case 11:
	price = 11.46;
	break;
   default:
	price = -1;
}

if (price == -1)
   cout << "Invalid product ID" << endl;
else
   cout << "Price: $" << price << endl;
return 0;
}