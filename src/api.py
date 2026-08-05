import os

import requests
from dotenv import load_dotenv

load_dotenv()

class APIClient:
    """
    Cliente para interactuar con la API de FIUNI.
    Permite obtener materias y asistencias del estudiante y devolver los datos como respuesta JSON.
    """
    def __init__(self, email, password):
        """
        Inicializa el cliente de la API configurando el token de autorización,
        los encabezados, la URL base y la carga útil predeterminada para las
        solicitudes a la API.
        Args:
            email (str): Email del estudiante para iniciar sesión.
            password (str): Contraseña del estudiante para iniciar sesión.
            base_url (str): URL base de la API.
        Raises:
            ValueError: Si las credenciales o la URL base no se proporcionan.
        """

        if not email or not password:
            raise ValueError("Las credenciales de inicio de sesión no pueden estar vacías")

        self._base_url = os.getenv("BASE_URL_INTEGRALFIUNI")
        
        if not self._base_url:
            raise ValueError("La URL base de la API no puede estar vacía")

        
        self._token = self.__get_token(email, password)

        self._headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json"
        }
        
        self._default_payload = {
            "page": 1,
            "pageSize": 25,
            "filters": {}
        }

    def __get_token(self, email, password):
        endpoint = "usuarios/login"
        url = self._base_url + endpoint

        payload = {"email": email, "password": password, "loggingIn": False}

        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        return response.json().get("token")

    def __check_response(self, response):
        """
        Verifica que la respuesta HTTP sea exitosa y devuelve su contenido JSON.
        Args:
            response (requests.Response): El objeto de respuesta HTTP que contiene los datos JSON.
        Returns:
            dict: El contenido JSON de la respuesta.
        Raises:
            requests.exceptions.HTTPError: Si la respuesta HTTP contiene un código de estado de error.
        """
        response.raise_for_status()
        return response.json()

    def fetch_subjects(self):
        """
        Obtiene datos sobre todas las materias asociadas con el estudiante.
        Este método envía una solicitud POST al endpoint "studentsubjects/all-my-subjects" 
        de la API para recuperar información sobre las materias del estudiante.
        Retorna:
            dict: Los datos JSON de la respuesta con las materias del estudiante.
        Raises:
            requests.exceptions.HTTPError: Si la respuesta HTTP contiene un código de estado de error.
        """
        
        endpoint = "studentsubjects/all-my-subjects"
        url = self._base_url + endpoint

        response = requests.post(url, headers=self._headers, json={})
        return self.__check_response(response)

    def fetch_favorite_subjects(self):
        """
        Obtiene datos sobre las materias favoritas del estudiante.
        Este método envía una solicitud GET al endpoint "MateriasPeriodo/materias-tablero-alumno" 
        de la API para recuperar información sobre las materias favoritas del estudiante.
        Returns:
            dict: Los datos JSON de la respuesta con las materias favoritas del estudiante.
        Raises:
            requests.exceptions.HTTPError: Si la respuesta HTTP contiene un código de estado de error.
        """

        endpoint = "MateriasPeriodo/materias-tablero-alumno"
        url = self._base_url + endpoint

        response = requests.get(url, headers=self._headers)
        return self.__check_response(response)

    def fetch_assistance_data(self, subject_id):
        """
        Obtiene datos de asistencias para una materia específica.
        Este método envía una solicitud POST a la API para recuperar datos de asistencias
        asociados con el ID de la materia proporcionado.
        Args:
            subject_id (str): El ID de la materia para la cual se obtendrán los datos de asistencias.
                              No debe estar vacío.
        Returns:
            dict: Los datos JSON de la respuesta con las asistencias de la materia.
        Raises:
            ValueError: Si el `subject_id` está vacío.
            requests.exceptions.HTTPError: Si la respuesta HTTP contiene un código de estado de error.
        """

        if not subject_id:
            raise ValueError("El id de la materia no puede estar vacío")

        endpoint = f"assistances/{subject_id}/my"
        url = self._base_url + endpoint

        response = requests.post(url, headers=self._headers, json=self._default_payload)
        return self.__check_response(response)

    def fetch_homework_data(self, subject_id):
        """
        Obtiene datos de tareas para una materia específica.
        Este método envía una solicitud POST a la API para recuperar datos de tareas
        asociados con el ID de la materia proporcionado.
        Args:
            subject_id (str): El ID de la materia para la cual se obtendrán los datos de tareas.
                              No debe estar vacío.
        Returns:
            dict: Los datos JSON de la respuesta con las tareas de la materia.
        Raises:
            ValueError: Si el `subject_id` está vacío.
            requests.exceptions.HTTPError: Si la respuesta HTTP contiene un código de estado de error.
        """
        if not subject_id:
            raise ValueError("El id de la materia no puede estar vacío")
        
        endpoint = f"MateriasPeriodo/{subject_id}/homework/my"
        url = self._base_url + endpoint

        response = requests.post(url, headers=self._headers, json=self._default_payload)
        return self.__check_response(response)
    
    def fetch_derecho_examen_data(self):
        """
        Obtiene datos sobre los derechos a exámenes del estudiante.
        Este método envía una solicitud POST al endpoint "studentsubjects/mis_derechos_a_examenes" 
        de la API para recuperar información sobre los exámenes a los que el estudiante tiene derecho.
        Returns:
            dict: Los datos JSON de la respuesta con los derechos a exámenes del estudiante.
        Raises:
            requests.exceptions.HTTPError: Si la respuesta HTTP contiene un código de estado de error.
        """
        endpoint = "studentsubjects/mis_derechos_a_examenes"
        url = self._base_url + endpoint

        response = requests.post(url, headers=self._headers, json=self._default_payload)
        return self.__check_response(response)

    def fetch_exam_data(self):
        """
        Obtiene datos sobre los exámenes del estudiante.
        Este método envía una solicitud POST al endpoint "inscripcionexamen/my-exams" 
        de la API para recuperar información sobre los exámenes en los que el estudiante está inscrito.
        Returns:
            dict: Los datos JSON de la respuesta con los exámenes del estudiante.
        Raises:
            requests.exceptions.HTTPError: Si la respuesta HTTP contiene un código de estado de error.
        """
        endpoint = "inscripcionexamen/my-exams"
        url = self._base_url + endpoint

        response = requests.post(url, headers=self._headers, json={})
        return self.__check_response(response)

    def enroll_exam(self, id_exam):
        """
        Inscribe al estudiante en un examen específico.
        Este método obtiene los derechos a exámenes del estudiante y luego envía una solicitud 
        POST para inscribir al estudiante en el examen con el ID proporcionado.
        Args:
            id_exam (str): El ID del examen en el cual se desea inscribir al estudiante.
                           No debe estar vacío.
        Returns:
            bool: True si la inscripción fue exitosa (código de estado 200), False en caso contrario.
        Raises:
            ValueError: Si el `id_exam` está vacío o si no se pueden obtener los derechos a exámenes.
        """
        if not id_exam:
            raise ValueError("El id del examen no puede estar vacío")

        exams = self.fetch_derecho_examen_data()

        # Si no existen examenes, no se puede inscribir
        if exams["items"] == []:
            return False
        
        student_id = exams.get("items", [{}])[0].get("studentId")

        endpoint = f"inscripcionexamen/inscribirme"
        url = self._base_url + endpoint

        payload = {
            "examenId": int(id_exam),
            "id" : 0,
            "perfilAlumnoId": student_id,
            "calificacon": 0
        }

        response = requests.post(url, headers=self._headers, json=payload)
        return response.status_code == 200
    
    def enroll_all_exams(self):
        """
        Inscribe al estudiante en todos los exámenes disponibles.
        Este método obtiene la lista de exámenes a los que el estudiante tiene derecho
        y procede a inscribirlo en cada uno de ellos automáticamente.
        Returns:
            list: Una lista de diccionarios con los resultados de cada inscripción.
                  Cada diccionario contiene:
                  - "materia": El nombre de la materia
                  - "id": El ID del examen
                  - "success": True si la inscripción fue exitosa, False en caso contrario
        Raises:
            requests.exceptions.HTTPError: Si no se pueden obtener los derechos a exámenes.
        """
        exams = self.fetch_derecho_examen_data()
        exam_items = exams.get("items", [])
        results = []

        for exam in exam_items:
            exam_id = exam.get("examenId")
            if exam_id:
                result = self.enroll_exam(exam_id)
                results.append({
                    "materia": exam.get("materia"),
                    "id": exam_id, 
                    "success": result})
        
        return results
