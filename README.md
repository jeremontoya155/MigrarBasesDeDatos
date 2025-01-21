<h1>Migración de Bases de Datos PostgreSQL</h1>

 <h2>Descripción</h2>
  <p>Esta herramienta permite la migración de datos y estructuras de tablas entre dos bases de datos PostgreSQL. Es especialmente útil para mover datos de una base de datos en Railway a otra base de datos destino, preservando relaciones y manejando tablas largas.</p>

  <h2>Características</h2>
  <ul>
      <li><strong>Migración completa de tablas:</strong> Se copian tanto la estructura como los datos.</li>
      <li><strong>Soporte para tablas largas:</strong> Los datos se transfieren en bloques para evitar problemas de memoria.</li>
      <li><strong>Validación de existencia:</strong> Si una tabla ya existe en el destino, se omite su creación.</li>
      <li><strong>Interfaz gráfica simple:</strong> Implementada con Tkinter para facilitar la configuración.</li>
  </ul>

  <h2>Requisitos</h2>

  <h3>Software necesario</h3>
  <ul>
      <li>Python 3.7 o superior</li>
      <li>Bibliotecas de Python:
          <ul>
              <li>psycopg2</li>
              <li>tkinter</li>
          </ul>
      </li>
  </ul>

  <h3>Base de datos</h3>
  <ul>
      <li>Dos instancias de PostgreSQL configuradas (origen y destino).</li>
  </ul>

  <h2>Instalación</h2>

  <h3>Paso 1: Clonar el repositorio</h3>
  <pre>
      <code>
git clone https://github.com/tuusuario/migracion-postgresql.git
cd migracion-postgresql
      </code>
  </pre>

  <h3>Paso 2: Instalar dependencias</h3>
  <p>Asegúrate de tener <code>pip</code> instalado y luego ejecuta:</p>
  <pre>
      <code>
pip install psycopg2
      </code>
  </pre>

  <h2>Uso</h2>

  <h3>Paso 1: Ejecutar la aplicación</h3>
  <pre>
      <code>
python migracion.py
      </code>
  </pre>

  <h3>Paso 2: Configurar las conexiones</h3>
  <ol>
      <li>Ingresa los detalles de la base de datos de <strong>origen</strong> (Railway): 
          <ul>
              <li>Host</li>
              <li>Puerto</li>
              <li>Base de datos</li>
              <li>Usuario</li>
              <li>Contraseña</li>
          </ul>
      </li>
      <li>Ingresa los detalles de la base de datos de <strong>destino</strong>:
          <ul>
              <li>Host</li>
              <li>Puerto</li>
              <li>Base de datos</li>
              <li>Usuario</li>
              <li>Contraseña</li>
          </ul>
      </li>
  </ol>

  <h3>Paso 3: Iniciar la migración</h3>
  <p>Haz clic en el botón <strong>Iniciar Migración</strong>. Si todo está configurado correctamente:</p>
  <ul>
      <li>Las tablas y sus datos serán migrados.</li>
      <li>Un mensaje de éxito aparecerá al finalizar.</li>
  </ul>

  <h2>Funcionalidades avanzadas</h2>

  <h3>Manejo de tablas largas</h3>
  <p>Los datos se transfieren en bloques de 1000 registros para evitar problemas de memoria y tiempos de espera excesivos.</p>

  <h3>Preservación de relaciones</h3>
  <p>La migración sigue un orden lógico para evitar problemas de dependencias entre tablas relacionadas.</p>

  <h3>Validación</h3>
  <p>Si una tabla ya existe en la base de datos destino, no se crea nuevamente.</p>

  <h2>Errores comunes y soluciones</h2>

  <h3>Error de conexión</h3>
  <p>Si recibes un error relacionado con la conexión, verifica:</p>
  <ul>
      <li>Las credenciales de las bases de datos (usuario, contraseña).</li>
      <li>La configuración de red y puertos (asegúrate de que sean accesibles).</li>
  </ul>

  <h3>Error de permisos</h3>
  <p>Si una tabla no puede ser creada, verifica:</p>
  <ul>
      <li>Los permisos del usuario de la base de datos destino.</li>
  </ul>

  <h2>Contribuciones</h2>
  <p>Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request con mejoras.</p>

  <h2>Licencia</h2>
  <p>Este proyecto está bajo la licencia MIT. Para más detalles, revisa el archivo <code>LICENSE</code>.</p>
