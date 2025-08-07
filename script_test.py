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
                  #   save_dir="save_dir4",
                    only_seg=True,
                    count_image=50,
                    name=EXPERIMENT,
                    exceptions=[
                       "3973168_00001",
                       "4077548_00001",
                       "4198678_00002",
                       "4210625_00005",
                       "4331841_00002",
                       "4349706_00004",
                       "4349706_00004",
                       "4399148_00004",
                       "4477602_00003",
                       "4504036_00003",
                       "4648845_00001",
                       "4857225_00008",
                       "4995603_00004",
                       "5104805_00007",
                       "5121155_00005",
                       "5430366_00008",
                       "5430370_00005",
                       "5615323_00004",
                       "5748559_00007",
                       "5758854_00003",
                       "5874891_00007",

                    ])

import shutil
import os
shutil.move(benchmark.name + ".txt", os.path.join(EXPERIMENT, "test_result.txt"))