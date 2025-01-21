import psycopg2
from psycopg2 import sql
from tkinter import Tk, Label, Entry, Button, messagebox

def migrate_data(railway_conn, dest_conn):
    conn_railway = None
    conn_dest = None
    railway_cursor = None
    dest_cursor = None

    try:
        # Conexiones a las bases de datos
        conn_railway = psycopg2.connect(**railway_conn)
        conn_dest = psycopg2.connect(**dest_conn)
        railway_cursor = conn_railway.cursor()
        dest_cursor = conn_dest.cursor()

        # Obtener las tablas de la base de datos de origen
        railway_cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tables = [table[0] for table in railway_cursor.fetchall()]

        for table_name in tables:
            try:
                # Verificar si la tabla ya existe en la base de datos destino
                dest_cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = %s AND table_schema = 'public'
                    );
                """, (table_name,))
                if dest_cursor.fetchone()[0]:
                    print(f"La tabla {table_name} ya existe. Saltando creación.")
                    continue

                # Obtener la definición de la tabla
                railway_cursor.execute("""
                    SELECT column_name, data_type, character_maximum_length 
                    FROM information_schema.columns 
                    WHERE table_name = %s;
                """, (table_name,))
                columns = railway_cursor.fetchall()

                # Crear la tabla en la base de datos de destino
                create_table_query = sql.SQL("CREATE TABLE {} (").format(sql.Identifier(table_name))
                for col_name, col_type, col_length in columns:
                    if col_length:
                        col_type = f"{col_type}({col_length})"
                    create_table_query += sql.SQL("{} {}, ").format(
                        sql.Identifier(col_name),
                        sql.SQL(col_type)
                    )
                create_table_query = create_table_query.rstrip(sql.SQL(", ")) + sql.SQL(");")
                dest_cursor.execute(create_table_query)
                conn_dest.commit()
                print(f"Tabla {table_name} creada exitosamente.")

                # Copiar los datos de la tabla en bloques
                railway_cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                total_rows = railway_cursor.fetchone()[0]
                batch_size = 1000  # Tamaño del bloque
                for offset in range(0, total_rows, batch_size):
                    railway_cursor.execute(
                        sql.SQL("SELECT * FROM {} LIMIT %s OFFSET %s;").format(sql.Identifier(table_name)),
                        (batch_size, offset)
                    )
                    rows = railway_cursor.fetchall()
                    for row in rows:
                        placeholders = ', '.join(['%s'] * len(row))
                        insert_query = sql.SQL("INSERT INTO {} VALUES ({})").format(
                            sql.Identifier(table_name),
                            sql.SQL(placeholders)
                        )
                        dest_cursor.execute(insert_query, row)
                    conn_dest.commit()
                print(f"Datos de {table_name} migrados exitosamente.")

            except Exception as e:
                print(f"Error migrando la tabla {table_name}: {e}")

        messagebox.showinfo("Éxito", "Migración completada con éxito.")
    except Exception as e:
        messagebox.showerror("Error", f"Error general durante la migración: {e}")
    finally:
        # Verificar antes de cerrar
        if railway_cursor:
            railway_cursor.close()
        if dest_cursor:
            dest_cursor.close()
        if conn_railway:
            conn_railway.close()
        if conn_dest:
            conn_dest.close()

def start_migration():
    # Leer datos del formulario
    railway_conn = {
        "host": entry_host_railway.get(),
        "port": entry_port_railway.get(),
        "database": entry_db_railway.get(),
        "user": entry_user_railway.get(),
        "password": entry_pass_railway.get(),
    }

    dest_conn = {
        "host": entry_host_dest.get(),
        "port": entry_port_dest.get(),
        "database": entry_db_dest.get(),
        "user": entry_user_dest.get(),
        "password": entry_pass_dest.get(),
    }

    migrate_data(railway_conn, dest_conn)

# Crear ventana principal
root = Tk()
root.title("Migración de Bases de Datos PostgreSQL")

# Etiquetas y campos para la base de datos de origen
Label(root, text="Base de datos de origen (Railway)").grid(row=0, column=0, columnspan=2)
Label(root, text="Host:").grid(row=1, column=0)
entry_host_railway = Entry(root, width=30)
entry_host_railway.grid(row=1, column=1)

Label(root, text="Port:").grid(row=2, column=0)
entry_port_railway = Entry(root, width=30)
entry_port_railway.grid(row=2, column=1)

Label(root, text="Database:").grid(row=3, column=0)
entry_db_railway = Entry(root, width=30)
entry_db_railway.grid(row=3, column=1)

Label(root, text="User:").grid(row=4, column=0)
entry_user_railway = Entry(root, width=30)
entry_user_railway.grid(row=4, column=1)

Label(root, text="Password:").grid(row=5, column=0)
entry_pass_railway = Entry(root, width=30, show="*")
entry_pass_railway.grid(row=5, column=1)

# Etiquetas y campos para la base de datos de destino
Label(root, text="Base de datos de destino").grid(row=6, column=0, columnspan=2)
Label(root, text="Host:").grid(row=7, column=0)
entry_host_dest = Entry(root, width=30)
entry_host_dest.grid(row=7, column=1)

Label(root, text="Port:").grid(row=8, column=0)
entry_port_dest = Entry(root, width=30)
entry_port_dest.grid(row=8, column=1)

Label(root, text="Database:").grid(row=9, column=0)
entry_db_dest = Entry(root, width=30)
entry_db_dest.grid(row=9, column=1)

Label(root, text="User:").grid(row=10, column=0)
entry_user_dest = Entry(root, width=30)
entry_user_dest.grid(row=10, column=1)

Label(root, text="Password:").grid(row=11, column=0)
entry_pass_dest = Entry(root, width=30, show="*")
entry_pass_dest.grid(row=11, column=1)

# Botón para iniciar la migración
Button(root, text="Iniciar Migración", command=start_migration).grid(row=12, column=0, columnspan=2)

# Iniciar el loop de la aplicación
root.mainloop()
