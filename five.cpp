#include <iostream>
#include <iomanip>

using namespace std;

int main ()
{
//declare variables
int totalCals = 0;
int fatGrams = 0;
int fatCals = 0;
double fatPercent = 0.0;

//input items
cout << "Total calories: ";
cin >> totalCals;
cout << "Grams of fat: ";
cin >> fatGrams;


if (totalCals >= 0 && fatGrams >= 0)
{

fatCals = fatGrams * 9;

fatPercent = static_cast<double>(fatCals) / totalCals * 100;

cout << "Fat calories: " << fatCals << endl;
cout << fixed << setprecision(0);
cout << "Fat percentage: " << fatPercent << "%" << endl;

}

else
	cout << "Input Error" << endl;

//endif


return 0;
}





