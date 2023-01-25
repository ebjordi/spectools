import imageio
import imageio.v2 as imageio

def main(images_prefix = None,output_gif = None)
    with imageio.get_writer('orbitssasda.gif', mode='I') as writer:
        for i in range(100):
            filename = f'sp_or{i}.png'
            image = imageio.imread(filename)
            writer.append_data(image)

if __name__='__main__':
    main()
