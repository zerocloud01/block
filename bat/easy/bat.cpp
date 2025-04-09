#include <bits/stdc++.h>
using namespace std;

int main() 
{
    freopen("bat.out", "w", stdout);
    int T = 1e3; // 数据次数，也可以写死循环直到wa。
    for(int i=1;i<=100;++i)
    {
        cout << "test:" << i << '\n';
        system("generater.exe > data.in");
        system("std.exe < data.in > std.out");
        system("solve.exe < data.in > solve.out");
        if(system("fc std.out solve.out > diff.log"))   cout << "WA\n";
    }
}