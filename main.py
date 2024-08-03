import speedtest
import requests
import customtkinter as ctk
from tkinter import messagebox

def get_public_ip():
    try:
        response = requests.get('https://api.myip.com')
        return response.json().get('ip', 'Unknown IP')
    except Exception as e:
        return f"Error: {e}"

def test_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convertir a Mbps
        upload_speed = st.upload() / 1_000_000  # Convertir a Mbps
        latency = st.results.ping
        public_ip = get_public_ip()
        return download_speed, upload_speed, latency, public_ip
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None, None, None, None

def update_speed():
    download_speed, upload_speed, latency, public_ip = test_speed()
    if download_speed is not None:
        lbl_download.configure(text=f"Download Speed: {download_speed:.2f} Mbps")
        lbl_upload.configure(text=f"Upload Speed: {upload_speed:.2f} Mbps")
        lbl_latency.configure(text=f"Latency: {latency} ms")
        lbl_ip.configure(text=f"Public IP: {public_ip}")

# Configuración de la ventana principal
root = ctk.CTk()
root.title("Internet Speed Test")

# Agregar widgets
lbl_download = ctk.CTkLabel(root, text="Download Speed: N/A")
lbl_download.pack(pady=10)
lbl_upload = ctk.CTkLabel(root, text="Upload Speed: N/A")
lbl_upload.pack(pady=10)
lbl_latency = ctk.CTkLabel(root, text="Latency: N/A")
lbl_latency.pack(pady=10)
lbl_ip = ctk.CTkLabel(root, text="Public IP: N/A")
lbl_ip.pack(pady=10)

btn_test = ctk.CTkButton(root, text="Test Speed", command=update_speed)
btn_test.pack(pady=20)

# Iniciar la aplicación
root.mainloop()
