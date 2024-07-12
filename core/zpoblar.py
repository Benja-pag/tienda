import os
import sqlite3
from django.contrib.auth.models import User, Permission
from django.db import connection
from datetime import date, timedelta
from random import randint
from core.models import Categoria, Producto, Carrito, Perfil, Boleta, DetalleBoleta, Bodega

def eliminar_tabla(nombre_tabla):
    conexion = sqlite3.connect('db.sqlite3')
    cursor = conexion.cursor()
    cursor.execute(f"DELETE FROM {nombre_tabla}")
    conexion.commit()
    conexion.close()

def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def crear_usuario(username, tipo, nombre, apellido, correo, es_superusuario, 
    es_staff, rut, direccion, subscrito, imagen):

    try:
        print(f'Verificar si existe usuario {username}.')

        if User.objects.filter(username=username).exists():
            print(f'   Eliminar {username}')
            User.objects.get(username=username).delete()
            print(f'   Eliminado {username}')
        
        print(f'Iniciando creación de usuario {username}.')

        usuario = None
        if tipo == 'Superusuario':
            print('    Crear Superuser')
            usuario = User.objects.create_superuser(username=username, password='123')
        else:
            print('    Crear User')
            usuario = User.objects.create_user(username=username, password='123')

        if tipo == 'Administrador':
            print('    Es administrador')
            usuario.is_staff = es_staff
            
        usuario.first_name = nombre
        usuario.last_name = apellido
        usuario.email = correo
        usuario.save()

        if tipo == 'Administrador':
            print(f'    Dar permisos a core y apirest')
            permisos = Permission.objects.filter(content_type__app_label__in=['core', 'apirest'])
            usuario.user_permissions.set(permisos)
            usuario.save()

        print(f'    Crear perfil: RUT {rut}, Subscrito {subscrito}, Imagen {imagen}')
        Perfil.objects.create(
            usuario=usuario, 
            tipo_usuario=tipo,
            rut=rut,
            direccion=direccion,
            subscrito=subscrito,
            imagen=imagen)
        print("    Creado correctamente")
    except Exception as err:
        print(f"    Error: {err}")

def eliminar_tablas():
    eliminar_tabla('auth_user_groups')
    eliminar_tabla('auth_user_user_permissions')
    eliminar_tabla('auth_group_permissions')
    eliminar_tabla('auth_group')
    eliminar_tabla('auth_permission')
    eliminar_tabla('django_admin_log')
    eliminar_tabla('django_content_type')
    #eliminar_tabla('django_migrations')
    eliminar_tabla('django_session')
    eliminar_tabla('Bodega')
    eliminar_tabla('DetalleBoleta')
    eliminar_tabla('Boleta')
    eliminar_tabla('Perfil')
    eliminar_tabla('Carrito')
    eliminar_tabla('Producto')
    eliminar_tabla('Categoria')
    #eliminar_tabla('authtoken_token')
    eliminar_tabla('auth_user')

