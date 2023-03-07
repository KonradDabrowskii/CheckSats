import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk

# define a function to fetch the SAT and rarity values for a given URL
def fetch_sat_and_rarity(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    a_tag = soup.select_one('a[href^="/sat"]')
    if a_tag:
        value = a_tag.text.strip()

        sat_url = f'https://ordinals.com/sat/{value}'
        sat_response = requests.get(sat_url)
        sat_soup = BeautifulSoup(sat_response.content, 'html.parser')

        span_tag = sat_soup.select_one('span.common')
        if span_tag:
            sat_value = value
            rarity_value = span_tag.text.strip()

            time_tag = sat_soup.select_one('time')
            if time_tag:
                time_value = time_tag.text.strip()
            else:
                time_value = "No matching <time> tag found."

        else:
            sat_value = value
            rarity_value = "No matching <span> tag found."
            time_value = "No matching <time> tag found."

    else:
        sat_value = "No matching <a> tag found."
        rarity_value = ""
        time_value = "No matching <time> tag found."

    return sat_value, rarity_value, time_value

# define a function to process a list of URLs and display the results in the output_text box
def process_urls():
    output_text.delete(1.0, tk.END)
    urls = url_entry.get("1.0", tk.END).split('\n')
    urls = [url.strip() for url in urls if url.strip()]  # remove empty strings and leading/trailing whitespace

    for url in urls:
        sat_value, rarity_value, time_value = fetch_sat_and_rarity(url)
        output_text.insert(tk.END, f"INPUT LINK: {url}\nSAT: {sat_value}\nRARITY: {rarity_value}\nTIME: {time_value}\n\n")

# create the GUI
root = tk.Tk()
root.title("SAT Checker")
root.configure(bg="#2b2d42")

# create a style for the labels and buttons
style = ttk.Style()
style.configure("TLabel", background="#2b2d42", foreground="#ffffff")
style.configure("TButton", background="#000000", foreground="#000000", borderwidth=0)
style.configure('Dark.TButton', background='#000000', foreground='#000000')

# create the URL entry label
url_label = ttk.Label(root, text="Enter URLs (one per line):")
url_label.pack(pady=10)

# create the URL entry box
url_entry = tk.Text(root, height=10, width=50, bg="#1d1f2f", fg="#ffffff", borderwidth=0)
url_entry.pack()

# create the submit button
submit_button = ttk.Button(root, text="Check SATs", command=process_urls, style='DarkButton.TButton')
submit_button.pack(pady=10)

# create the output label
output_label = ttk.Label(root, text="Results:")
output_label.pack(pady=10)

# create the output text box
output_text = tk.Text(root, height=20, width=50, bg="#1d1f2f", fg="#ffffff", borderwidth=0)
output_text.pack()

root.mainloop()