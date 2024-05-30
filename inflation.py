import tkinter as tk
from tkinter import simpledialog, messagebox


def calculate_past_price(current_price, target_year, current_year=2023):
    inflation_rates = {
        1924: 0.004, 1925: 0.024, 1926: 0.009, 1927: -0.019, 1928: -0.012, 1929: 0.0,
        1930: -0.027, 1931: -0.089, 1932: -0.103, 1933: -0.052, 1934: 0.035, 1935: 0.026,
        1936: 0.01, 1937: 0.037, 1938: -0.02, 1939: -0.013, 1940: 0.007, 1941: 0.051,
        1942: 0.109, 1943: 0.06, 1944: 0.016, 1945: 0.023, 1946: 0.085, 1947: 0.144,
        1948: 0.077, 1949: -0.01, 1950: 0.011, 1951: 0.079, 1952: 0.023, 1953: 0.008,
        1954: 0.003, 1955: -0.003, 1956: 0.015, 1957: 0.033, 1958: 0.027, 1959: 0.0108,
        1960: 0.015, 1961: 0.011, 1962: 0.012, 1963: 0.012, 1964: 0.013, 1965: 0.016,
        1966: 0.03, 1967: 0.028, 1968: 0.043, 1969: 0.055, 1970: 0.058, 1971: 0.043,
        1972: 0.033, 1973: 0.062, 1974: 0.111, 1975: 0.091, 1976: 0.057, 1977: 0.065,
        1978: 0.076, 1979: 0.113, 1980: 0.135, 1981: 0.103, 1982: 0.061, 1983: 0.032,
        1984: 0.043, 1985: 0.035, 1986: 0.019, 1987: 0.037, 1988: 0.041, 1989: 0.048,
        1990: 0.054, 1991: 0.042, 1992: 0.03, 1993: 0.03, 1994: 0.026, 1995: 0.028,
        1996: 0.029, 1997: 0.023, 1998: 0.016, 1999: 0.022, 2000: 0.034, 2001: 0.028,
        2002: 0.016, 2003: 0.023, 2004: 0.027, 2005: 0.034, 2006: 0.032, 2007: 0.029,
        2008: 0.038, 2009: -0.004, 2010: 0.016, 2011: 0.032, 2012: 0.021, 2013: 0.015,
        2014: 0.016, 2015: 0.001, 2016: 0.013, 2017: 0.021, 2018: 0.024, 2019: 0.018,
        2020: 0.012, 2021: 0.047, 2022: 0.08, 2023: 0.041
    }

    if target_year > current_year:
        raise ValueError("Target year cannot be in the future.")
    elif target_year < 1924:
        raise ValueError("Data not available for years before 1924.")

    past_price = current_price
    for year in range(target_year, current_year):
        rate = inflation_rates.get(year, 0)  # Use default rate of 0 if year is missing
        past_price /= (1 + rate)

    return past_price


def on_calculate():
    try:
        current_price = float(price_var.get())
        target_year = int(year_var.get())
        result = calculate_past_price(current_price, target_year)
        messagebox.showinfo("Result", f"The estimated price of the item in {target_year} is: ${result:.2f}")
    except ValueError as e:
        messagebox.showerror("Error", str(e))


# Setting up the main window
root = tk.Tk()
root.title("Inflation Calculator")
root.geometry("300x200")
root.configure(bg='white')

# Setting up the entry fields and labels
tk.Label(root, text="Enter the current price of the item:", bg='white', fg='blue').pack(pady=(20, 5))
price_var = tk.StringVar()
price_entry = tk.Entry(root, textvariable=price_var, highlightbackground='red')
price_entry.pack()

tk.Label(root, text="Enter the target year to find the price for:", bg='white', fg='blue').pack(pady=5)
year_var = tk.StringVar()
year_entry = tk.Entry(root, textvariable=year_var, highlightbackground='red')
year_entry.pack()

# Calculate button
calculate_button = tk.Button(root, text="Calculate", command=on_calculate, bg='blue', fg='red')
calculate_button.pack(pady=(20, 0))

# Main event loop
root.mainloop()
