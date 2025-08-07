import os 
from pager.page_model.sub_models import JsonWithFeatchs
from pager.page_model.sub_models.dtype import ImageSegment
from .pager_models import featch_rows, featch_A, nodes_feature,edges_feature


def true_class_from_publaynet(blocks, rows, A):
    # Вспомогательные функции
    def get_block_seg(json_block):
        seg = ImageSegment(dict_p_size=json_block)
        seg.add_info("label", json_block["label"])
        return seg
    def get_word_seg(json_row):
        return ImageSegment(dict_2p=json_row['segment'])
    
    def is_one_block(seg1, seg2, blocks):
        for block in blocks:
            if block.is_intersection(seg1) and block.is_intersection(seg2):
                return 1
        return 0
    
    def get_class_node(row, blocks):
        if row.height > 20: #TODO: есть большие строки!!!!
            return -1
        for block in blocks:
            if block.is_intersection(row):
                return block.get_info("label")
        
        return -1
    
    # Получение верных меток из датасета PubLayNet
    block_segs = [get_block_seg(bl) for bl in blocks]
    row_segs = [get_word_seg(r) for r in rows]
    edges_ind = [is_one_block(row_segs[i],row_segs[j], block_segs) for i, j in zip(A[0], A[1])]
    nodes_ind = [get_class_node(r, block_segs) for r in row_segs]
    return [edges_ind, nodes_ind]

def extract(path_dataset, path_img_publaynet=None, path_pdf_publaynet=None):
    json_with_featchs = JsonWithFeatchs()
    files = os.listdir(path_dataset)
    N = len(files)
    for i, file in enumerate(files):
        print(file, end=' ')
        try:
            path_json = os.path.join(path_dataset, file)
            json_with_featchs.read_from_file(path_json)
            path_pdf = os.path.join(path_pdf_publaynet, json_with_featchs.json['file_name'][:-4]+'.pdf')
            json_with_featchs.add_featchs(lambda: featch_rows(path_pdf), names=[ 'rows'], 
                                is_reupdate=False, rewrite=True)
            json_with_featchs.add_featchs(lambda: featch_A(json_with_featchs.json['rows']), names=['A'], 
                                is_reupdate=True, rewrite=True)
            json_with_featchs.add_featchs(lambda: nodes_feature(json_with_featchs.json['rows']), names=['nodes_feature'], 
                                is_reupdate=False, rewrite=True) 
            json_with_featchs.add_featchs(lambda: edges_feature(json_with_featchs.json['A'], json_with_featchs.json['rows']), names=['edges_feature'], 
                                is_reupdate=True, rewrite=True)
            json_with_featchs.add_featchs(lambda: true_class_from_publaynet(json_with_featchs.json['blocks'], json_with_featchs.json['rows'], json_with_featchs.json['A']), names=["true_edges", "true_nodes"], 
                                is_reupdate=True, rewrite=True)
            
        except:
            print("error in ", file)
        
        print(f" ({(i+1)/N*100:.2f} %) "+20*" ", end='\n')  