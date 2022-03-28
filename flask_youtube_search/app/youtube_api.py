import requests
import pymongo
from isodate import parse_duration
from flask import current_app

connection = pymongo.MongoClient("localhost", 27017)
db = connection.youtubeData

def search(busca):
    search_url = 'https://www.googleapis.com/youtube/v3/search'
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    videos = []

    search_params = {
            'key': current_app.config['YOUTUBE_API_KEY'],
            'q': str(busca),   
            'part': 'snippet',
            'maxResults': 9,
            'type': 'video'
        }

    r = requests.get(search_url, params=search_params)


    results = r.json()['items']

    video_ids = []
    
    for result in results:
        video_ids.append(result['id']['videoId'])
        

    video_params = {
                'key': current_app.config['YOUTUBE_API_KEY'],
                'id': ','.join(video_ids),
                'part': 'snippet,contentDetails',
                'maxResults': 9
            }


    r = requests.get(video_url, params=video_params)
    results = r.json()['items']
    

    for result in results:
        video_data = {
                    'id': result['id'],
                    'url': f'https://www.youtube.com/watch?v={result["id"]}',
                    'thumbnail': result['snippet']['thumbnails']['high']['url'],
                    'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                    'publishedAt': result['snippet']['publishedAt'],
                    'title': result['snippet']['title'],
                    'description': result['snippet']['description'],
                    'channelTitle': result['snippet']['channelTitle']
                }

        videos.append(video_data)

    return videos
      

def pesquisa_video(id):
    video_url = 'https://www.googleapis.com/youtube/v3/videos'

    video = []
    
    video_params = {
                'key': current_app.config['YOUTUBE_API_KEY'],
                'id': str(id),
                'part': 'snippet,contentDetails,statistics',
            }

    r = requests.get(video_url, params=video_params)

    results = r.json()['items']

    for result in results:
        video_data = {
            
                    'id': result['id'],
                    'url': f'https://www.youtube.com/watch?v={result["id"]}',
                    'thumbnail': result['snippet']['thumbnails']['high']['url'],
                    'publishedAt': result['snippet']['publishedAt'],
                    'title': result['snippet']['title'],
                    'description': result['snippet']['description'],
                    'channelTitle': result['snippet']['channelTitle'],
                    'categoryId': result['snippet']['categoryId'],
                    'duration': int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60),
                    'licensedContent': result['contentDetails']['licensedContent'],
                    'viewCount': result['statistics']['viewCount'],
                    'likeCount': result['statistics']['likeCount'],
                    'dislikeCount': result['statistics']['dislikeCount'],
                    'favoriteCount': result['statistics']['favoriteCount'],
                    'commentCount': result['statistics']['viewCount'],

                     "General":{
                        "Identifier": result['id'],
                        "Title": result['snippet']['title'],
                        "Catalog_Entry":{
                            "Catalogue": result['snippet']['categoryId'], 
                            "Entry": None
                        },
                        "Language": None,
                        "Description": result['snippet']['description'],
                        "Keywords": None,
                        "Coverage": None,
                        "Structure": 'Linear, Hierárquico',
                        "Aggregation_Level": '3'
                    },
                    "Life_Cycle":{
                        "Version": None,
                        "Status": None,
                        "Contribute":{
                            "Role": None,
                            "Entity": None,
                            "Date": result['snippet']['publishedAt'] 
                        }
                    },
                    "Meta_metadata":{
                        "Identifier": result['id'],
                        "Catalog":{
                            "Catalog": result['snippet']['categoryId'],
                            "Entry": None 
                        },
                        "Contribute":{
                            "Role": result['snippet']['channelTitle'],
                            "Entity": 'YouTube',
                            "Date": result['snippet']['publishedAt']
                        },
                        "Metadata_Scheme": 'IEEE LOM',
                        "Language": None 
                    },
                    "Technical":{
                        "Format": None,
                        "Size": None,
                        "Location": None,
                        "Requirements":{
                            "Type": None,
                            "Name": None,
                            "Min_version": None,
                            "Max_version": None
                        },
                        "Installation_Remarks": None,
                        "Other_platform_requirements": None,
                        "Duration": int(parse_duration(result['contentDetails']['duration']).total_seconds() // 60)
                    },
                    "Educational":{
                        "Interactivity_Type": 'Expositivo',
                        "Learning_Resource_Type": 'Vídeo',
                        "Interactivity_Level": 'Baixo',
                        "Semantic_Density": 'Médio',
                        "Intended_end_user_role": 'Aprendiz',
                        "Context": None,
                        "Typical_Age_Range": None,
                        "Difficulty": None,
                        "Typical_learning_Time": None,
                        "Description": None,
                        "Language": None
                    },
                    "Rights":{
                        "Cost": None,
                        "Copyright_and_other_restrictions": result['contentDetails']['licensedContent'],
                        "Description": None, 
                    },
                    "Relation":{
                        "Kind": None,
                        "Resource":{
                            "Identifier": None,
                            "Description": None,
                            "Catalog_entry": None 
                        }
                    },
                    "Annotation":{
                        "Person": None,
                        "Date": result['snippet']['publishedAt'],
                        "Description": None
                    },
                    "Classification":{
                        "Purpose": None,
                        "Taxon_path":{
                            "Source": None,
                            "Taxon":{
                                "ID": result['id'],
                                "Entry": f'https://www.youtube.com/watch?v={result["id"]}'
                            }
                        },
                        "Description": None,
                        "Keywords": None
                    }
        } 

    video.append(video_data)
    
    return video

def salvar_video(video):
    try:
        db.youtube.insert_one(video)
    except:
        print("Ocorreu um erro ao inserir vídeo!")   


def apagar_video(video):
    try:
        db.youtube.delete_one(video)
    except:
        print("Ocorreu um erro ao deletar vídeo!")

def videos_salvos():
    videos = list(db.youtube.find())
    return videos

def video_dados(video):
    video_dado = db.youtube.find_one({"id": str(video)})
    return video_dado

def update_title(video, novo_titulo):
    try:
        db.youtube.update_one({"General.Title": str(video["General"]["Title"])},{"$set":{"General.Title": str(novo_titulo)}})
        print("\nTítulo atualizado!")
    except:
        print("Ocorreu um erro!")
    return None

def update_resumo(video, novo_resumo):
    try:
        db.youtube.update_one({"General.Description": str(video["General"]["Description"])},{"$set":{"General.Description": str(novo_resumo)}})
        print("\nResumo atualizado!")
    except:
        print("Ocorreu um erro!")
    return None


