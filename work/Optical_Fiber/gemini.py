import numpy as np
from scipy.special import jv, kv, jn_zeros
from scipy.optimize import brentq
import matplotlib.pyplot as plt
from matplotlib.pyplot import *

# 特征方程
def func(U, V, m):
    # LP_mn: U J_{m-1}(U) K_m(W) + W K_{m-1}(W) J_m(U) = 0 课本P12 1-44b

    # 避免 U=0, U=V 导致 W=V 或 W=0 的问题
    if(U <= 1e-9 or U >= V - 1e-9): return np.inf # 返回较大的值，get会避开这个无效区域
    W = np.sqrt(V**2 - U**2)
    # 避免 W=0
    if(W <= 1e-9): return np.inf

    val_Jm = jv(m, U)           # J_m(U)
    val_Jm_1 = jv(m - 1, U)     # J_{m-1}(U)
    val_Km = kv(m, W)           # K_m(W)
    val_Km_1 = kv(m - 1, W)     # K_{m-1}(W)

    return U * val_Jm_1 * val_Km + W * val_Km_1 * val_Jm


# 寻根函数
def get(V_val, m, num_roots_to_find):
    
    roots = [] # 存找到的根
    func_to_solve = lambda U_param: func(U_param, V_val, m)

    u_scan_points = np.linspace(1e-6, V_val - 1e-6, 500) # 采样
    f_values = np.array([func_to_solve(u) for u in u_scan_points])

    for i in range(len(u_scan_points) - 1):
        if(np.sign(f_values[i]) != np.sign(f_values[i+1])):
            u_low, u_high = u_scan_points[i], u_scan_points[i+1]
            try:
                root = brentq(func_to_solve, u_low, u_high)
                if root not in roots:
                     roots.append(root)
            except ValueError:
                pass # brentq 找不到根，或 f(a)f(b)>0
    
    roots.sort()
    return roots[:num_roots_to_find]


# 参数
V_min = 0.1
V_max = 15
num_V_points = 200
V_arr = np.linspace(V_min, V_max, num_V_points)

modes_to_plot_detailed = [
    (0, [1, 2]),  # LP01, LP02
    (1, [1, 2]),  # LP11, LP12
    (2, [1]),     # LP21
    (3, [1]),     # LP31
    (4, [1]),     # LP41
]

cutoff_approximations = {
    "LP01": 0.0,
    "LP02": jn_zeros(0, 1)[0],
    "LP11": jn_zeros(0, 1)[0], 
    "LP12": jn_zeros(0, 2)[1], 
    "LP21": jn_zeros(1, 1)[0], 
    "LP31": jn_zeros(2, 1)[0], 
    "LP41": jn_zeros(3, 1)[0], 
}


plt.figure(figsize=(10, 7))
plt.xlabel(r'$V$')
plt.ylabel(r'$b = \frac{\beta - n_2 k_0}{n_1 k_0 \Delta}$')
plt.grid(True)
plt.ylim(0, 1.05)
plt.xlim(V_min, V_max)

# 绘图
for m_azimuthal, radial_indices in modes_to_plot_detailed:
    for n_radial_target in radial_indices:
        b_values = []
        V_plot_points = [] 

        mode_str = rf'$LP_{{{m_azimuthal}{n_radial_target}}}$'# 渲染为 LaTex
        vc_approx = cutoff_approximations.get(mode_str, 0)

        for V_val in V_arr:
            if V_val < vc_approx and not np.isclose(vc_approx, 0): 
                b_values.append(0) 
                V_plot_points.append(V_val)
                continue

            current_U_roots = get(V_val, m_azimuthal, n_radial_target + 2) 

            if(len(current_U_roots) >= n_radial_target):
                U_sol = current_U_roots[n_radial_target - 1]
                if(1e-7 < U_sol < V_val):
                    W_sq = V_val**2 - U_sol**2
                    if(W_sq >= -1e-9):
                        W_sq = max(0, W_sq)
                        b = W_sq / V_val**2
                        if(-0.001 <= b <= 1.001):
                            b_values.append(max(0, min(1, b)))
                            V_plot_points.append(V_val)
                            continue
            b_values.append(0 if V_val < vc_approx and not np.isclose(vc_approx, 0) else np.nan)
            V_plot_points.append(V_val)


        valid_indices = ~np.isnan(b_values)
        if np.any(valid_indices):
            current_v_plot = np.array(V_plot_points)[valid_indices]
            current_b_plot = np.array(b_values)[valid_indices]
            if len(current_v_plot) > 0:
                 plt.plot(current_v_plot, current_b_plot, label=mode_str)

plt.legend()
plt.show()