def poblar_bd(test_user_email=''):
    eliminar_tablas()

    #nuevos usuarios
    #modificar despues
    #ahora ver los problemas con las imagenes
    crear_usuario(
        username='jperez',
        tipo='Cliente', 
        nombre='Juan', 
        apellido='Perez', 
        correo=test_user_email if test_user_email else 'jperez@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='20.393.296-9',	
        direccion='Avenida Apoquindo 3000\nLas Condes\n Región Metropolitana', 
        subscrito=True, 
        imagen='perfiles/jperez.jpg')

    crear_usuario(
        username='sarmando',
        tipo='Cliente', 
        nombre='Sebastian', 
        apellido='Armando', 
        correo=test_user_email if test_user_email else 'sarmando@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='19.332.009-4', 
        direccion='Avenida Vicuña Mackenna 4860\n Macul\n Región Metropolitana', 
        subscrito=True, 
        imagen='perfiles/sarmando.jpg')

    crear_usuario(
        username='srojas',
        tipo='Cliente', 
        nombre='Sofia', 
        apellido='Rojas', 
        correo=test_user_email if test_user_email else 'srojas@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='17.721.563-5', 
        direccion='Calle Agustinas 1570\n Santiago\n Región Metropolitana', 
        subscrito=False, 
        imagen='perfiles/srojas.jpg')

    crear_usuario(
        username='Asanmartin',
        tipo='Cliente', 
        nombre='Alenjandro', 
        apellido='San Martin', 
        correo=test_user_email if test_user_email else 'Asanmartin@gmail.com', 
        es_superusuario=False, 
        es_staff=False, 
        rut='15.212.293-7', 
        direccion='Avenida El Bosque 123\n Providencia, Región Metropolitana', 
        subscrito=False, 
        imagen='perfiles/asanmartin.jpg')

    crear_usuario(
        username='mgonzales',
        tipo='Administrador', 
        nombre='María', 
        apellido='Gonzales', 
        correo=test_user_email if test_user_email else 'mgonzales@gamestore.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='11.775.002-3', 
        direccion=' Avenida Libertador Bernardo \nO Higgins 1349, \nSantiago, Región Metropolitana', 
        subscrito=False, 
        imagen='perfiles/mgonzales.jpg')
    
    crear_usuario(
        username='cmartinez',
        tipo='Administrador', 
        nombre='Carlos', 
        apellido='Martinez', 
        correo=test_user_email if test_user_email else 'cmartinez@gamestore.com', 
        es_superusuario=False, 
        es_staff=True, 
        rut='16.544.353-6', 
        direccion='Calle Bombero Núñez 363\n Recoleta, Región Metropolitana', 
        subscrito=False, 
        imagen='perfiles/cmartinez.jpg')

    crear_usuario(
        username='superusuario',
        tipo='Superusuario',
        nombre='Daniela',
        apellido='Muñoz',
        correo=test_user_email if test_user_email else 'dmuñoz@gamestore.com',
        es_superusuario=True,
        es_staff=True,
        rut='12.203.562-8',
        direccion=' Calle Huérfanos 1055\n Santiago, Región Metropolitana',
        subscrito=False,
        imagen='perfiles/dmuñoz.jpg')

    
    categorias_data = [
        { 'id': 1, 'nombre': 'Acción'},
        { 'id': 2, 'nombre': 'Aventura'},
        { 'id': 3, 'nombre': 'Estrategia'},
        { 'id': 4, 'nombre': 'RPG'},
        { 'id': 5, 'nombre': 'Mundo abierto'},
        { 'id': 6, 'nombre': 'Simulador'},
    ]

    print('Crear categorías')
    for categoria in categorias_data:
        Categoria.objects.create(**categoria)
    print('Categorías creadas correctamente')

    productos_data = [
        #juegos de accion (9)
        {	    
            'id': 1,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Black Myth: Wukong',
            'descripcion': 'Black Myth: Wukong es un RPG de acción inspirado en la mitología china. Encarnarás al Predestinado, que ha de embarcarse en un viaje repleto de peligros y maravillas para descubrir la verdad oculta acerca de una gloriosa leyenda del pasado.',
            'precio': 39999,
            'descuento_subscriptor': 10,
            'descuento_oferta': 10,
            'imagen': 'productos/001.jpg'
        },
        {
            'id': 2,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Hitman: Absolution™ ',
            'descripcion': '¡El asesino original está de vuelta! El agente 47 busca redimirse en un mundo corrupto y torcido mientras lo caza la policía, después de haber sido traicionado por la agencia.',
            'precio': 13800,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/002.jpg'
        },
        {
            'id': 3,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'HITMAN World of Assassination',
            'descripcion': 'Entra al mundo del asesino definitivo. HITMAN: mundo del asesinato reúne lo mejor de HITMAN, HITMAN 2 y HITMAN 3. Incluye la campaña principal, contratos, intensificaciones, objetivos escurridizos y HITMAN: Freelancer, un modo inspirado en el género roguelike.',
            'precio': 15500,
            'descuento_subscriptor': 0,
            'descuento_oferta': 0,
            'imagen': 'productos/003.jpg'
        },
        {
            'id': 4,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Sekiro™: Shadows Die Twice - GOTY Edition',
            'descripcion': 'Juego del año - The Game Awards 2019 Mejor juego de acción de 2019 - IGN Traza tu propio camino hacia la venganza en la galardonada aventura de FromSoftware, creadores de Bloodborne y la saga Dark Souls. Véngate. Restituye tu honor. Mata con ingenio.',
            'precio': 47650,
            'descuento_subscriptor': 45,
            'descuento_oferta': 15,
            'imagen': 'productos/004.jpg'
        },
        {
            'id': 5,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'HELLDIVERS™ 2',
            'descripcion': 'La última línea de ataque de la galaxia. Alístate en los Helldivers y únete a la lucha por la libertad en una galaxia hostil en un juego de disparos en tercera persona rápido, frenético y feroz.',
            'precio': 29990,
            'descuento_subscriptor': 35,
            'descuento_oferta': 15,
            'imagen': 'productos/005.jpg'
        },
        {
            'id': 6,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Monster Hunter: World',
            'descripcion': '¡Bienvenidos a un nuevo mundo! En Monster Hunter: World, la última entrega de la serie, podrás disfrutar de la mejor experiencia de juego, usando todos los recursos a tu alcance para acechar monstruos en un nuevo mundo rebosante de emociones y sorpresas.',
            'precio': 24100,
            'descuento_subscriptor': 25,
            'descuento_oferta': 15,
            'imagen': 'productos/006.jpg'
        },
        {
            'id': 7,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Granblue Fantasy: Relink',
            'descripcion': '¡Una gran aventura te aguarda en los cielos! Elige entre un variopinto plantel de navegantes para formar un grupo de cuatro y empuña tu espada, tu arma o tu magia para vencer a los temibles enemigos en este RPG de acción. ¡Afronta misiones en solitario o con la ayuda de hasta cuatro...',
            'precio': 38000,
            'descuento_subscriptor': 15,
            'descuento_oferta': 15,
            'imagen': 'productos/007.jpg'
        },
        {
            'id': 8,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Batman™: Arkham Knight',
            'descripcion': 'Batman™: Arkham Knight es la épica conclusión de la galardonada trilogía de Arkham, creada por Rocksteady Studios. El título, desarrollado en exclusiva para plataformas de nueva generación, presenta la espectacular versión del batmóvil imaginada por Rocksteady.',
            'precio': 13999,
            'descuento_subscriptor': 10,
            'descuento_oferta': 0,
            'imagen': 'productos/008.jpg'
        },
        {
            'id': 9,
            'categoria': Categoria.objects.get(id=1),
            'nombre': 'Lies of P',
            'descripcion': 'Lies of P es un soulslike trepidante que toma la conocida historia de Pinocho, le da la vuelta y la ubica en una belle époque elegante y oscura.',
            'precio': 35800,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/009.jpg'
        },
        #juegos de Aventura (7)
        {
            'id': 10,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Forza Horizon 4',
            'descripcion': 'Las estaciones dinámicas lo cambian todo en el mejor festival automovilístico del mundo. Ve por cuenta propia o únete a otros equipos para explorar la hermosa e histórica Gran Bretaña en un mundo abierto compartido.',
            'precio': 49990,
            'descuento_subscriptor': 0,
            'descuento_oferta': 90,
            'imagen': 'productos/010.jpg'
        },
        {
            'id': 11,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'KINGDOM HEARTS -HD 1.5+2.5 ReMIX-',
            'descripcion': 'KINGDOM HEARTS -HD 1.5+2.5 ReMIX- es una colección remasterizada en alta definición de 6 inolvidables experiencias de KINGDOM HEARTS. Empuña tu llave espada para salvar los mundos de Disney de la oscuridad.',
            'precio': 39999,
            'descuento_subscriptor': 5,
            'descuento_oferta': 50,
            'imagen': 'productos/011.jpg'
        },
        {
            'id': 12,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Chained Together',
            'descripcion': 'Desde las profundidades del infierno, escala encadenado a tus amigos a través de diversos mundos. Solo o en cooperativo, intenta alcanzar la cumbre y descubre lo que te espera allí...',
            'precio': 3000,
            'descuento_subscriptor': 0,
            'descuento_oferta': 0,
            'imagen': 'productos/012.jpg'
        },
        {
            'id': 13,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Sons Of The Forest',
            'descripcion': 'Enviado a buscar a un multimillonario desaparecido en una isla remota, te encuentras en un infierno infestado de caníbales. Crea, construye y lucha por sobrevivir, solo o con amigos, en este nuevo y aterrador simulador de terror y supervivencia de mundo abierto.',
            'precio': 15500,
            'descuento_subscriptor': 10,
            'descuento_oferta': 0,
            'imagen': 'productos/013.jpg'
        },
        {
            'id': 14,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Persona 3 Reload',
            'descripcion': 'Sumérgete en la Hora Oscura y despierta lo más profundo de tu corazón. Persona 3 Reload es la fascinante nueva versión del RPG que definió el género y que ahora renace para la era moderna con gráficos y una jugabilidad de última generación.',
            'precio': 60900,
            'descuento_subscriptor': 75,
            'descuento_oferta': 15,
            'imagen': 'productos/014.jpg'
        },
        {
            'id': 15,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'DAVE THE DIVER',
            'descripcion': 'DAVE THE DIVER es un juego casual de rol y aventuras para un solo jugador que incluye elementos de pesca y exploración del fondo marino durante el día y de gestión de un restaurante de sushi durante la noche. Ayuda a Dave y a sus extraños amigos a destapar los secretos de la...',
            'precio': 10500,
            'descuento_subscriptor': 25,
            'descuento_oferta': 15,
            'imagen': 'productos/015.jpg'
        },
        {
            'id': 16,
            'categoria': Categoria.objects.get(id=2),
            'nombre': 'Sea of Thieves: 2024 Edition',
            'descripcion': 'Sea of Thieves es un exitoso juego de aventuras piratas que ofrece la experiencia pirata por excelencia de saquear tesoros perdidos, batallas intensas, vencer monstruos marinos y más. Sumérgete en esta edición revisada del juego, que incluye acceso a medios digitales de bonificación.',
            'precio': 22990,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/016.jpg'
        },
        #juegos de Estrategia (6)
        {
            'id': 17,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Crusader Kings III',
            'descripcion': 'Ama, lucha, planea y reclama la grandeza. Determina el legado de tu casa nobiliaria en la gran estrategia en expansión de Crusader Kings III. La muerte solo es el comienzo mientras lideras el linaje de tu dinastía en esta completa simulación realista de la Edad Media.',
            'precio': 35200,
            'descuento_subscriptor': 25,
            'descuento_oferta': 5,
            'imagen': 'productos/017.jpg'
        },
        {
            'id': 18,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Hearts of Iron IV',
            'descripcion': '¡Tenemos la victoria al alcance de la mano! Tu capacidad para liderar tu nación es tu arma principal. En el juego de estrategia Hearts of Iron IV podrás ponerte el mando de cualquier nación de la II Guerra Mundial, el conflicto más fascinante de la historia mundial.',
            'precio': 35200,
            'descuento_subscriptor': 25,
            'descuento_oferta': 35,
            'imagen': 'productos/018.jpg'
        },
        {
        'id': 19,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Anno 1800',
            'descripcion': 'Anno 1800™ – ¡Lidera la Revolución Industrial! Te damos la bienvenida al comienzo de la Era Industrial. El camino que elijas determinará el futuro de tu mundo. ¿Innovarás o explotarás al pueblo? ¿Conquistarás o liberarás a los oprimidos? El mundo te recordará, pero la forma en que lo haga solo...',
            'precio': 39900,
            'descuento_subscriptor': 15,
            'descuento_oferta': 35,
            'imagen': 'productos/019.jpg'
        },
        {
        'id': 20,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Age of Mythology: Retold',
            'descripcion': 'De los creadores de la galardonada franquicia «Age of Empires», «Age of Mythology: Retold» va más allá de la historia y te transporta a una época mítica de conflicto entre los dioses, los monstruos y los humanos.',
            'precio': 17000,
            'descuento_subscriptor': 10,
            'descuento_oferta': 25,
            'imagen': 'productos/020.jpg'
        },
        {
            'id': 21,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Total War: THREE KINGDOMS',
            'descripcion': 'Total War™: THREE KINGDOMS es el primero de la serie que recrea conflictos épicos de la antigua China. Al combinar una apasionante campaña por turnos de construcción de imperios y conquista con batallas a tiempo real, THREE KINGDOMS redefine la serie de una época de héroes y leyendas.',
            'precio': 28500,
            'descuento_subscriptor': 15,
            'descuento_oferta': 35,
            'imagen': 'productos/021.jpg'
        },
        {
            'id': 22,
            'categoria': Categoria.objects.get(id=3),
            'nombre': 'Infection Free Zone',
            'descripcion': '¡Lidera a los supervivientes de tu ciudad! Elige tu base de operaciones; y reconstruye y acondiciona edificios para crear un asentamiento autosuficiente. ¡Cuando caiga la noche tendrás que defenderlo de los infectados! Juega en CUALQUIER CIUDAD DEL MUNDO, ¡el juego usa datos geográficos reales!',
            'precio': 11999,
            'descuento_subscriptor': 0,
            'descuento_oferta': 0,
            'imagen': 'productos/022.jpg'
        },
        #juegos de RPG (5)
        {
            'id': 23,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Hades',
            'descripcion': 'Desafía al dios de los muertos y protagoniza una salvaje fuga del Inframundo en este juego de exploración de mazmorras de los creadores de Bastion, Transistor y Pyre.',
            'precio': 13000,
            'descuento_subscriptor': 0,
            'descuento_oferta': 0,
            'imagen': 'productos/023.jpg'
        },
        {
            'id': 24,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Hades II',
            'descripcion': 'Usa las artes oscuras para abrirte paso más allá del inframundo y enfréntate al Titán del Tiempo en esta cautivadora continuación del galardonado juego de mazmorras de tipo rogue-like.',
            'precio': 15500,
            'descuento_subscriptor': 50,
            'descuento_oferta': 30,
            'imagen': 'productos/024.jpg'
        },
        {
            'id': 25,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Baldur´s Gate 3',
            'descripcion': 'Reúne a tu grupo y vuelve a los Reinos Olvidados en un relato de compañerismo y traición, sacrificio y supervivencia, además de la atracción de un poder absoluto.',
            'precio': 39999,
            'descuento_subscriptor': 50,
            'descuento_oferta': 15,
            'imagen': 'productos/025.jpg'
        },
        {
            'id': 26,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'Hogwarts Legacy',
            'descripcion': 'Hogwarts Legacy es un RPG inmersivo de acción en mundo abierto. Ahora puedes tomar el control de la acción y ser el centro de tu propia aventura en el mundo mágico',
            'precio': 39999,
            'descuento_subscriptor': 0,
            'descuento_oferta': 50,
            'imagen': 'productos/026.jpg'
        },
        {
            'id': 27,
            'categoria': Categoria.objects.get(id=4),
            'nombre': 'RPG Maker MV',
            'descripcion': 'SENCILLEZ PARA INICIADOS, COMPLEJIDAD PARA EXPERTOS. ¡RPG MAKER MV pone a tu disposición todas las herramientas para que hagas el RPG con el que siempre has soñado! ¡Esta versión cuenta con un sinfín de nuevas características y opciones de exportación para MAcOS, Android e...',
            'precio': 38000,
            'descuento_subscriptor': 25,
            'descuento_oferta': 25,
            'imagen': 'productos/027.jpg'
        },
        #juegos de Mundo abierto(9)
        {
            'id': 28,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'theHunter: Call of the Wild™',
            'descripcion': 'Descubre un atmosférico juego de caza sin parangón en un mundo abierto realista y sobrecogedor que se actualiza a menudo en colaboración con la comunidad. Sumérgete en la campaña de un jugador o comparte la experiencia definitiva de caza con amigos.',
            'precio': 10500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/028.jpg'
        },
        {
            'id':29,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'Palworld',
            'descripcion': 'Este es un juego multijugador de supervivencia en mundo abierto inmenso y original, en el que tendrás que hacerte con unas misteriosas criaturas llamadas Pals, capaces de combatir, construir, cultivar y trabajar en fábricas.',
            'precio': 15500,
            'descuento_subscriptor': 8,
            'descuento_oferta': 20,
            'imagen': 'productos/029.jpg'
        },
        {
            'id': 30,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'Rust',
            'descripcion': 'El único objetivo en Rust es sobrevivir. Todo quiere que mueras: la vida salvaje de la isla y otros habitantes, el medio ambiente y otros supervivientes. Haz lo que sea necesario para durar una noche más.',
            'precio': 17900,
            'descuento_subscriptor': 2,
            'descuento_oferta': 15,
            'imagen': 'productos/030.jpg'
        },
        {
        'id': 31,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'ARK: Survival Ascended',
            'descripcion': '¡Ark se reinventa desde cero en esta próxima generación de tecnología de videojuegos con Unreal Engine 5! Forma una tribu, domestica y cría cientos de dinosaurios únicos y criaturas primitivas, exploran, cree, construyen y luchan hasta la cima de la cadena alimentaria. ¡Tu nuevo mundo te espera!',
            'precio': 41600,
            'descuento_subscriptor': 5,
            'descuento_oferta': 2,
            'imagen': 'productos/031.jpg'
        },
        {
        'id': 32,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'ARK: Survival Evolved',
            'descripcion': 'Juega como un hombre o una mujer desnudo, congelándote y muriéndote de hambre en una isla misteriosa. Debes cazar, cosechar, crear objetos, cultivar, y construir refugios para sobrevivir. Usa tu habilidad y astucia para matar, domesticar, criar y cabalgar dinosaurios y otras criaturas primitivas.',
            'precio': 8300,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/032.jpg'
        },
        {
            'id': 33,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'Terraria',
            'descripcion': '¡Cava, lucha, explora, construye! Con este juego de aventuras repleto de acción nada es imposible. ¡Pack de Cuatro también disponible!',
            'precio': 5750,
            'descuento_subscriptor': 0,
            'descuento_oferta': 0,
            'imagen': 'productos/033.jpg'
        },
        {
            'id': 34,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'New World',
            'descripcion': 'Explora un emocionante MMO de mundo abierto repleto de peligros y oportunidades en el que forjarás un nuevo destino en la isla sobrenatural de Aetérnum.',
            'precio': 35706,
            'descuento_subscriptor': 5,
            'descuento_oferta': 45,
            'imagen': 'productos/034.jpg'
        },
        {
            'id': 35,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'Fallout 4',
            'descripcion': 'Bethesda Game Studios, el galardonado creador de Fallout 3 y The Elder Scrolls V: Skyrim, os da la bienvenida al mundo de Fallout 4, su juego más ambicioso hasta la fecha y la siguiente generación de mundos abiertos.',
            'precio': 13900,
            'descuento_subscriptor': 10,
            'descuento_oferta': 15,
            'imagen': 'productos/035.jpg'
        },
        {
            'id': 36,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'FINAL FANTASY XV WINDOWS EDITION',
            'descripcion': 'Una aventura con la mejor calidad. Gracias a un montón de contenidos adicionales y compatibilidad con opciones gráficas de alta resolución y HDR10, ahora puedes disfrutar como nunca antes de la experiencia de FINAL FANTASY XV en un mundo hermoso y lleno de detalles.',
            'precio': 23200,
            'descuento_subscriptor': 10,
            'descuento_oferta': 25,
            'imagen': 'productos/036.jpg'
        },
        #juegos de Simulador (4)
        {
            'id': 37,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'Euro Truck Simulator 2',
            'descripcion': '¡Viaja por Europa como el rey de la carretera, un camionero que entrega cargas importantes a distancias impresionantes! Con docenas de ciudades para explorar, tu resistencia, habilidad y velocidad serán llevadas al límite.',
            'precio': 10900,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/037.jpg'
        },
        {
            'id': 38,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'jurassic world evolution2',
            'descripcion': 'Jurassic World Evolution 2 es la esperada secuela de Jurassic World Evolution, el éxito de Frontier de 2018. La segunda parte de la franquicia ofrece una propuesta atrevida basada en el éxito que cosechó la primera entrega con su enfoque innovador e inmersivo.',
            'precio': 30500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 30,
            'imagen': 'productos/038.jpg'
        },
        {
            'id': 39,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'Stardew Valley',
            'descripcion': 'Acabas de heredar la vieja parcela agrícola de tu abuelo de Stardew Valley. Decides partir hacia una nueva vida con unas herramientas usadas y algunas monedas. ¿Te ves capaz de vivir de la tierra y convertir estos campos descuidados en un hogar próspero?',
            'precio': 7500,
            'descuento_subscriptor': 5,
            'descuento_oferta': 0,
            'imagen': 'productos/039.jpg'
        },
        {
            'id': 40,
            'categoria': Categoria.objects.get(id=5),
            'nombre': 'Supermarket Simulator',
            'descripcion': 'Dirige tu propio supermercado. Abastece las estanterías, fija los precios a tu gusto, acepta pagos, contrata personal, amplía y diseña tu tienda. Pedidos y entregas en línea, ladrones, seguridad, mercado local.',
            'precio': 7300,
            'descuento_subscriptor': 5,
            'descuento_oferta': 5,
            'imagen': 'productos/040.jpg'
        }
    ]

    print('Crear productos')
    for producto in productos_data:
        Producto.objects.create(**producto)
    print('Productos creados correctamente')

    print('Crear carritos')
    for rut in ['20.393.296-9', '11.775.002-3']:
        cliente = Perfil.objects.get(rut=rut)
        for cantidad_productos in range(1, 11):
            producto = Producto.objects.get(pk=randint(1, 10))
            if cliente.subscrito:
                descuento_subscriptor = producto.descuento_subscriptor
            else:
                descuento_subscriptor = 0
            descuento_oferta = producto.descuento_oferta
            descuento_total = descuento_subscriptor + descuento_oferta
            descuentos = int(round(producto.precio * descuento_total / 100))
            precio_a_pagar = producto.precio - descuentos
            Carrito.objects.create(
                cliente=cliente,
                producto=producto,
                precio=producto.precio,
                descuento_subscriptor=descuento_subscriptor,
                descuento_oferta=descuento_oferta,
                descuento_total=descuento_total,
                descuentos=descuentos,
                precio_a_pagar=precio_a_pagar
            )
    print('Carritos creados correctamente')

    print('Crear boletas')
    nro_boleta = 0
    perfiles_cliente = Perfil.objects.filter(tipo_usuario='Cliente')
    for cliente in perfiles_cliente:
        estado_index = -1
        for cant_boletas in range(1, randint(6, 21)):
            nro_boleta += 1
            estado_index += 1
            if estado_index > 3:
                estado_index = 0
            estado = Boleta.ESTADO_CHOICES[estado_index][1]
            fecha_venta = date(2023, randint(1, 5), randint(1, 28))
            fecha_despacho = fecha_venta + timedelta(days=randint(0, 3))
            fecha_entrega = fecha_despacho + timedelta(days=randint(0, 3))
            if estado == 'Anulado':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Vendido':
                fecha_despacho = None
                fecha_entrega = None
            elif estado == 'Despachado':
                fecha_entrega = None
            boleta = Boleta.objects.create(
                nro_boleta=nro_boleta, 
                cliente=cliente,
                monto_sin_iva=0,
                iva=0,
                total_a_pagar=0,
                fecha_venta=fecha_venta,
                fecha_despacho=fecha_despacho,
                fecha_entrega=fecha_entrega,
                estado=estado)
            detalle_boleta = []
            total_a_pagar = 0
            for cant_productos in range(1, randint(4, 6)):
                producto_id = randint(1, 10)
                producto = Producto.objects.get(id=producto_id)
                precio = producto.precio
                descuento_subscriptor = 0
                if cliente.subscrito:
                    descuento_subscriptor = producto.descuento_subscriptor
                descuento_oferta = producto.descuento_oferta
                descuento_total = descuento_subscriptor + descuento_oferta
                descuentos = int(round(precio * descuento_total / 100))
                precio_a_pagar = precio - descuentos
                bodega = Bodega.objects.create(producto=producto)
                DetalleBoleta.objects.create(
                    boleta=boleta,
                    bodega=bodega,
                    precio=precio,
                    descuento_subscriptor=descuento_subscriptor,
                    descuento_oferta=descuento_oferta,
                    descuento_total=descuento_total,
                    descuentos=descuentos,
                    precio_a_pagar=precio_a_pagar)
                total_a_pagar += precio_a_pagar
            monto_sin_iva = int(round(total_a_pagar / 1.19))
            iva = total_a_pagar - monto_sin_iva
            boleta.monto_sin_iva = monto_sin_iva
            boleta.iva = iva
            boleta.total_a_pagar = total_a_pagar
            boleta.fecha_venta = fecha_venta
            boleta.fecha_despacho = fecha_despacho
            boleta.fecha_entrega = fecha_entrega
            boleta.estado = estado
            boleta.save()
            print(f'    Creada boleta Nro={nro_boleta} Cliente={cliente.usuario.first_name} {cliente.usuario.last_name}')
    print('Boletas creadas correctamente')

    print('Agregar productos a bodega')
    for producto_id in range(1, 11):
        producto = Producto.objects.get(id=producto_id)
        cantidad = 0
        for cantidad in range(1, randint(2, 31)):
            Bodega.objects.create(producto=producto)
        print(f'    Agregados {cantidad} "{producto.nombre}" a la bodega')
    print('Productos agregados a bodega')

