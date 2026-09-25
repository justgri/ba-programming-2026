import streamlit as st

st.set_page_config(page_title="Intro Streamlit App")

st.markdown("""
# Week 2 - Python Intro
## Disclaimer: this code is AI-generated
""")


st.markdown("""
## Streamlit Basics

Run this app from the `intro` folder with `streamlit run intro_app.py`.
Streamlit runs your Python script from top to bottom. Changing a widget normally
reruns the whole script and updates the page.

- `st.markdown("**Hello**")`: display formatted text, headings, and lists.
- `st.write("Result:", 42)`: display text, values, or data.
- `st.title("My app")` / `st.header("Section")`: add headings.
- `st.code("x = 1")`: display code without running it.
- `st.columns(2)`: arrange content side by side.
- `st.text_input("Name")`: get text from the user.
- `st.slider("Age", 0, 100, 23)`: select a number.
- `st.button("Say hello")`: return `True` on the rerun triggered by a click.
""")

# A tiny interactive example with two columns
left, right = st.columns(2)
with left:
    demo_name = st.text_input("Your name", "Student")
with right:
    demo_age = st.slider("Your age", 0, 100, 23)

if st.button("Say hello"):
    st.write(f"Hello, {demo_name}! You are {demo_age} years old.")


st.markdown("""
## Preserving Variables with Session State

An ordinary variable such as `count = 0` resets whenever the script reruns.
Use `st.session_state` to keep a value across reruns in the current browser session.
Initialize it only if it does not exist, then read or update it like a dictionary.
This is temporary storage: refreshing the browser page resets the session.

```python
if "count" not in st.session_state:
    st.session_state["count"] = 0

if st.button("Add 1"):
    st.session_state["count"] += 1

st.write("Count:", st.session_state["count"])
```

Try the counter below, then change your name or age above: the count stays the same.
""")

if "count" not in st.session_state:
    st.session_state["count"] = 0

if st.button("Add 1"):
    st.session_state["count"] += 1

st.write("Count:", st.session_state["count"])


st.markdown("""
# Topic 1 - Object Types

We’ll create: **bool, int, float, str, list, tuple, dict**.  
Check types with `type()`. Cast types with `int()`, `float()`, `str()` when sensible.
""")


# Booleans
is_student = True
has_halbtax = False
st.write(f"{is_student} {type(is_student)}")

# Integers & floats
population_ch = 8_900_000  # ~8.9M
inflation = 1.6  # %
st.write(f"{type(population_ch)} {type(inflation)}")


# Strings
city = "Zürich"
currency = "CHF"
greeting = f"Welcome to {city}!"
st.write(f"{greeting} {type(greeting)}")

# Lists (mutable)
cantons = ["ZH", "BE", "LU", "UR"]
cantons.append("VD")
st.write(f"{cantons} {type(cantons)}")

# Tuples (immutable)
coords_uni_zh = (47.376, 8.548)
st.write(f"{coords_uni_zh} {type(coords_uni_zh)}")

# Dictionaries (key → value)
gdp = {"CH": 800, "DE": 4500, "LT": 70}  # CHF billions (illustrative)
st.write(f"{gdp} {type(gdp)}")

# Type casting
year_str = "2025"
year_int = int(year_str)
pi_str = "3.14"
pi_float = float(pi_str)
st.write(f"{year_int} {type(year_int)} | {pi_float} {type(pi_float)}")


st.markdown("""
**⏱️ Mini-exercise**  
Create your own: a `str` with your **major**, an `int` with **ECTS**, and a `dict` mapping **course code → ECTS**. Print their `type()`.
""")


st.markdown("""
# Topic 2 - Indexing & Slicing

Access elements inside: **strings**, **lists/tuples**, and **dicts**.  
- Zero-based indexing: first item is index `0`.  
- Slicing: `seq[start:stop:step]` (stop is exclusive).
""")


# Strings
sbb_line = "IC5: Zürich HB → Lausanne"
st.write(sbb_line[0], sbb_line[-1])  # first and last char
st.write(sbb_line[4:10])  # slice
st.write(sbb_line[::-1])  # reverse

# Lists / tuples
fares = [3.4, 4.2, 8.8, 12.5]  # CHF
st.write(fares[0], fares[1:3], fares[-1])
st.write(coords_uni_zh[0])  # tuple indexing

