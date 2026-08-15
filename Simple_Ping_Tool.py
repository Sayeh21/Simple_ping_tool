import customtkinter as ctk
import subprocess
import threading
import queue
import ipaddress
from PIL import Image
import re


ctk.set_appearance_mode('dark')



class Ping_app(ctk.CTk):
    def __init__(self):
       super().__init__()
       self.geometry('900x720')
       self.configure(fg_color="#1a0505")
       self.title('Ping Tool')
       self.create_header()
       self.create_ip_input()
       self.create_btn()
       self.create_container()
       self.status_frame()
       self.create_stats_cards()
       self.text_box()
       self.create_footer()

    #------------------------------PING ENGINE STATE----------------------------------------------

       self.result_queue = queue.Queue()
       self.stop_event = threading.Event()
       self.process = None
       self.check_queue()


       

    def create_header(self):
        header_frame = ctk.CTkFrame(self ,fg_color='transparent')
        header_frame.pack(fill='x' ,padx =20 ,pady=(20,10))

        icon_frame = ctk.CTkFrame(header_frame,width=50 ,height=50 ,corner_radius=20 ,border_width=2)
        icon_frame.pack_propagate(False)
        icon_frame.pack(side='left' ,padx=(0,15))

        icon_image = ctk.CTkImage(
                     light_image=Image.open("icon.png"),
                     dark_image=Image.open("icon.png"),
                     size=(70, 70)
        )


        icon_label = ctk.CTkLabel(icon_frame, image=icon_image, text="")
        icon_label.pack(expand=True)

        txt_frame =ctk.CTkFrame(header_frame ,fg_color="transparent")
        txt_frame.pack(side='left')

        title_lable =ctk.CTkLabel(txt_frame ,text='Simple Ping Tool' ,font=('Arial' ,29,'bold'),text_color="#FFFFFF")
        title_lable.pack(anchor='w')

        sub_lable =ctk.CTkLabel(txt_frame,text='N E T W O R K   D I A G N O S T I C S',font=('arial',14),text_color="#c0392b")
        sub_lable.pack(anchor='w')


    def create_ip_input(self):
        self.ip_entry =ctk.CTkEntry(self ,
                  placeholder_text='Enter ip address or domain',
                  placeholder_text_color="#C3BEBE",
                  height=45,
                  border_width=1,
                  border_color="#A89E9E",
                  fg_color="#1F1010",
                  text_color="#FFFFFF",
                  font=('arial',13)  ,
                  corner_radius=20
        )
        self.ip_entry.pack(fill='x' ,padx=20,pady=10)                                                                                            


    def create_btn(self):
        btn_frame = ctk.CTkFrame(self ,fg_color='transparent')
        btn_frame.pack(fill='x',padx=20,pady=10)

        btn_frame.grid_columnconfigure(0,weight=1)
        btn_frame.grid_columnconfigure(1,weight=1)

        self.ping_btn =ctk.CTkButton(btn_frame ,
                  fg_color="#1F1010" ,
                  border_width= 1,
                  border_color="#5B5959" ,
                  text='Ping',
                  text_color="#FFFFFF" ,
                  hover_color="#1A2A1B" ,
                  height=45 ,
                  corner_radius=15 ,
                  command=self.start_ping
        )
        self.ping_btn.grid(row=0,column=0 ,sticky='ew',padx=(0,10))
  
        self.stop_btn = ctk.CTkButton(btn_frame,
                    fg_color="#1F1010" ,
                    border_width= 1,
                    border_color="#551C1C" ,
                    text='Stop',
                    text_color="#FFFFFF" ,
                    hover_color="#391717" ,
                    height=45 ,
                    corner_radius=15 ,
                    command=self.stop_ping,
                    state='disabled'
        )
        self.stop_btn.grid(row=0,column=1 ,sticky='ew',padx=(10,0))


        
    def create_container(self):
        self.main_frame = ctk.CTkFrame(self ,
                          fg_color="#1a0505"  ,
                          border_width=1 ,
                          border_color= "#000000" ,
                          corner_radius= 15 
        )
        self.main_frame.pack(fill='both' ,expand=True,padx=10,pady=20)           

    def status_frame(self):
        status_frame =ctk.CTkFrame(self.main_frame,fg_color="transparent")
        status_frame.pack(fill='x' ,pady=(15,10))

        inner = ctk.CTkFrame(status_frame, fg_color="transparent")
        inner.pack(anchor="center")

        self.status_label = ctk.CTkLabel(inner, text="READY", text_color="#2ecc71", font=('Arial', 16, 'bold'))
        self.status_label.pack(side='left')

        separator = ctk.CTkFrame(self.main_frame, height=1.5, fg_color="#5B5959")
        separator.pack(fill='x', padx=15, pady=(5,15))


    def create_stat_card (self, parent ,title ,value):

        card =ctk.CTkFrame(parent ,fg_color='#0d0303' ,border_width=1 ,border_color="#5B5959",corner_radius=10)

        title_lable =ctk.CTkLabel(card ,text=title ,text_color='#ffffff' ,font=('arial' ,11 ))
        title_lable.pack(pady=(12,5))

        value_lable =ctk.CTkLabel(card ,text=value ,font=('arial' ,18 ,'bold'),text_color='#2ecc71')
        value_lable.pack(pady=(0,12))

        return card,value_lable 


    
    def create_stats_cards(self):
        cards_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        cards_frame.pack(fill='x', padx=15, pady=(0, 15))

        for i in range(5):
            cards_frame.grid_columnconfigure(i, weight=1)

        card1, self.loss_label = self.create_stat_card(cards_frame, "PACKET LOSS", "0%")
        card1.grid(row=0, column=0, sticky="ew", padx=5)

        card2, self.avg_label = self.create_stat_card(cards_frame, "AVERAGE", "0 ms")
        card2.grid(row=0, column=1, sticky="ew", padx=5)

        card3, self.host_label = self.create_stat_card(cards_frame, "HOST", "-")
        card3.grid(row=0, column=2, sticky="ew", padx=5)

        card4, self.min_label = self.create_stat_card(cards_frame, "MIN", "0 ms")
        card4.grid(row=0, column=3, sticky="ew", padx=5)

        card5, self.max_label = self.create_stat_card(cards_frame, "MAX", "0 ms")
        card5.grid(row=0, column=4, sticky="ew", padx=5)


    def text_box(self):
        self.txt_box =ctk.CTkTextbox(self.main_frame ,
                    fg_color="#1a0505",
                    text_color="#ffffff",
                    font=("Consolas", 12),
                    corner_radius=10,
                    border_width=1,
                    border_color="#5B5959"

        )
        self.txt_box.pack(fill='both', expand=True, padx=15, pady=(0, 15))

    def create_footer(self):
        footer_label = ctk.CTkLabel(
        self,
        text="made by sayeh21",
        font=('Arial', 10),
        text_color="#5c4a4a", 
        corner_radius=30,
        height=5
    )
        footer_label.place(relx=1.0, rely=1.0, anchor='se', x=-15, y=-10)
    #------------------------------PING LOGIC----------------------------------------------

    def validate_target(self, target):
        target = target.strip()

        try:
            ipaddress.ip_address(target)
            return True
        except ValueError:
            pass

        if len(target) > 253:
            return False

        if target.endswith('.'):
            target = target[:-1]

        labels = target.split('.')

        if len(labels) < 2:
            return False

        for label in labels:
            if not label:
                return False
            if len(label) > 63:
                return False
            if label.startswith('-') or label.endswith('-'):
                return False
            if not re.fullmatch(r'[A-Za-z0-9-]+', label):
                return False

        return True


    def run_ping(self):
        ip = self.ip_entry.get().strip()

        if ip == '':
            self.result_queue.put(("⚠️ ERROR", "Please enter IP address or domain.", "--", "--", "--", "--", "--"))
            return

        if not self.validate_target(ip):
            self.result_queue.put(("❌ INVALID TARGET", "Please enter a valid IP address or domain.", "--", "--", "--", "--", "--"))
            return

        self.process = subprocess.Popen(
            ['ping', '-n', '4', ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        proc = self.process
        lines = []
        for line in self.process.stdout:
            line = line.strip()
            lines.append(line)
            self.result_queue.put(("LIVE", line, "--", "--", ip, "--", "--"))
        proc.wait()
        stdout = '\n'.join(lines)

        if self.stop_event.is_set():
            self.result_queue.put(("🛑 STOPPED", "Ping was stopped.", "--", "--", ip, "--", "--"))
            self.process = None
            return

        loss_match = re.search(r'\((\d+)% loss\)', stdout)
        loss = loss_match.group(1) if loss_match else "N/A"

        latency_match = re.search(r'Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms', stdout)
        if latency_match:
            minimum = latency_match.group(1)
            maximum = latency_match.group(2)
            average = latency_match.group(3)
        else:
            minimum = maximum = average = "N/A"

        status = "🟢 ONLINE" if self.process.returncode == 0 else "🔴 OFFLINE"

        result = (
            f"Packet Loss: {loss}%\n"
            f"Minimum: {minimum}ms\n"
            f"Maximum: {maximum}ms\n"
            f"Average: {average}ms\n\n"
            f"{stdout}"
        )

        self.result_queue.put((status, result, loss, average, ip, minimum, maximum))
        self.process = None


    def start_ping(self):
        self.txt_box.delete('1.0', 'end')
        self.status_label.configure(text='🟡 Pinging...')
        self.ping_btn.configure(state='disabled')
        self.stop_btn.configure(state='normal')
        self.stop_event.clear()

        thread = threading.Thread(target=self.run_ping, daemon=True)
        thread.start()


    def stop_ping(self):
        self.stop_event.set()
        if self.process is not None:
            self.process.terminate()
            self.process = None


    def check_queue(self):
        try:
          status, res, loss, average, ip, minimum, maximum = self.result_queue.get_nowait()

          if status == "LIVE":
            self.txt_box.insert('end', res + '\n')
            self.txt_box.see('end')
          else:
            if "ONLINE" in status:
                color = "#2ecc71"
            elif "OFFLINE" in status:
                color = "#b31e19"
            elif "ERROR" in status or "INVALID" in status:
                color = "#d85c19"
            elif "STOPPED" in status:
                color = "#e67e22"
            else:
                color = "#2ecc71"

            self.status_label.configure(text=status, text_color=color)

            self.ping_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")

            self.loss_label.configure(text=f"{loss}%")
            self.avg_label.configure(text=f"{average} ms")
            self.host_label.configure(text=ip)
            self.min_label.configure(text=f"{minimum} ms")
            self.max_label.configure(text=f"{maximum} ms")

            self.txt_box.delete('1.0', 'end')
            self.txt_box.insert('end', res)

        except queue.Empty:
           pass

        self.after(100, self.check_queue)



if __name__ =="__main__":
    app =Ping_app()
    app.mainloop()