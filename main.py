import speedtest
import requests
import customtkinter as ctk
from tkinter import messagebox
import time

def get_public_ip():
    try:
        response = requests.get('https://api.myip.com')
        return response.json().get('ip', 'Unknown IP')
    except Exception as e:
        return f"Error: {e}"

def test_speed(num_tests=3):
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        
        download_speeds = []
        upload_speeds = []
        
        start_time = time.time()  # Marca el tiempo de inicio
        
        for _ in range(num_tests):
            download_speed = st.download() / 1_000_000  # Convertir a Mbps
            upload_speed = st.upload() / 1_000_000  # Convertir a Mbps
            latency = st.results.ping
            
            download_speeds.append(download_speed)
            upload_speeds.append(upload_speed)
            
            time.sleep(1)  # Esperar un segundo entre pruebas para evitar interferencias

        avg_download_speed = sum(download_speeds) / len(download_speeds)
        avg_upload_speed = sum(upload_speeds) / len(upload_speeds)
        public_ip = get_public_ip()
        
        elapsed_time = time.time() - start_time  # Calcula el tiempo transcurrido
        
        return avg_download_speed, avg_upload_speed, latency, public_ip, elapsed_time
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        return None, None, None, None, None

def update_speed():
    global running
    global start_time
    running = True
    start_time = time.time()  # Marca el tiempo de inicio
    lbl_status.configure(text="Testing...")
    btn_test.configure(state="disabled")
    update_timer()  # Inicia la actualización del cronómetro

def update_timer():
    if running:
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        lbl_timer.configure(text=f"Time Elapsed: {minutes:02}:{seconds:02}")
        root.after(1000, update_timer)  # Actualiza el cronómetro cada segundo

def stop_test():
    global running
    running = False
    lbl_status.configure(text="Completed")
    btn_test.configure(state="normal")

    download_speed, upload_speed, latency, public_ip, _ = test_speed(num_tests=3)
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

lbl_timer = ctk.CTkLabel(root, text="Time Elapsed: 00:00")
lbl_timer.pack(pady=10)

lbl_status = ctk.CTkLabel(root, text="")
lbl_status.pack(pady=10)

btn_test = ctk.CTkButton(root, text="Start Test", command=update_speed)
btn_test.pack(pady=20)

# Inicializa la variable de estado
running = False
start_time = 0

# Iniciar la aplicación
root.mainloop()
