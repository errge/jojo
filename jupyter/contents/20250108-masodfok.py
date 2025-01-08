# %% [markdown]
# # Másodfokú függvények és egyenletek
#
# ## Bevezető
#
# Másodfokú polinómoknak (quadratic polynomial) nevezik az olyan kifejezéseket, aminek alakja $3x^2 - 7x - 6$ (ahol természetesen a 3, a -7 és a -6 számok helyett más számok is állhatnak, negatívak és törtek is mind a három helyen).
#
# Lássuk, hogy ezek a kifejezések (és a belőlük képzett függvények, egyenletek), hogyan viselkednek, hogyan kell őket koordináta rendszerben ábrázolni, illetve a zérushelyeiket megkeresni.
#
# Emlékeztető: elsőfokú (linear equation), azaz $4x + 13 = 0$ alakú kifejezéseknél a helyzet viszonylag egyszerű volt, a zérushely egyszerű egyenletmegoldással (13-at kivonunk, majd osztunk 4-gyel) megtalálható, az ábrázolás során pedig mindig egy egyenest kapunk (jelen esetben 4 meredekségű és 13-mal felfele eltolt az y tengelyen).
#
# ## Általános alak (angolul: quadratic form vagy standard form)
#
# A másodfokú kifejezés általános alakjának azt hívják amit korábban is láttunk: $f(x) = 3x^2 - 7x - 6$.
#
# Ez az alak remekül használható értéktáblázat (value table) készítéséhez, csak be kell helyettesítenünk a kívánt számokat és készen vagyunk.

# %%
import sympy
from IPython.display import display, HTML
from tabulate import tabulate

x = sympy.symbols("x")
f = 3*x**2 - 7*x - 6

inputs = list(range(-4, 5))
outputs = list(map(lambda i: float(f.subs(x, i)), inputs))

display(tabulate([['Output'] + outputs], headers=['Input'] + inputs, tablefmt='html'))

# %% [markdown]
# Az értéktáblázat alapján van elképzelésünk a függvényről:
#   - pozitív parabola, ami természetesen negatív és pozitív irányba is gyorsan nő (mivel 3 a négyzetes tag együtthatója),
#   - az értékei közt felvesz negatív számokat is, azaz a nullát két helyen is metszi (a negatív értékektől balra és jobbra),
#   - az egyik gyököt (ahol a függvény értéke 0, angolul: solution) megtaláltuk szerencsével (x=3, a másik valahol -1 és 0 között van).
#
# Lássuk többet látunk-e, ha ábrázoljuk ezeket a pontokat és megpróbáljuk csak egyszerűen összekötni őket!

# %%
import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Scatter(x=inputs, y=outputs, mode = 'markers+lines', name='f'))
fig.update_xaxes(range=[-2,4], zerolinecolor = 'black')
fig.update_yaxes(range=[-15,10], zerolinecolor = 'black')
fig.update_layout(width=600)
fig

# %% [markdown]
# Óvatosnak kell lenni, különben az ábra alapján hibát véthetünk:
#   - úgy tűnik, mintha a függvénynek a minimuma az 1-be lenne -10 értékkel,
#   - valamint úgy tűnik, mintha a második gyök $-{1\over2}$-nél lenne.
#
# Azonban emlékezzünk, hogy az ábrában egyszerűen csak 9 kiszámolt pontot kötöttünk össze szakaszokkal és a parabola természetesen nem szakaszokból áll, hanem egy folytonos, sehol sem "töredező" görbe, ezért ezek a sejtéseink könnyen helytelennek bizonyulhatnak.
#
# Használhatunk jobb szoftvert az ábrázoláshoz: [geogebra](https://geogebra.org/classic?command=a=Slider%28-10,10,0.5,0,200,False,True,False,False%29;b=Slider%28-10,10,0.5,0,200,False,True,False,False%29;c=Slider%28-10,10,0.5,0,200,False,True,False,False%29;a=3;b=-7;c=-6;f=ax^2%2bbx%2bc;ZoomIn%280.5%29)
#
# Ezen az ábrán nagyítva már megfigyelhető, hogy a feltételezéseink nem helyesek, a függvény minimum értéke lemegy -10 alá és a bal oldali gyök (nulla érték) sem a -1/2-nél van.
#
# Lássuk, hogyan tudnánk teljesen pontos ábrát rajzolni, papíron ceruzával, komoly számítógépes program nélkül!

