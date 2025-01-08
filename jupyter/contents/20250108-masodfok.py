# %% [markdown]
# # Másodfokú függvények és egyenletek
#
# ## Bevezető
#
# Másodfokú polinómoknak nevezik az olyan kifejezéseket, aminek alakja $3x^2 - 7x - 6$ (ahol természetesen a 3, a -7 és a -6 számok helyett más számok is állhatnak, negatívak és törtek is mind a három helyen).
#
# Lássuk, hogy ezek a kifejezések (és a belőlük képzett függvények, egyenletek), hogyan viselkednek, hogyan kell őket koordináta rendszerben ábrázolni, illetve a zérushelyeiket megkeresni.
#
# Emlékeztető: elsőfokú, azaz $4x + 13$ alakú kifejezéseknél a helyzet viszonylag egyszerű volt, a zérushely egyszerű egyenletmegoldással (13-at kivonunk, majd osztunk 4-gyel) megtalálható, az ábrázolás során pedig mindig egy egyenest kapunk (jelen esetben 4 meredekségű és 13-mal felfele eltolt az y tengelyen).
#
# ## Általános alak
#
# A másodfokú kifejezés általános alakjának azt hívják amit korábban is láttunk: $f(x) = 3x^2 - 7x - 6$.
#
# Ez az alak remekül használható értéktáblázat készítéséhez, csak be kell helyettesítenünk a kívánt számokat és készen vagyunk.

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
#   - az egyik megoldást megtaláltuk szerencsével (x=3, a másik valahol -1 és 0 között van).
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
#   - valamint úgy tűnik, mintha a második gyök -1/2-nél lenne.
#
# Azonban emlékezzünk, hogy az ábrában egyszerűen csak 9 kiszámolt pontot kötöttünk össze szakaszokkal és a parabola természetesen nem szakaszokból áll, hanem egy folytonos, sehol sem "töredező" görbe, ezért ezek a sejtéseink könnyen helytelennek bizonyulhatnak.
#
# Nyilván használhatunk jobb szoftvert az ábrázoláshoz: [geogebra](https://geogebra.org/classic?command=a=Slider%28-10,10,0.5,0,200,False,True,False,False%29;b=Slider%28-10,10,0.5,0,200,False,True,False,False%29;c=Slider%28-10,10,0.5,0,200,False,True,False,False%29;a=3;b=-7;c=-6;f=ax^2%2bbx%2bc;ZoomIn%280.5%29)
