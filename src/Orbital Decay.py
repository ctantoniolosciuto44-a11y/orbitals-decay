import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

G, Re= 3.986e14, 6.371e6
B= 2.2 * 0.03/4.0

# B= Cd*A/m Cd=2.2 assumpition for cube satellites 
#altitude[km] density [km/m3]

h_tab = np.array([200, 300, 400, 500, 600, 700]) *1e3
d_tab = np.array ([2.5e-10, 2.4e-11, 2.8e-12, 5.2e-13, 1.1e-13, 3.2e-14])


# d(h)= log-interpolation of h_tab and d_tab
def d(h):
    return np.exp(np.interp(h,h_tab, np.log(d_tab)))

#differential equation as a model for height 
def f(t,y):
    h= y[0]
    return [-d(h)*B*np.sqrt(G*(Re+h))]

#simulation stops at negative values of y-150e3 thus meaning satellite exited the horbit
def reentry (t, y):
    return y[0]-150e3
reentry.terminal = True

#differential equation solution starting at given altitude h0, time span =30 years(0.3*3.15e7) stop event = reentry, solution metod LSODA, max step 1 day 
for h0 in [300, 400, 500, 600]:
    sol= solve_ivp(f, [0,30*3.15e7], [h0*1e3], events=reentry, method= 'LSODA', max_step=86400)
    plt.plot(sol.t/86400, sol.y[0]/1e3, label= f'{h0} km')
plt.xlabel('Days')
plt.ylabel('Altitude [Km]')
plt.legend()
plt.show()

    
