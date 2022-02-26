#include <iostream>
#include <iomanip>

using namespace std;

int main ()
{

int months = 0;
double avgBill = 0.0;
double bill = 0.0;
double totalBills = 0.0;

cout << "Bill for month 1: ";
cin >> bill;

while (bill >= 0.0)

{
months += 1; // months = months + 1

totalBills += bill; //totalBills = totalBills + bill
cout << totalBills << endl;
cout << "Bill for month" << months + 1 << ": ";
cin >> bill;

}

if (months > 0)

{
avgBill = totalBills / months ;

cout << fixed << setprecision(2);
cout << "Average electric bill for" << months << "months: $" << avgBill << endl;

}
else

cout << "No bill amount entered." << endl; 



return 0;
}