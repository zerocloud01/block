#include<bits/stdc++.h>
using namespace std;

// 随机数种子
random_device rd;
mt19937 cri(rd()*time(0));

int ri(int l,int r)
{
    int res = (cri() + cri() + cri())/3;
    return (res%(r-l+1)+l);
}

signed main(void)
{
    // std与解答的名称
    string std = "std";
    string sol = "solve";

    // 编译
    cout << "Compiling..." << endl;
    string std_com = "g++ " + std + ".cpp -o " + std;
    string sol_com = "g++ " + sol + ".cpp -o " + sol;
    system(std_com.c_str());
    system(sol_com.c_str());

    // 数据生成
    cout << "Creating data..." << endl;
    ofstream out;
    out.open("data.in");
    // code begin
    int T = 1;
    while(T --)
    {
        int x = ri(1,100), y = ri(1,100);
        out << x << ' ' << y << '\n';
    }
    // code end
    out.close();

    // 运行
    cout << "Running..." << endl;
    string std_out = std + ".out";
    string sol_out = sol + ".out";
    string sys_std_out = std + ".exe" + " < data.in > " + std_out;
    string sys_sol_out = sol + ".exe" + " < data.in > " + sol_out;
    system(sys_std_out.c_str());
    system(sys_sol_out.c_str());

    // 对拍
    cout << "batting...\n" << endl;
    ifstream std_in, sol_in;
    ofstream bat;
    std_in.open(std_out);
    sol_in.open(sol_out);
    bat.open("bat.txt");
    int t = 0;
    string d1,d2;
    while(getline(std_in,d1) && getline(sol_in,d2))
    {
        if(d1 != d2)
        {
            cout << "test-" << ++ t << '\n';
            bat << "test-" << t << "\n";
            bat << d1 << '\n' << d2 << '\n';
        }
    }
    std_in.close();
    sol_in.close();
    bat.close();
    return 0;
}