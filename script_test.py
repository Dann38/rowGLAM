from config import PATH_TEST_DATASET, PATH_TEST_IMAGES, PATH_TEST_JSON, PATH_TEST_PDF, get_final_model,EXPERIMENT
from pager.benchmark.seg_detection.seg_detection_word_IoU import  SegDetectionBenchmark

# from pager import PageModel, PageModelUnit, PDFModel, WordsModel, PhisicalModel, PDF2Words, Words2OneBlock
# page = PageModel([
#     PageModelUnit("pdf", PDFModel({"method":"w"}), extractors=[], converters={}),
#     PageModelUnit("words", WordsModel(), extractors=[], converters={"pdf": PDF2Words()}),
#     PageModelUnit("phis", PhisicalModel(), extractors=[], converters={"words": Words2OneBlock()}),
# ])

page = get_final_model()
benchmark = SegDetectionBenchmark(path_dataset=PATH_TEST_DATASET,
                    page_model=page,
                    path_images=PATH_TEST_IMAGES, 
                    path_pdfs=PATH_TEST_PDF,
                    path_json=PATH_TEST_JSON,
                    # save_dir="save_dir3",
                    only_seg=True,
                    count_image=50,
                    name=EXPERIMENT)

import shutil
import os
shutil.move(benchmark.name + ".txt", os.path.join(EXPERIMENT, "test_result.txt"))