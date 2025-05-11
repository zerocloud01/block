import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jv, kv
from scipy.optimize import brentq
import matplotlib.ticker as mticker
from matplotlib.pyplot import *

def func(l, b, V):
    U_val = V * np.sqrt(1 - b)
    W_val = V * np.sqrt(b)
    # 处理贝塞尔函数数值稳定性
    if U_val < 1e-12:  # 避免 U=0
        return np.inf
    
    # 主方程
    L = U_val * jv(l-1, U_val) / jv(l, U_val)
    R = -W_val * kv(l-1, W_val) / kv(l, W_val)
    return L - R

# 寻根
def get(l, V, num_points=300, tol=1e-6):
    bs = np.linspace(tol, 1 - tol, num_points)
    roots = []
    f_vals = [func(l, b, V) for b in bs]
    
    for i in range(len(bs)-1):
        if np.isnan(f_vals[i]) or np.isnan(f_vals[i+1]):
            continue
        if f_vals[i] * f_vals[i+1] < 0:
            try:
                root = brentq(lambda b: func(l, b, V),
                              bs[i], bs[i+1], xtol=1e-8)
                roots.append(root)
            except:
                continue
    
    # 降序排列，否则乱码
    roots = np.sort(roots)[::-1]
    return roots

# 定义 LP 模式 (l, p)
modes = {r'$LP_{01}$': (0, 1),r'$LP_{02}$': (0, 2),r'$LP_{11}$': (1, 1),r'$LP_{12}$': (1, 2),r'$LP_{21}$': (2, 1),r'$LP_{31}$': (3, 1),r'$LP_{41}$': (4, 1),}

# V 范围
V_vals = np.linspace(0.1, 12, 500)
b_curves = {mode: [] for mode in modes}

# 计算曲线
for mode, (l, p) in modes.items():
    if(p == 2):  l += 1
    print(f"计算模式 {mode}...")
    b_vals = []
    for V in V_vals:
        roots = get(l, V)
        if len(roots) >= p:
            b_vals.append(roots[p-1])
        else:
            b_vals.append(np.nan)
    b_curves[mode] = np.array(b_vals)

# 画图
figure(figsize=(12, 8), dpi=100)
colors = {r'$LP_{01}$':'red',r'$LP_{02}$':'orange',r'$LP_{11}$':'yellow',r'$LP_{12}$':'green',r'$LP_{21}$':'cyan',r'$LP_{31}$':'blue',r'$LP_{41}$':'purple'}

for mode in modes:
    plot(V_vals, b_curves[mode], 
             label=mode, color=colors[mode], linewidth=2)

xlabel(r'$V$', fontsize=10)
ylabel(r'$b = \frac{\beta - n_2 k_0}{n_1 k_0 \Delta}$', fontsize=10)
legend(fontsize=10, loc='upper left')
grid(True, linestyle='--', alpha=0.3)
xlim(0, 12)
ylim(0.05, 1.05) # 防止y零点出现
tight_layout()
show()