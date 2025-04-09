#include<bits/stdc++.h>
using namespace std;

signed main(void)
{
    srand(time(0));// 随机数，需要<random>库

    int x = rand()%100;
    int y = rand()%100;

    cout << x << ' ' << y << '\n';

    return 0;
}

