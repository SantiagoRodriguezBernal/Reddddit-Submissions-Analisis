import zstandard
import os
import json
import sys
import csv
from datetime import datetime
import logging.handlers


# Especificar la ruta del archivo de entrada o carpeta de archivos a procesar

#input_file = r"\\MYCLOUDPR4100\Public\reddit\subreddits23\wallstreetbets_submissions.zst"

# Especificar el nombre o ruta del archivo de salida. La extensión del archivo se añadirá automáticamente.
# Si el archivo de entrada es una carpeta, la salida también se tratará como una carpeta

#output_file = r"\\MYCLOUDPR4100\Public\output"

# Formato de salida, elegir una de las siguientes opciones:
#   zst: igual que el archivo de entrada, un archivo ndjson comprimido con zstandard. Puede ser leído por otros scripts en el repositorio
#   txt: un archivo ndjson, que es un archivo de texto con un objeto json separado en cada línea. Puede abrirse con cualquier editor de texto
#   csv: un archivo de valores separados por comas. Puede abrirse con un editor de texto o Excel
# ADVERTENCIA: si usas salida en txt o csv en un archivo de entrada grande sin filtrar la mayoría de las filas, el archivo resultante será extremadamente grande.
# Generalmente, alrededor de 7 veces más grande que el archivo de entrada comprimido.

#output_format = "csv"

# Sobrescribir el formato anterior y output solo este campo en un archivo de texto, uno por línea.
# Útil si quieres hacer una lista de autores o IDs. Ver los ejemplos abajo.
# Cualquier campo que esté en el dump es soportado, pero los útiles son:
#   author: el nombre de usuario del autor
#   id: el ID de la publicación o comentario
#   link_id: solo para comentarios, el nombre completo de la publicación a la que está asociado el comentario
#   parent_id: solo para comentarios, el nombre completo del padre del comentario. Puede ser otro comentario o la publicación si es de nivel superior

#single_field = None

# Los campos en el archivo son diferentes dependiendo de si tiene comentarios o publicaciones.
# Si estamos escribiendo un csv, necesitamos saber qué campos escribir.
# Configurar esto en true para escribir en el log cada vez que hay una línea incorrecta, configurarlo en false si esperas que solo algunas de las líneas coincidan con la clave

# write_bad_lines = True

# Solo output elementos entre estas dos fechas
#from_date = datetime.strptime("2005-01-01", "%Y-%m-%d")
#to_date = datetime.strptime("2030-12-31", "%Y-%m-%d")

# Campo a filtrar, los valores a filtrar y si debe ser una coincidencia exacta.
# Algunos ejemplos:
#
# Retornar solo objetos donde el autor sea u/watchful1 o u/spez
# field = "author"
# values = ["watchful1","spez"]
# exact_match = True
#
# Retornar solo objetos donde el título contenga "stonk" o "moon"
# field = "title"
# values = ["stonk","moon"]
# exact_match = False
#
# Retornar solo objetos donde el cuerpo contenga "stonk" o "moon". Para publicaciones el cuerpo está en el campo "selftext", para comentarios está en el campo "body"
# field = "selftext"
# values = ["stonk","moon"]
# exact_match = False
#
#
# Filtrar un archivo de publicaciones y luego obtener un archivo con todos los comentarios solo en esas publicaciones. Este es un proceso de varios pasos.
# Añade tus filtros de publicaciones y configura el nombre del archivo de salida a algo único
# input_file = "redditdev_submissions.zst"
# output_file = "filtered_submissions"
# output_format = "csv"
# field = "author"
# values = ["watchful1"]
#
# Ejecuta el script, esto resultará en un archivo llamado "filtered_submissions.csv" que contiene solo publicaciones de u/watchful1
# Ahora ejecutaremos el script nuevamente con los mismos filtros de entrada, pero configurando la salida a campo único. Asegúrate de cambiar el archivo de salida a un nuevo nombre, pero no cambies ninguna de las otras entradas
# output_file = "submission_ids"
# single_field = "id"
#
# Ejecuta el script nuevamente, esto resultará en un archivo llamado "submission_ids.txt" que tiene un ID en cada línea
# Ahora eliminaremos todos los otros filtros y actualizaremos el script para que la entrada sea desde el archivo de comentarios, y usemos la lista de IDs de publicaciones que creamos antes. Y cambiamos el nombre de la salida nuevamente para no sobrescribir nada
# input_file = "redditdev_comments.zst"
# output_file = "filtered_comments"
# single_field = None  # reiniciando esto para que no se use
# field = "link_id"  # en el objeto de comentario, este es el campo que contiene el ID de la publicación
# values_file = "submission_ids.txt"
# exact_match = False  # el campo link_id tiene un prefijo, por lo que no podemos hacer una coincidencia exacta
#
# Ejecuta el script una última vez y ahora tendrás un archivo llamado "filtered_comments.csv" que solo tiene comentarios de tus publicaciones anteriores
# Si solo quieres comentarios de nivel superior en lugar de todos los comentarios, puedes configurar field a "parent_id" en lugar de "link_id"