# Dictionaries
st.write(gdp["CH"])  # by key
gdp["CH"] = gdp["CH"] * 1.01  # update value
st.write(gdp.get("FR", "No data"))  # safe get with default


st.markdown("""
**⏱️ Mini-exercise**  
Given `name = "University of Zurich"`, slice to get `"Zurich"`. From `cantons`, get the last two entries via slicing.
""")


st.markdown("""
# Topic 3 - Basic Operations & Built-in Functions

- **Math** on numbers: `+ - * / // % **`  
- **Strings**: concatenation `+`, repeat `*`, `.upper()`, `.lower()`, `.replace()`  
- **Lists**: `len`, `sorted`, `.append()`, `.extend()`
""")


# Numbers
monthly_ticket = 70  # CHF (example)
months = 6
cost_semester = monthly_ticket * months
st.write("Semester cost:", cost_semester)

# Strings
school = "UZH"
msg = school + " Economics"
st.write(msg, "| upper:", msg.upper())

# Lists: length & sorting
prices = [12.5, 3.4, 8.8, 4.2]
st.write("n =", len(prices), "| sorted:", sorted(prices))

# Mutating list
prices.append(6.9)
st.write("updated:", prices)


st.markdown("""
**⏱️ Mini-exercise**  
Create a list of three **favorite Swiss cities**, then print how many and the sorted list alphabetically.
""")


st.markdown("""
# Topic 4 - Booleans & Conditionals

Use comparisons to produce booleans, then branch with `if / elif / else`.
Common comparisons: `==`, `!=`, `>`, `<`, `>=`, `<=`; combine with `and`, `or`, `not`.
""")


# Simple policy example: student discount if age < 25 OR has Halbtax
age = 23
has_halbtax = True

eligible = (age < 25) or has_halbtax
st.write("Discount eligible?", eligible)

# If/elif/else
income = 2200  # CHF/month (toy example)
if income < 2000:
    bracket = "low"
elif income < 5000:
    bracket = "middle"
else:
    bracket = "high"
st.write("Income bracket:", bracket)


st.markdown("""
# Topic 5 - Fille Input/Output""")


# Use the existing data folder at the root of week_2
from pathlib import Path

# Paths are relative to this notebook's intro folder
DATA = Path("../../data")
in_path = DATA / "cities.txt"
out_path = DATA / "cities_clean.txt"


# 1) Read the .txt file
raw_text = in_path.read_text(encoding="utf-8")
lines = raw_text.splitlines()

# 2) Clean & transform (strip empties, normalize spacing, Title Case)
cleaned = []
for ln in lines:
    ln = ln.strip()
    if not ln:
        continue
    cleaned.append(ln.title())

# 3) Save to a new .txt
out_path.write_text("\n".join(cleaned), encoding="utf-8")

# 4) Quick preview
st.write(f"Input file:  {in_path} ({len(lines)} lines)")
st.write(f"Output file: {out_path} ({len(cleaned)} lines)\n")
st.write("Preview:")
for ln in cleaned[:5]:
    st.write(" •", ln)


st.markdown("""# Topic 6 - Importing Libraries & Local Scripts

Use `import` to access reusable code. An alias such as `np` gives a library a shorter name; use `name.function()` to call its functions.
NumPy must be installed in your notebook environment (if needed, run `%pip install numpy` in a separate cell). `math` comes with Python.
""")


# Import two libraries and call their functions
import numpy as np
import math

prices = [3.4, 4.2, 8.8, 12.5]
st.write("Average price:", np.mean(prices))
st.write("Square root of 81:", math.sqrt(81))


st.markdown(
    """A local `.py` file can also be imported as a **module**. The companion `my_module.py` is in this notebook's folder; run with `intro` as the working directory.
`from ... import ...` imports selected variables; `import ...` imports the whole module, whose variables and functions you access with a dot. Omit `.py` in both forms.
Python runs a module's top-level code on its first import in a kernel session.
"""
)


# Import selected variables from the local script
from my_module import city, ticket_price

st.write("City:", city)
st.write("Ticket price:", ticket_price, "CHF")

# Import the whole local script as a module
import my_module

st.write("Currency:", my_module.currency)
st.write("Cost of 3 tickets:", my_module.total_cost(3), my_module.currency)
