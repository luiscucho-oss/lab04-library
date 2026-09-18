# Lab 04 - Biblioteca: Modelos y Relaciones en Django

## Descripcion

Proyecto de laboratorio que implementa un sistema de gestion de biblioteca utilizando Django, demostrando el uso de modelos, migraciones y diferentes tipos de relaciones (ForeignKey, OneToOneField, ManyToManyField y modelo intermedio).

## Diagrama de Modelos

```
┌──────────────────┐       ┌──────────────────────┐
│     Category     │       │      Publisher       │
├──────────────────┤       ├──────────────────────┤
│ name             │       │ name                 │
│ description      │       │ address              │
└────────┬─────────┘       │ city                 │
         │                 │ website              │
         │ M2M             └──────────┬───────────┘
         │                            │
         │     ┌──────────────────────┤
         │     │                      │
┌────────▼─────┴───┐    ┌────────────▼──────────┐
│       Book        │    │     Publication       │
├───────────────────┤    │  (Modelo Intermedio)  │
│ title             │    ├───────────────────────┤
│ author (FK) ──┐   │    │ book (FK)             │
│ isbn          │   │    │ publisher (FK)        │
│ pages         │   │    │ publication_date      │
│ cover         │   │    │ edition               │
│ language      │   │    └───────────────────────┘
│ publication_date  │    │
│ categories (M2M)──┘    │
└───────────┬────────────┘
            │
            │ FK (on_delete=CASCADE)
            │
┌───────────▼────────────┐    ┌──────────────────────┐
│       Author           │    │    AuthorProfile     │
├────────────────────────┤    ├──────────────────────┤
│ first_name             │◄───│ author (OneToOne)    │
│ last_name              │    │ biography            │
│ email                  │    │ birth_place          │
│ bio                    │    │ photo                │
│ date_of_birth          │    └──────────────────────┘
└────────────────────────┘
```

## Tipos de Relaciones Implementadas

| Relacion | Tipo | Modelo | Descripcion |
|----------|------|--------|-------------|
| Book - Author | ForeignKey | Book.author | Un autor tiene muchos libros (CASCADE) |
| Book - AuthorProfile | OneToOneField | AuthorProfile.author | Un autor tiene un perfil biografico |
| Book - Category | ManyToManyField | Book.categories | Un libro puede tener muchas categorias |
| Book - Publisher | ManyToManyField (intermedio) | Publication | Relacion con fecha y edicion |

## Capturas de Pantalla

### Panel de Administrador
<img width="1888" height="908" alt="Captura de pantalla 2026-09-17 212806" src="https://github.com/user-attachments/assets/23f1c1a7-0e43-4ba9-ad8b-a3bfbbce85b8" />


### Lista de Libros
<img width="1579" height="948" alt="Captura de pantalla 2026-09-17 213206" src="https://github.com/user-attachments/assets/21ebfe53-1c80-48ca-ae2e-d945d02d7eef" />


### Detalle de Libro con Datos Relacionados

<img width="1857" height="946" alt="Captura de pantalla 2026-09-17 213032" src="https://github.com/user-attachments/assets/14546ad2-30c5-4b0b-9732-b30d0bca3325" />


## Instalacion

```bash
# Clonar el repositorio
git clone https://github.com/luiscucho-oss/lab04-library.git
cd lab04-library

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar el servidor
python manage.py runserver
```

## Datos de Prueba

- **Autores:** Gabriel Garcia Marquez, Isabel Allende
- **Libros:** Cien anos de soledad, El amor en los tiempos del colera, La casa de los espiritus, Paula
- **Categorias:** Ficcion, Novela, Clasico
- **Editoriales:** Planeta, Anagrama

## Consultas Realizadas

### Consultas de Ida (Forward)
```python
libro = Book.objects.first()
libro.author                    # ForeignKey -> Author
libro.categories.all()          # ManyToMany -> Category
libro.publication_set.all()     # Reverse -> Publication
```

