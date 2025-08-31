# INFO278-SistemasDeInformacion
Sistema de información para que alumnos puedan crear su plan de estudio personalizado según las asignaturas cursadas que tienen.


# pasos
porfavor hacer 
sis_info\Scripts\activate
para el entorno
e instalar requirements
# Estructura

.
├── academic_path_finder/
│   ├── __init__.py
│   ├── data_handler/
│   │   ├── __init__.py
│   │   └── json_loader.py
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── shortest_path.py
│   │   └── alternative_routes.py
│   ├── data/
│   │   └── academic_graph.json  <- Aquí va el archivo JSON
│   └── utils/
│       ├── __init__.py
│       └── custom_exceptions.py
├── tests/
│   ├── test_data_handler.py
│   └── test_analysis.py
├── notebooks/
│   └── exploration.ipynb
├── .gitignore
├── requirements.txt
└── README.md