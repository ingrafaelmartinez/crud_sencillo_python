import os
import pymysql

DROP_TABLE_USERS = " DROP TABLE IF EXISTS users "

USERS_TABLE = """ CREATE TABLE users(
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)"""


def system_clear(function):
    def wrapper(conexion, cursor):
        
        os.system("clear")

        function(conexion, cursor)

        input("")

        os.system("clear")
    
    wrapper.__doc__ = function.__doc__
    return wrapper


@system_clear
def create_user(conexion, cursor):
    """A) Crear usuario"""
    
    username = input("Ingresa un username: ")
    email = input("Ingresa un email: ")

    query = "INSERT INTO users(username, email) VALUES(%s, %s)"
    values = (username, email)

    cursor.execute(query, values)
    conexion.commit()

    print(">>> Usuario creado \n")


@system_clear
def list_user(conexion, cursor):
    """B) Listar usuarios"""

    query = "SELECT id, username, email FROM users"
    cursor.execute(query)

    for id, username, email in cursor.fetchall():
        print(id, '-', username, '-', email)
    
    print("Listado de usuarios \n")


def user_exists(function):

    def wrapper(conexion, cursor):
        id = input("Ingrese el id del usuario: ")
        query = "SELECT id FROM users WHERE id = %s"
        cursor.execute(query, (id,))

        user = cursor.fetchone()
        if user:
            function(id, conexion, cursor)
        else:
            print("No existe un usuario con ese id. Intente nuevamente.")
    
    wrapper.__doc__ = function.__doc__
    return wrapper


@system_clear
@user_exists
def update_user(id, conexion, cursor):
    """C) Actualizar usuario"""
    
    
    username = input("Ingrese un nuevo username: ")
    email = input("Ingrese un nuevo email: ")

    query = "UPDATE users SET username = %s, email = %s WHERE id = %s"
    values = (username, email, id)

    cursor.execute(query, values)
    conexion.commit()

    print(">>> Usuario actualizado correctamente. \n")


@system_clear
@user_exists
def delete_user(id, conexion, cursor):
    """D) Eliminar usuario"""

    query = "DELETE FROM users WHERE id = %s"

    cursor.execute(query, (id,))
    conexion.commit()

    print(">>> Usuario eliminado exitosamente \n")


def default(*args):
    print("¡Opción no válida!")

if __name__ == '__main__':

    options = {
        'a': create_user,
        'b': list_user,
        'c': update_user,
        'd': delete_user
    }
    
    try:
        conexion = pymysql.Connect(host='localhost', port=3306, user='root', passwd='', db='python_db')

        with conexion.cursor() as cursor:
            # cursor.execute(DROP_TABLE_USERS)
            # cursor.execute(USERS_TABLE)

            while True:
                for function in options.values():
                    print(function.__doc__)
                
                print("quit para salir")

                option = input("Selecciona una opción válida: ").lower()

                if option == "quit" or option == "q":
                    break

                function = options.get(option, default)
                function(conexion, cursor)

    except pymysql.err.OperationalError as err:
        print("No fue posible realizar la conexión")
        print(err)

    # finally:
    #     conexion.close()
    #     print("Conexión finalizada de forma exitosa")