# Cambia esto a field = None si no quieres filtrar por nada
#field = "body"
#values = ['']

# Si tienes una lista larga de valores, puedes ponerlos en un archivo y especificar el nombre del archivo aquí. Si se configura, esto anula la lista de valores anterior
# Si esta lista es muy grande, podría ralentizar enormemente el proceso
#values_file = None
#exact_match = False

########################
# EJECUCIÓN REALIZADA  #
########################

input_file = "C:/Users/estudiante/Desktop/submissions/RS_2021-01.zst"

output_file = "C:/Users/estudiante/Desktop/Submissions_Output/submission_test"

output_format = "csv"

single_field = None

write_bad_lines = False

field = "selftext"

values = ["hack","attack","breach","leak","vulnerability","exploit","phish","phishing","malware","ransomware","cyber","hacker","password","service","security","account"]

exact_match = False

values_file = None

from_date = datetime.strptime("2005-01-01", "%Y-%m-%d")

to_date = datetime.strptime("2030-12-31", "%Y-%m-%d")

########################
########################
########################



# Configurar el logging para la consola y para un archivo

log = logging.getLogger("bot")
log.setLevel(logging.INFO)
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
log_str_handler = logging.StreamHandler()
log_str_handler.setFormatter(log_formatter)
log.addHandler(log_str_handler)
if not os.path.exists("logs"):
	os.makedirs("logs")
log_file_handler = logging.handlers.RotatingFileHandler(os.path.join("logs", "bot.log"), maxBytes=1024*1024*16, backupCount=5)
log_file_handler.setFormatter(log_formatter)
log.addHandler(log_file_handler)

# Función para escribir una línea en un archivo comprimido zst

def write_line_zst(handle, line):
	handle.write(line.encode('utf-8'))
	handle.write("\n".encode('utf-8'))

# Función para escribir una línea en formato json

def write_line_json(handle, obj):
	handle.write(json.dumps(obj))
	handle.write("\n")

# Función para escribir una sola línea en el campo especificado

def write_line_single(handle, obj, field):
	if field in obj:
		handle.write(obj[field])
	else:
		log.info(f"{field} not in object {obj['id']}")
	handle.write("\n")

# Función para escribir una línea en formato csv

def write_line_csv(writer, obj, is_submission):
	output_list = []
	output_list.append(str(obj['score']))
	output_list.append(datetime.fromtimestamp(int(obj['created_utc'])).strftime("%Y-%m-%d"))
	if is_submission:
		output_list.append(obj['title'])
	output_list.append(f"u/{obj['author']}")
	output_list.append(f"https://www.reddit.com{obj['permalink']}")
	if is_submission:
		if obj['is_self']:
			if 'selftext' in obj:
				output_list.append(obj['selftext'])
			else:
				output_list.append("")
		else:
			output_list.append(obj['url'])
	else:
		output_list.append(obj['body'])
	writer.writerow(output_list)

# Función para leer y decodificar un archivo en fragmentos

def read_and_decode(reader, chunk_size, max_window_size, previous_chunk=None, bytes_read=0):
	chunk = reader.read(chunk_size)
	bytes_read += chunk_size
	if previous_chunk is not None:
		chunk = previous_chunk + chunk
	try:
		return chunk.decode()
	except UnicodeDecodeError:
		if bytes_read > max_window_size:
			raise UnicodeError(f"Unable to decode frame after reading {bytes_read:,} bytes")
		log.info(f"Decoding error with {bytes_read:,} bytes, reading another chunk")
		return read_and_decode(reader, chunk_size, max_window_size, chunk, bytes_read)

# Función para leer líneas de un archivo comprimido zst

