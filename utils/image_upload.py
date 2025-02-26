from imagehost import ImageHost
def upload_image(path):
    client = ImageHost('6d207e02198a847aa98d0a2a901485a5')

    response = client.upload(path)

    print(response['image']['url'])
    return response['image']['url']
