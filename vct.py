import tweepy
from time import sleep
from datetime import datetime
from textblob import TextBlob
import matplotlib.pyplot as plt

consumer_key = "zS35D3QFtKcJpks50JczbR8X4"
consumer_secret = "WgMAwvknU39GG7moVMPOXfMEFAhKEDBwPt01t6pscvqdaGehR8"
access_token = "1379790962566836227-L6Dwxikmh8AqdIh2kdwU0mxa0ldVTR"
access_token_secret = "GtIsJJFsX7A8Y5sz3ZM6erpVh4r2b5E6aS2jRVWL3NwyM"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

palabra = input("Buscar: ")
numero_de_tweets = int(input("Número de tweets a capturar: "))
lenguaje = input("Idioma [es/en]: ")

def ObtenerTweets(palabra,num_tweets,lenguaje):
    polaridad_list = []
    numeros_list = []
    numero = 1
    for tweet in tweepy.Cursor(api.search, palabra, lang=lenguaje).items(num_tweets):
        try:
            analisis = TextBlob(tweet.text)
            analisis = analisis.sentiment
            polaridad = analisis.polarity
            polaridad_list.append(polaridad)
            numeros_list.append(numero)
            numero = numero + 1
            
        except tweepy.TweepError as e:
            print(e.reason)
            
        except StopIteration:
            break
    return (numeros_list, polaridad_list, numero)

def GraficarDatos(numeros_list, polaridad_list, numero):
    axes = plt.gca()
    axes.set_ylim([-1, 2])
    
    plt.scatter(numeros_list, polaridad_list)
    polaridadPromedio = (sum(polaridad_list))/(len(polaridad_list))
    polaridadPromedio = "{0:.2f}%".format(polaridadPromedio * 100)
    time = datetime.now().strftime("A: %H:%M\nEl: %d-%m-%y")
    plt.text(0, 1.25,
            "Sentimiento promedio: " + str(polaridadPromedio) + "\n" + time,
            fontsize = 12,
            bbox = dict(facecolor="none",
                       edgecolor="black",
                       boxstyle="square, pad = 1"))
    
    plt.title("Sentimientos sobre " + palabra + " en twitter")
    plt.xlabel("Número de tweets")
    plt.ylabel("Polaridad sentimiento")
    plt.show()
    
numeros_list, polaridad_list, numero = ObtenerTweets(palabra, numero_de_tweets, lenguaje)

GraficarDatos(numeros_list,polaridad_list,numero)