### Consultas de Vuelta (Reverse)
```python
autor = Author.objects.first()
autor.books.all()               # related_name='books'
autor.profile.biography         # OneToOne -> AuthorProfile
```

### Filtros con Doble Guion Bajo
```python
Book.objects.filter(author__last_name="Garcia Marquez")
Book.objects.filter(categories__name="Ficcion")
Book.objects.filter(publication__publisher__name="Planeta")
Author.objects.filter(books__title__contains="amor")
```

## Comportamiento de Borrado

| Configuracion | Comportamiento |
|---------------|----------------|
| `on_delete=CASCADE` | Borrar un autor elimina tambien todos sus libros |
| `on_delete=PROTECT` | Borrar un autor con libros lanza `ProtectedError` |

## Credenciales de Admin

- **Usuario:** admin
- **Contrasena:** admin123

## Tecnologias

- Django 6.1.1
- Pillow 12.3.0 (para campos de imagen)
- SQLite (base de datos)

## Observaciones

1. **Estructura del proyecto:** Se utilizo la estructura estandar de Django con el proyecto llamado "biblioteca" y la aplicacion "library", separando la configuracion del proyecto de la logica de la aplicacion.

2. **Pillow:** Se instalo la libreria Pillow para soportar campos `ImageField` en los modelos `Book` (portada) y `AuthorProfile` (foto), necesaria para el manejo de imagenes en Django.

3. **related_name:** Se definio `related_name='books'` en la ForeignKey de Book hacia Author, lo que permite acceder a los libros de un autor de forma intuitiva con `autor.books.all()`.

4. **Modelo intermedio Publication:** Se opto por un modelo intermedio explicito en lugar de un ManyToManyField simple para poder almacenar `publication_date` y `edition`, datos que dependen de la relacion entre libro y editorial.

5. **OneToOneField para perfil:** Se separo la informacion biografica del autor en un modelo `AuthorProfile` usando OneToOneField, siguiendo el patron de separar datos personales de datos biograficos, permitiendo que el perfil sea opcional.

6. **Datos de prueba:** Se cargaron datos reales de autores latinoamericanos (Garcia Marquez y Allende) para facilitar la comprension de las relaciones y las consultas.

7. **Serializacion de consultas:** Las consultas con doble guion bajo (`__`) permiten recorrer relaciones sin necesidad de hacer multiples queries, optimizando el rendimiento de la base de datos.

## Conclusiones

1. **Relaciones en Django:** Se implementaron los cuatro tipos principales de relaciones entre modelos: ForeignKey (Book-Author), OneToOneField (Author-AuthorProfile), ManyToManyField automatica (Book-Category) y ManyToManyField con modelo intermedio (Book-Publisher via Publication).

2. **on_delete:** Se comprobo que `CASCADE` elimina en cascada los registros dependientes, mientras que `PROTECT` lanza una excepcion `ProtectedError` impidiendo el borrado. La eleccion correcta depende de la logica del negocio.

3. **Consultas ORM:** Django permite navebar relaciones de ida (`libro.author`) y de vuelta (`autor.books.all()`) de forma sencilla. Los filtros con doble guion bajo (`__`) permiten consultas complejas como `Book.objects.filter(author__last_name="Garcia Marquez")`.

4. **Modelo intermedio:** Usar un modelo intermedio (`Publication`) en lugar de un `ManyToManyField` simple permite guardar datos adicionales como `publication_date` y `edition` en la relacion entre libros y editoriales.

5. **Migraciones:** El sistema de migraciones de Django genera automaticamente las tablas necesarias, incluyendo las tablas intermedias para relaciones ManyToMany, manteniendo la base de datos sincronizada con los modelos.

6. **Admin:** El panel de administracion de Django permite gestionar rapidamente los datos de prueba, facilitando la verificacion de las relaciones y el comportamiento de la aplicacion.
