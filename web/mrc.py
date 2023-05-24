# coding=utf-8

import time

import torch
from torch.utils.data import DataLoader
from transformers import BertTokenizerFast

from dataset.dataset1 import MrcDataset
from dataset.dataset1 import collate_fn
from models.model import MRC_model

from utils.finetuning_argparse import get_argparse
from metric.metric import compute_prediction_checklist

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
def predictfunc(data,model,tokenizer):
    all_start_logits = []
    all_end_logits = []
    all_cls_logits = []

    parser = get_argparse()
    args = parser.parse_args()
    # Dataset & Dataloader
    test_dataset = MrcDataset(args,
                              input=data,
                              tokenizer=tokenizer)

    eval_iter = DataLoader(test_dataset,
                           shuffle=False,
                           batch_size=1,
                           collate_fn=collate_fn,
                           num_workers=0)


    with torch.no_grad():
        for step, batch in enumerate(eval_iter):
            for key in batch.keys():
                batch[key] = batch[key].to(device)
            start_logits_tensor, end_logits_tensor, cls_logits_tensor = model(
                input_ids=batch['all_input_ids'],
                attention_mask=batch['all_attention_mask'],
                token_type_ids=batch['all_token_type_ids']
            )
            ###########

            for idx in range(start_logits_tensor.shape[0]):
                all_start_logits.append(start_logits_tensor.cpu().numpy()[idx])
                all_end_logits.append(end_logits_tensor.cpu().numpy()[idx])
                all_cls_logits.append(cls_logits_tensor.cpu().numpy()[idx])

    all_predictions, all_nbest_json, all_cls_predictions = compute_prediction_checklist(
        eval_iter.dataset.examples,
        eval_iter.dataset.tokenized_examples,
        (all_start_logits, all_end_logits, all_cls_logits),
        True,
        5,
        15,
        0.4
    )
    return all_predictions['test']
if __name__ == '__main__':
    context = "F-22水平面上为高梯形机翼搭配一体化尾翼的综合气动力外型，包括彼此隔开很宽和并朝外倾斜的带方向舵型垂直尾翼，且水平安定面直接靠近机翼布置。按照技术标准（小反射外形、吸收无线电波材料、用无线电电子对抗器材和小辐射无线电电子设备装备战斗机，其设计最小雷达反射面为0.005～0.01平方米左右）。在结构上还广泛使用热加工塑胶（12%）和人造纤维（10%）的聚合复合材料（KM）。在量产型上使用复合材料（KM）的比例（按重量）更将达35%。"
    question = "F-22的雷达反射面积是多少"
    title = "F-22"
    core = {'qas': [{'question': question, 'id': 'test'}], 'context': context, 'title': title}
    testdata = [{'title': '', 'paragraphs': [core]}]

    tokenizer = BertTokenizerFast.from_pretrained("bert-base-chinese")
    fine_tunning_model = "output/best_model.pkl"
    model = MRC_model("bert-base-chinese")
    model.to(device)
    model.load_state_dict(torch.load(fine_tunning_model))
    model.eval()
    start=time.perf_counter()
    print(predictfunc(testdata,model,tokenizer))
    print(time.perf_counter()-start)




