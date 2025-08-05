// // // Online C++ compiler to run C++ program online
// // #include <iostream>
// // #include<math.h>
// // using namespace std;

// // int main(){
// //     double x1,x2,x0,f1,f2,f0;
// //     cout<<"Enter the initial guess:";
// //     cin>>x1;
// //     cout<<"Enter the second guess:";
// //     cin>>x2;
// //     f1=x1*log10(x1)-1.2;
// //     f2=x2*log10(x2)-1.2;
// //     f0=x0*log10(x0)-1.2;
// //       x0=x1-(f1*(x2-x1)/(f2-f1));
// //     cout<<x0<<"\n";
    
// //     if (f0==0)
// //     {
// //         cout<<"the root is"<<x0;
// //     }
// //     else{
// //         while(abs(f0)>0.0001){
// //             if(f0*f1<0){
                
// //                 f2=f0;
// //                 x2=x0;
// //                 x0=(x1+x2)/2;
// //                 f1=x1*log10(x1)-1.2;
// //                 f2=x2*log10(x2)-1.2;
// //                 f0=x0*log10(x0)-1.2;
// //             }
// //             else{
                
// //                 f1=f0;
// //                 x1=x0;
// //                 x0=(x1+x2)/2;
// //                 f1=x1*log10(x1)-1.2;
// //                 f2=x2*log10(x2)-1.2;
// //                 f0=x0*log10(x0)-1.2;
                
// //             }
// //         }
// //         cout<<"the root is"<<x0;
// //     }
// // }

// #include <iostream>
// #include <iomanip>
// #include <cstdlib>
// using namespace std;

// const int SIZE = 10;

// int main() {
//     float a[SIZE][SIZE + 1], x[SIZE], ratio;
//     int n;

//     // Input
//     cout << "Enter number of unknowns: ";
//     cin >> n;

//     cout << "Enter the augmented matrix (coefficients and constants):\n";
//     for (int row = 0; row < n; row++) {
//         for (int col = 0; col <= n; col++) {
//             cout << "a[" << row << "][" << col << "] = ";
//             cin >> a[row][col];
//         }
//     }

//     // Forward Elimination
//     for (int pivot = 0; pivot < n - 1; pivot++) {
//         if (a[pivot][pivot] == 0.0) {
//             cout << "Mathematical Error: Division by zero\n";
//             exit(0);
//         }

//         for (int row = pivot + 1; row < n; row++) {
//             ratio = a[row][pivot] / a[pivot][pivot];

//             for (int col = 0; col <= n; col++) {
//                 a[row][col] -= ratio * a[pivot][col];
//             }
//         }
//     }

//     // Back Substitution
//     x[n - 1] = a[n - 1][n] / a[n - 1][n - 1];

//     for (int i = n - 2; i >= 0; i--) {
//         x[i] = a[i][n];  // start with constant

//         for (int j = i + 1; j < n; j++) {
//             x[i] -= a[i][j] * x[j];
//         }

//         x[i] /= a[i][i];  // divide by coefficient
//     }

//     // Output solution
//     cout << "\nSolution:\n";
//     for (int i = 0; i < n; i++) {
//         cout << "x" << i + 1 << " = " << fixed << setprecision(3) << x[i] << endl;
//     }

//     return 0;
// }
#include <iostream>
#include <iomanip>
#include <cstdlib>
using namespace std;

const int SIZE = 10;

int main() {
    float a[SIZE][SIZE + 1];
    int n;

    // Input
    cout << "Enter number of unknowns: ";
    cin >> n;

    cout << "Enter the augmented matrix (coefficients and constants):\n";
    for (int row = 0; row < n; row++) {
        for (int col = 0; col <= n; col++) {
            cout << "a[" << row << "][" << col << "] = ";
            cin >> a[row][col];
        }
    }

    // Gauss-Jordan Elimination
    for (int pivot = 0; pivot < n; pivot++) {
        if (a[pivot][pivot] == 0.0) {
            cout << "Mathematical Error: Division by zero\n";
            exit(0);
        }

        // Make pivot 1
        float pivotVal = a[pivot][pivot];
        for (int col = 0; col <= n; col++) {
            a[pivot][col] /= pivotVal;
        }

        // Make all other elements in pivot column 0
        for (int row = 0; row < n; row++) {
            if (row != pivot) {
                float ratio = a[row][pivot];
                for (int col = 0; col <= n; col++) {
                    a[row][col] -= ratio * a[pivot][col];
                }
            }
        }
    }

    // Output solution
    cout << "\nSolution:\n";
    for (int i = 0; i < n; i++) {
        cout << "x" << i + 1 << " = " << fixed << setprecision(3) << a[i][n] << endl;
    }

    return 0;
}
