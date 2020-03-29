import numpy as np
from io import BytesIO
from PIL import Image
import requests
import time


def get_proof():
    with open('../result.txt', 'rb') as f:
        data = f.read().split(b'\n')[:-1]
    return [item.decode()[3:] for item in data]


def get_tab_from_image():
    with open('image', 'rb') as f:
        data = f.read()
    r = requests.get('http://pixelwar.h25.io/image')
    if data == r.content:  # image still in cache 
        print('Waiting cache to update, sleep 10 secs')
        time.sleep(10)
        return get_tab_from_custom_image()
    # update image
    print('Update local image file')
    with open('image', 'wb') as f:
        f.write(r.content)
    all_tab = np.array(Image.open(BytesIO(r.content)))
    return all_tab[-25-10:-10, 30:30+25].tolist()  # bottom left corner


def get_tab_from_custom_image():
    with open('png/picture.png', 'rb') as f:
        content = f.read()
    tab = np.array(Image.open(BytesIO(content)))
    return tab.tolist()


def update_pixel(x: int, y: int, color: str, proof: str):
    params = {
        'x': str(x),
        'y': str(y),
        'color': color,
        'proof': proof
    }
    r = requests.get('http://137.74.47.86/setpixel', params=params)
    print((r.content, params))
    time.sleep(0.03)


def main():
    proofs = get_proof()
    count = int(open('count.txt', 'rb').read().decode())
    proofs = proofs[count:]  # ignore already used proofs
    server_tab = get_tab_from_image()
    custom_tab = get_tab_from_custom_image()
    if len(proofs) == 0:
        print('Wait to compute more hashes')
        return
    for i in range(len(server_tab)):
        for j in range(len(server_tab[0])):
            server_pixel = server_tab[i][j][:3]
            custom_pixel = custom_tab[i][j][:3]
            if custom_pixel == [0, 0, 0]:
                continue  # ignore transparent pixel
            if server_pixel == custom_pixel:
                continue  # do not update pixel
            y = 100 - 25 - 10 + i
            x = 30 + j
            custom_color = ''.join([hex(i)[2:].zfill(2) for i in custom_pixel])
            proof = proofs[0]
            update_pixel(x, y, custom_color, proof)
            count += 1
            with open('count.txt', 'wb') as f:
                f.write(str(count).encode())
            count = int(open('count.txt', 'rb').read().decode())
            proofs = proofs[1:]  # update available proofs
            if len(proofs) == 0:
                print('Wait to compute more hashes')
                return


if __name__ == '__main__':
    while True:
        main()