# %% [markdown]
# ## Teljes négyzetes alak (más nevén: tengelyes vagy csúcsponti, angolul: vertex form)
#
# A következő ötletek kellenek, hogy eszünkbe jusson, a következő átalakítást, módszert kell elvégeznünk:
#   - $3x^2 - 7x - 6$
#     - az $x^2$ együtthatóját mindig kiemelejük, ez a lépés kihagyható, ha az négyzetes tag együtthatója 1
#   - $3(x^2 - {7\over3}x - 2)$
#     - a lineáris (csak $x$-et tartalmazó) tag együtthatóját olyan formára hozzuk, hogy valaminek a duplája legyen
#     - így már emlékeztet az $(a+b)^2 = a^2 + 2ab + b^2$ nevezetes azonosságra
#   - $3(x^2 - 2{7\over6}x - 2)$
#     - a nevezetes azonosságot visszafele alkalmazzuk, mindig $a=x^2$ és jelen esetben $b={7\over6}$
#     - azonban $b^2={7\over6}^2$ értéket nem látunk sehol, tehát azt le kell vonnunk, hogy ne "hazudjunk"
#   - $3((x-{7\over6})^2-{49\over36}-2)$
#     - a külső zárójelet felbontjuk, de a négyzet zárójelét természetesen nem, pont azon küzdöttünk, hogy az kialakuljon
#   - $3(x-{7\over6})^2 - {49\over12} - 6$
#     - végül a kifejezés végén lévő konstans (számokat) összevonjuk
#   - $3(x-{7\over6})^2 - {49+6\cdot12\over12}$ = $3(x-{7\over6})^2 - {121\over12}$ 
#
# A módszer végrehajtása után a végeredmény mindig ilyen alakú: $a(x+b)^2+c$, jelen esetben $a=3$, $b=-{7\over6}$ és $c=-{121\over12}$.
#
# Nagyon figyeljünk arra, amikor gondolkodunk, hogy az előjelek az egyes tagokhoz éppen negatívak vagy pozitívak!
#
# Ezt az alakot több okból is szeretik a matematikában, először is, nagyon könnyűvé teszi a függvény számítógép nélküli ábrázolását:
#   - kiindulunk az eredeti $x^2$ parabolábol az origóban,
#   - amennyiben $a\neq1$, akkor módosítjuk a parabolát a "meredekségével",
#     - pl. a jelenlegi $a=3$ esetben azt jelenti, hogy háromszor olyan gyorsan nő,
#     - azaz a szokásos 1, 4, 9, 16 négyzetszámok helyett azok háromszorosait kell ábrázolnunk: 3, 12, 27, 48,
#   - az így kapott $3x^2$ függvény még mindig origó középpontú, de gondoljuk meg, hogy ehhez képest a $3(x-{7\over6})^2$ függvény csak egy eltolás,
#     - méghozzá jobbra kell tolni $7\over6$ értékkel,
#     - igen, ez itt kicsit meglepő, a kifejezés kontravariánsan viselkedik: amennyiben $b<0$ akkor kell jobbra tolni és ha $b$ pozitív akkor kell balra tolni,
#     - ezt úgy könnyű megjegyezni, ha a nulla pontra koncentrálunk, nullának a négyzete is nulla és az $x-{7\over6}$ pont akkor nulla, ha az x-et jobbra toljuk pozitív ${7\over6}$-ba,
#   - végül az egész függvényt függőlegesen kell tolni $c$ értékével, pozitív esetén felfelé, negatív esetén lefelé, ezesetben nincs meglepetés.
#
# Az alábbi ábrán megtekinthető a lépések menete:
#   - piros: $x^2$
#   - narancs: $3x^2$
#   - kék: $3(x-{7\over6})^2$
#   - fekete: $3(x-{7\over6})^2-{121\over12}$
#
# (Vegyük észre, hogy az ábrán az x és y tengely a láthatóság kedvéért nem ugyanolyan beosztással van rajzolva, az y tengely jelentősen "sűrűbb", ezért látszik még a háromszoros parabola is nem túl gyorsan növekvőnek.)

# %%
import numpy as np

f1 = x**2
f2 = 3*x**2
f3 = 3*(x-7/6)**2
f4 = 3*(x-7/6)**2-121/12

# Generate a range of x-values for plotting
x_vals = np.linspace(-10, 10, 400)

# Evaluate each function over the range of x-values
y_vals_f1 = [float(f1.subs(x, val)) for val in x_vals]
y_vals_f2 = [float(f2.subs(x, val)) for val in x_vals]
y_vals_f3 = [float(f3.subs(x, val)) for val in x_vals]
y_vals_f4 = [float(f4.subs(x, val)) for val in x_vals]

# Create a Plotly figure
fig = go.Figure()

# Add scatter plot for each quadratic function
fig.add_trace(go.Scatter(x=x_vals, y=y_vals_f1, mode='lines', name='x²', line = { 'color': 'red' }))
fig.add_trace(go.Scatter(x=x_vals, y=y_vals_f2, mode='lines', name='3x²', line = { 'color': 'orange' }))
fig.add_trace(go.Scatter(x=x_vals, y=y_vals_f3, mode='lines', name='3(x-7/6)²', line = { 'color': 'blue' }))
fig.add_trace(go.Scatter(x=x_vals, y=y_vals_f4, mode='lines', name='f4', line = { 'color': 'black' }))

fig.update_xaxes(range=[-4,4], zerolinecolor = 'black')
fig.update_yaxes(range=[-15,20], zerolinecolor = 'black')

# Customize the layout
fig.update_layout(
    xaxis_title="x",
    yaxis_title="f(x)",
    template="plotly",
    width=800,  # Set desired width in pixels
    height=800  # Optionally set the height
)

# Display the plot
fig.show()

# %% [markdown]
# Lássuk, hogy segít-e ez az új alak a korábbi sejtéseink beigazolásában vagy megcáfolásában!
#
# Mivel a parabolát eltolással pozícionáltuk, forgatást nem végeztünk, tudjuk, hogy a minimuma, a parabola csúcsa az $x=7/6$ helyen van, ahol a minimális érték $121/12$. Tehát a korábbi értéktáblázatos ábrázolással mind a minimum helyét, mind az értékét helytelenül tippeltük.
#
# A zérus helyek, kiszámolását a következőképpen tehetjük az új forma alapján:
#   - $3(x-{7\over6})^2-{121\over12} = 0$
#   - hozzáadjuk az egyenlethez a konstanst
#   - $3(x-{7\over6})^2 = {121\over12}$
#   - osztunk hárommal
#   - $(x-{7\over6})^2 = {121\over36}$
#   - gyököt vonunk
#   - $|x-{7\over6}| = {11\over6}$
#   - $x_1-{7\over6} = {11\over6}$, azaz $x_1 = {18\over6} = 3$
#   - $-x_2+{7\over6} = {11\over6}$, azaz $x_2 = -{4\over6} = -{2\over3}$
#
# A második gyökben is tévedtünk, az nem a $-{1\over2}$, hanem a $-{2\over3}$ helyen van.
