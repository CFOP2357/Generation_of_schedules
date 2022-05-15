from tkinter import * 
from tkinter.ttk import Progressbar
from tkinter import filedialog
from PIL import ImageTk,Image
import threading
import file_manager as f_m
import data_processing as p
import algorithm as al

def ask_filename_csv(root: Tk):
	filename = filedialog.askopenfilename(title="Selecciona un archivo", 
										  filetypes=(("csv", "*.csv"), ("", "")))
	return filename

class UI(object):
	"""docstring for UI"""
	df_students = None
	df_majors = None
	df_subjects = None
	df_groups = None
	def __init__(self) -> None:
		
		self.root = Tk()
		self.root.title("Generación de Horarios")
        
		self.progreso = DoubleVar()#variable que monitoreara la barra de progreso
		# numero = f_m.Numero_Alumnos()
		# for num in numero:
		# 	numero = num[0]
		self.pbr_tarea = Progressbar(self.root, length=250, style='black.Horizontal.TProgressbar', variable=self.progreso, maximum=100)#aqui se agrega la variable que le da el aumento a la barra en la seccion de variable
		self.pbr_tarea['value'] = 0 #valor de inicio de barrra de progreso tambien se agrega el limite a la barra con maximum=#
		self.state = 0

		#Rutas de los archivos
		self.estudiantes_filename = ''
		self.grupos_filename = ''
		self.carreras_filename=''
		self.materias_filename=''
		self.root.resizable(False,False)
		self.root.iconbitmap('icono.ico')
		self.root.config(bg="#E9E9F1")
		self.headerImg = ImageTk.PhotoImage(Image.open('UASLP.PNG'))
		#self.root.iconbitmap(r'G:/Mi unidad/GenerationofSchedules/Generation-of-schedules/src/icono.ico')
		#self.root.config(bg="#E9E9F1")
		#self.headerImg = ImageTk.PhotoImage(Image.open(r'G:/Mi unidad/GenerationofSchedules/Generation-of-schedules/src/UASLP.PNG'))
		self.headerLabel = Label(self.root, image=self.headerImg)

		self.Label1 = Label(self.root, text="No cargado", bg="#E9E9F1")
		self.Label2 = Label(self.root, text="No cargado", bg="#E9E9F1")
		self.Label3 = Label(self.root, text="No cargado" , bg="#E9E9F1")
		self.Label4 = Label(self.root, text="No cargado", bg="#E9E9F1")
		self.Label5 = Label(self.root, text="No terminado", bg="#E9E9F1")
		self.Label_metricas = Label(self.root, text=" ", bg="#E9E9F1")
		self.Label6 = Label(self.root, text="Podrás descargar hasta que terminen los horarios", bg="#E9E9F1")
		self.label_general = Label(self.root, text="Favor de asignar todos los archivos para generar los horarios.",bg="#E9E9F1")

		self.label_Metrica = Label(self.root, text=" ",bg="#E9E9F1")
		self.open_estudiantes_button = Button(self.root, text="Abrir CSV de Estudiantes", 
											  command=self.update_estudiantes_filename,bg="#E9E9F1")
		self.open_grupos_button = Button(self.root, text="Abrir CSV de Grupos", 
										 command=self.update_grupos_filename,bg="#E9E9F1")
		self.open_carreras_button = Button(self.root, text="Abrir CSV de Carreras", 
										   command=self.update_carreras_filename,bg="#E9E9F1")
		self.open_materias_button = Button(self.root, text="Abrir CSV de Materias", 
										   command=self.update_materias_filename,bg="#E9E9F1")

		self.generate_schedules_button = Button(self.root, text="Generar Horarios", 
												command=self.run_thread,bg="#E9E9F1")
		self.generate_schedules_button["state"] = "disabled"
		self.download_schedule_button = Button(self.root, text="Descargar Horarios", 
												command=self.select_folder,bg="#E9E9F1")
		self.download_schedule_button["state"] = "disabled"
		self.build_ui()
    
	
	def select_folder(root: Tk):
		path = filedialog.askdirectory()
		print (path)
		# f_m.Crea_csv_horario(path)


	def run(self) -> None:
		self.root.mainloop()
	
	def button_gen_set(self) -> None:
		self.generate_schedules_button["state"] = "normal"

	def update_estudiantes_filename(self) -> None:
		self.estudiantes_filename = ask_filename_csv(self.root)
		r = f_m.read_error_filter(self.estudiantes_filename, "estudiantes")
		self.Label1['text'] = r[0]
		self.df_students = r[1]
		if(self.Label1['text'] == "El archivo de los estudiantes fue cargado correctamente"):
			self.open_estudiantes_button["state"] = "disabled"
			self.state +=1
			if(self.state == 4):
				self.button_gen_set()
		
	def update_grupos_filename(self) -> None:
		self.grupos_filename = ask_filename_csv(self.root)
		r = f_m.read_error_filter(self.grupos_filename, "grupos")
		self.Label2['text'] =  r[0]
		self.df_groups = r[1]
		if(self.Label2['text'] == "El archivo de los grupos fue cargado correctamente"):
			self.open_grupos_button["state"] = "disabled"
			self.state +=1
			if(self.state == 4):
				self.button_gen_set()
	
	def update_carreras_filename(self) -> None:
		self.carreras_filename = ask_filename_csv(self.root)
		r = f_m.read_error_filter(self.carreras_filename, "carreras")
		self.Label3['text'] = r[0]
		self.df_majors = r[1]
		if(self.Label3['text'] == "El archivo de las carreras fue cargado correctamente"):
			self.open_carreras_button["state"] = "disabled"
			self.state +=1
			if(self.state == 4):
				self.button_gen_set()

	def update_materias_filename(self) -> None:
		self.materias_filename = ask_filename_csv(self.root)
		r = f_m.read_error_filter(self.materias_filename, "materias")
		self.Label4['text'] = r[0]
		self.df_subjects = r[1]
		if(self.Label4['text'] == "El archivo de las materias fue cargado correctamente"):
			self.open_materias_button["state"] = "disabled"
			self.state +=1
			if(self.state == 4):
				self.button_gen_set()
	    
	def run_algorithm(self) -> None: 
		self.Label5['text'] = "generando horarios iniciales"
		process = p.DataProcessing(self.df_students,self.df_majors,self.df_subjects,self.df_groups)
		process.df_to_classes()
		al.algorithm()

		# self.Label5['text'] = "calculando metricas"

		# self.Label_metricas['text'] = "horarios completos: " + str(optimizador.get_metricas())

		# self.progreso.set(100)

		# self.Label5['text'] = "horario disponible"
		# self.download_schedule_button["state"] = "normal"
		# self.Label6['text'] = "Elige la carpeta para descargar los horarios"

		# self.generate_schedules_button['text'] = "Mejorar Horarios"
		# self.generate_schedules_button['command'] = self.run_thread2


	def run_thread(self):
		t1 = threading.Thread(target=self.run_algorithm)
		t1.start()	

	# def run_algorithm2(self) -> None: 
	# 	self.progreso.set(0)

	# 	self.download_schedule_button["state"] = "disabled"
	# 	self.Label5['text'] = "mejorando horario"
	# 	self.Label6['text'] = "Podrás descargar hasta que terminen los horarios"
		
	# 	ans = optimizador.enfriamiento_simulado(self)

	# 	self.Label5['text'] = "calculando metricas"
	# 	self.Label_metricas['text'] = "horarios completos: " + str(ans)

	# 	self.Label5['text'] = "horario disponible"
	# 	self.download_schedule_button["state"] = "normal"
	# 	self.Label6['text'] = "Elige la carpeta para descargar los horarios"

	# 	self.progreso.set(100)

	# 	self.generate_schedules_button['text'] = "Mejorar Horarios"
	# 	self.generate_schedules_button['command'] = self.run_thread2

	# def run_thread2(self):
	# 	t2 = threading.Thread(target=self.run_algorithm2)
	# 	t2.start()		



	def build_ui(self) -> None:
		self.headerLabel.grid(				padx=5,pady=4,ipadx=5,ipady=5, row=0, column=0, columnspan=3, sticky=S+N+E+W)
		self.label_general.grid(			padx=5,pady=4,ipadx=5,ipady=5, row=1, column=0, sticky=W)
		#self.label_Metrica.grid(			padx=5,pady=4,ipadx=5,ipady=5, row=2, column=0, sticky=W)
		self.open_estudiantes_button.grid(	padx=5,pady=4,ipadx=5,ipady=5, row=3, column=0, sticky=E+W)
		self.Label1.grid(                   padx=5,pady=4,ipadx=5,ipady=5, row=3, column=1, sticky=E+W)
		self.open_grupos_button.grid(		padx=5,pady=4,ipadx=5,ipady=5, row=4, column=0, sticky=E+W)
		self.Label2.grid(                   padx=5,pady=4,ipadx=5,ipady=5, row=4, column=1, sticky=E+W)
		self.open_carreras_button.grid(		padx=5,pady=4,ipadx=5,ipady=5, row=5, column=0, sticky=E+W)
		self.Label3.grid(                   padx=5,pady=4,ipadx=5,ipady=5, row=5, column=1, sticky=E+W)
		self.open_materias_button.grid(		padx=5,pady=4,ipadx=5,ipady=5, row=6, column=0, sticky=E+W)
		self.Label4.grid(                   padx=5,pady=4,ipadx=5,ipady=5, row=6, column=1, sticky=E+W)
		self.pbr_tarea.grid(                padx=5,pady=4,ipadx=5,ipady=5, row=7, column=0, sticky=E+W)#posicionamiento de barra
		self.Label5.grid(                   padx=5,pady=4,ipadx=5,ipady=5, row=7, column=1, sticky=E+W)
		self.generate_schedules_button.grid(padx=5,pady=4,ipadx=5,ipady=5, row=7, column=2, sticky=E+W)
		self.download_schedule_button.grid(padx=5,pady=4,ipadx=5,ipady=5, row=8, column=2, sticky=E+W)
		self.Label6.grid(                   padx=5,pady=4,ipadx=5,ipady=5, row=8, column=1, sticky=E+W)
		self.Label_metricas.grid(           padx=5,pady=4,ipadx=5,ipady=5, row=8, column=0, sticky=E+W)

		