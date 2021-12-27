import os

from yandex_music.client import Client
from pprint import pprint
import sqlalchemy
# без авторизации недоступен список треков альбома

class WRITE_DB:
    
    def __init__(self):
        # self.album_id = album_id
        self.token = os.environ.get('TOKEN')
        self.client = Client(self.token)
                
        

    def get_track_info(self, album_id):

        album = self.client.albums_with_tracks(album_id)
        
        tracks = []

        for i, volume in enumerate(album.volumes):
            if len(album.volumes) > 1:
                tracks.append(f'Диск {i + 1}')
            tracks += volume
        
        new_data = {}
        my_data = {}
        # track_list = []
        for track in tracks:
            # print(track.title)
            my_data[track.title] = track.duration_ms
            # track_list.append(my_data)
            if track.artists:
                for artist in track.artists:
                    name = artist.name
                    
                    #  = [artist.name.split()[0], artist.name.split()[1]] 

        new_data = {
            'name':name,
            'album_name':album.title,
            'genre_name':album.genre,
            'release_year':album.year,
            'track': my_data
        }
        return new_data

    def insert_db(self, val_dict):
        self.val_dict = val_dict
        # self.engine = sqlalchemy.create_engine(f'postgresql://{user_db}:{pass_db}@localhost:5433/{db_name}')
        engine = sqlalchemy.create_engine('postgresql://music:Start123@localhost:5433/music_store')
        # engine = sqlalchemy.create_engine('postgresql://bas:Start123@localhost:5432/music_store')
        connection = engine.connect()
        
        name_ex = f"{val_dict['name'].split()[0]}"

        alias_name = f"{val_dict['name']}"
        query_name = f"""SELECT alias 
            FROM executor 
            WHERE alias = '{alias_name}'
            ;"""
        res = connection.execute(f"{query_name}").fetchone()
        print(f"{res}, {val_dict['name']}")
        
        if not connection.execute(f"{query_name}").fetchone() == val_dict['name']:
            if len(val_dict['name'].split()) > 1:

                connection.execute(f"""INSERT INTO executor (executor_name, surname, alias) 
                VALUES('{name_ex}', '{val_dict['name'].split()[1]}', '{val_dict['name']}')
                ;""")
                print(f"Исполнитель записан {val_dict['name']}")

            else:

                connection.execute(f"""INSERT INTO executor (executor_name, alias) 
                VALUES('{name_ex}', '{val_dict['name']}')
                ;""")
                print(f"Исполнитель записан {val_dict['name']}")
        else:

            print(f"Запись присутствует в таблице '{val_dict['name']}'")

        if not connection.execute(f"""SELECT id_genre FROM genre WHERE genre_name = '{val_dict['genre_name']}';
            """).fetchone():
            connection.execute(f"INSERT INTO genre (genre_name) VALUES('{val_dict['genre_name']}');")
            print("Жанр записан в таблицу")
        else:
            print("Такой жанр присутствует в таблице")
          
        if not connection.execute(f"""SELECT * FROM album WHERE album_name = '{val_dict['album_name']}';
            """).fetchone():
            connection.execute(f"INSERT INTO album (album_name, release_year) VALUES('{val_dict['album_name']}', '{val_dict['release_year']}');")
        else:
            print("Такой альбом существует")

        for tr_name, dur in val_dict['track'].items():
            query_id_album = connection.execute(f"SELECT id_album FROM album WHERE album_name LIKE '{val_dict['album_name']}';").fetchone()[0]
            if not connection.execute(f"""SELECT track_name FROM track WHERE track_name = '{tr_name}';
            """).fetchone():
                connection.execute(f"INSERT INTO track (track_name, duration, id_album) VALUES('{tr_name}', '{dur}', {query_id_album});")
                print(f"Имя трэка {tr_name} продолжительность {dur} ИД альбома {query_id_album} - запись создана")
            else:
                print("Запись существует")

        query_id_executor = connection.execute(f"""SELECT * 
            FROM executor 
            WHERE executor_name = '{name_ex}'
            ;""").fetchone()[0]

        if not connection.execute(f"""SELECT id_executor, id_album FROM executoralbum WHERE id_executor = {query_id_executor} AND id_album = {query_id_album};""").fetchone():
            connection.execute(f"INSERT INTO executoralbum (id_executor, id_album) VALUES({query_id_executor}, {query_id_album});")
            print("связь добавлена")
        else:
            print("Связь существует")

        query_id_genre = connection.execute(f"""SELECT id_genre 
            FROM genre 
            WHERE genre_name = '{val_dict['genre_name']}'
            ;""").fetchone()[0]
        connection.execute(f"""INSERT INTO executorgenre (id_executor, id_genre) VALUES({query_id_executor}, {query_id_genre})
        ;""")

    def create_collection ():
        pass


if __name__ == '__main__':
    
    while True:
        album_in = int(input('Введите ID яндекс альбома(0-выход): '))
        if album_in == 0:
            break
        else:

            my_dict = WRITE_DB().get_track_info(album_in)
            print('--------------')
            print(my_dict)
            print('--------------')
            WRITE_DB().insert_db(my_dict)