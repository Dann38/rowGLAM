from config import get_final_model, PATH_GRAPHS_JSONS, PATH_PUBLAYNET
import argparse
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from pager.page_model.sub_models.converters import PDF2Img
from pager.page_model.sub_models.pdf_model import PDFModel
from pager.page_model.sub_models.image_model import ImageModel
from pager.page_model.sub_models.dtype import ImageSegment
from script_train import GLAMDataset
import os

# model = get_final_model()
COLORS = [
    '#1f77b4',  # синий (Vega Blue)
    '#ff7f0e',  # оранжевый (Vega Orange)
    '#2ca02c',  # зелёный (Vega Green)
    '#d62728',  # красный (Vega Red)
    '#9467bd',   # фиолетовый (Vega Purple)
    '#000000'
]

LABELS = ["figure", "text", "header", "list", "table", "no_detect"]

img = ImageModel()

dataset = GLAMDataset(PATH_GRAPHS_JSONS)

def plot_file(json_file):
    
    path_file = os.path.join(PATH_PUBLAYNET, 'train', json_file['file_name'])

    img.read_from_file(path_file)

    print(json_file.keys())
    print("nodes [0, end]:")
    print(json_file['nodes_feature'][0])
    print(json_file['nodes_feature'][-1])
    print("edges [0, end]:")
    print(json_file['edges_feature'][0])
    print(json_file['edges_feature'][-1])

    for data,cls in zip(json_file['rows'], json_file['true_nodes']):
        seg = ImageSegment(dict_2p=data['segment'])
        seg.plot(color=COLORS[cls if cls!=-1 else 5])
    img.show()


    legend_elements = [Patch(facecolor=color, label=label) 
                    for color, label in zip(COLORS, LABELS)]

    plt.legend(handles=legend_elements, 
            title='Классы изображений',
            loc='upper right')


# parser = argparse.ArgumentParser()
# parser.add_argument('-i', type=str, nargs='?', required=True)
# args = parser.parse_args()

# def plot_file(path_pdf, class_=False):
#     model.read_from_file(path_pdf)
#     pdf.read_from_file(path_pdf)
#     pdf2img.convert(pdf, img)
#     model.extract()

#     fig, (ax1, ax2)= plt.subplots(1, 2,dpi=200)
#     ax1.set_xticks([])  # Remove x-axis ticks
#     ax1.set_yticks([])  # Remove y-axis ticks
#     plt.subplot(1, 2, 1)
#     img.show()

#     A = model.page_units[0].sub_model.json["A"]
#     words = model.page_units[0].sub_model.json["words"]
#     segs = [ImageSegment(dict_2p=w['segment']) for w in words]
#     # for seg in segs:
#     #     seg.plot()
#     k = model.page_units[2].converters['json_model'].tmp_edge
    
#     for r, e1, e2 in zip(k,  A[0], A[1]):
#         b1 = segs[e1]
#         b2 = segs[e2]
#         x0, y0 = b1.get_center()
#         x1, y1 = b2.get_center()
#         plt.plot([x0, x1], [y0, y1], "g" if r > 0.5 else "r")

#     plt.subplot(1, 2, 2)
#     ax2.set_xticks([])  # Remove x-axis ticks
#     ax2.set_yticks([])  # Remove y-axis ticks
#     img.show()
    
#     model.page_units[-1].sub_model.show(with_label=class_)

# plot_file(args.i)
# plt.show()

class ImageViewer:
    def __init__(self, start_ind):
        self.current_index = start_ind
        self.current_name = None
        self.fig, self.ax = plt.subplots(figsize=(10, 7))
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.show_image()
        
    def show_image(self):
        """Показывает текущее изображение"""
        self.ax.clear()
        
        try:
            json_file = dataset[self.current_index]
            plot_file(json_file)


            self.ax.set_title(f"Изображение {self.current_index + 1} ({json_file['file_name']})")
            self.ax.axis('off')
            plt.tight_layout()
            plt.draw()
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
    
    def on_key_press(self, event):
        """Обработка нажатий клавиш"""
        if event.key == 'right' or event.key == ' ':
            # Следующее изображение
            self.current_index = (self.current_index + 1)
            self.show_image()
            
        elif event.key == 'left':
            # Предыдущее изображение
            self.current_index = (self.current_index - 1)
            self.show_image()
            
        elif event.key == 'escape':
            # Закрыть окно
            plt.close()

# Использование
if __name__ == "__main__":
    # Укажите путь к вашей папке с изображениями
    viewer = ImageViewer(0)
    plt.show()