def read_lines_zst(file_name):
	with open(file_name, 'rb') as file_handle:
		buffer = ''
		reader = zstandard.ZstdDecompressor(max_window_size=2**31).stream_reader(file_handle)
		while True:
			chunk = read_and_decode(reader, 2**27, (2**29) * 2)

			if not chunk:
				break
			lines = (buffer + chunk).split("\n")

			for line in lines[:-1]:
				yield line.strip(), file_handle.tell()

			buffer = lines[-1]

		reader.close()

# Función para procesar el archivo de entrada y generar el archivo de salida en el formato especificado

def process_file(input_file, output_file, output_format, field, values, from_date, to_date, single_field, exact_match):
	output_path = f"{output_file}.{output_format}"
	is_submission = "submission" in input_file
	log.info(f"Input: {input_file} : Output: {output_path} : Is submission {is_submission}")
	writer = None
	if output_format == "zst":
		handle = zstandard.ZstdCompressor().stream_writer(open(output_path, 'wb'))
	elif output_format == "txt":
		handle = open(output_path, 'w', encoding='UTF-8')
	elif output_format == "csv":
		handle = open(output_path, 'w', encoding='UTF-8', newline='')
		writer = csv.writer(handle)
	else:
		log.error(f"Unsupported output format {output_format}")
		sys.exit()

	file_size = os.stat(input_file).st_size
	created = None
	matched_lines = 0
	bad_lines = 0
	total_lines = 0
	for line, file_bytes_processed in read_lines_zst(input_file):
		total_lines += 1
		if total_lines % 100000 == 0:
			log.info(f"{created.strftime('%Y-%m-%d %H:%M:%S')} : {total_lines:,} : {matched_lines:,} : {bad_lines:,} : {file_bytes_processed:,}:{(file_bytes_processed / file_size) * 100:.0f}%")

		try:
			obj = json.loads(line)
			created = datetime.utcfromtimestamp(int(obj['created_utc']))

			if created < from_date:
				continue
			if created > to_date:
				continue

			if field is not None:
				field_value = obj[field].lower()
				matched = False
				for value in values:
					if exact_match:
						if value == field_value:
							matched = True
							break
					else:
						if value in field_value:
							matched = True
							break
				if not matched:
					continue

			matched_lines += 1
			if output_format == "zst":
				write_line_zst(handle, line)
			elif output_format == "csv":
				write_line_csv(writer, obj, is_submission)
			elif output_format == "txt":
				if single_field is not None:
					write_line_single(handle, obj, single_field)
				else:
					write_line_json(handle, obj)
			else:
				log.info(f"Something went wrong, invalid output format {output_format}")
		except (KeyError, json.JSONDecodeError) as err:
			bad_lines += 1
			if write_bad_lines:
				if isinstance(err, KeyError):
					log.warning(f"Key {field} is not in the object: {err}")
				elif isinstance(err, json.JSONDecodeError):
					log.warning(f"Line decoding failed: {err}")
				log.warning(line)

	handle.close()
	log.info(f"Complete : {total_lines:,} : {matched_lines:,} : {bad_lines:,}")

# Función principal

if __name__ == "__main__":
	if single_field is not None:
		log.info("Single field output mode, changing output file format to txt")
		output_format = "txt"

	if values_file is not None:
		values = []
		with open(values_file, 'r') as values_handle:
			for value in values_handle:
				values.append(value.strip().lower())
		log.info(f"Loaded {len(values)} from values file {values_file}")
	else:
		values = [value.lower() for value in values]  # convert to lowercase

	log.info(f"Filtering field: {field}")
	if len(values) <= 20:
		log.info(f"On values: {','.join(values)}")
	else:
		log.info(f"On values:")
		for value in values:
			log.info(value)
	log.info(f"Exact match {('on' if exact_match else 'off')}. Single field {single_field}.")
	log.info(f"From date {from_date.strftime('%Y-%m-%d')} to date {to_date.strftime('%Y-%m-%d')}")
	log.info(f"Output format set to {output_format}")

	input_files = []
	if os.path.isdir(input_file):
		if not os.path.exists(output_file):
			os.makedirs(output_file)
		for file in os.listdir(input_file):
			if not os.path.isdir(file) and file.endswith(".zst"):
				input_name = os.path.splitext(os.path.splitext(os.path.basename(file))[0])[0]
				input_files.append((os.path.join(input_file, file), os.path.join(output_file, input_name)))
	else:
		input_files.append((input_file, output_file))
	log.info(f"Processing {len(input_files)} files")
	for file_in, file_out in input_files:
		process_file(file_in, file_out, output_format, field, values, from_date, to_date, single_field, exact_match)
