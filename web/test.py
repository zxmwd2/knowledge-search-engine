from transformers import XLNetTokenizer, GPT2LMHeadModel
from transformers import TextGenerationPipeline
import jieba
#add spicel process
class XLNetTokenizer(XLNetTokenizer):
    translator = str.maketrans(" \n", "\u2582\u2583")
    def _tokenize(self, text, *args, **kwargs):
        text = [x.translate(self.translator) for x in jieba.cut(text, cut_all=False)]
        text = " ".join(text)
        return super()._tokenize(text, *args, **kwargs)
    def _decode(self, *args, **kwargs):
        text = super()._decode(*args, **kwargs)
        text = text.replace(' ', '').replace('\u2582', ' ').replace('\u2583', '\n')
        return text

tokenizer = XLNetTokenizer.from_pretrained('mymusise/CPM-Generate-distill')
model = GPT2LMHeadModel.from_pretrained("mymusise/CPM-Generate-distill")

text_generater = TextGenerationPipeline(model, tokenizer)

print(text_generater("f-22是第五代隐身战斗机，其设计最小雷达反射面为0.005～0.01平方米左右）。f-22的雷达反射截面积是", max_length=50, top_k=1, use_cache=True, prefix=''))
#
# from transformers import TextGenerationPipeline, AutoTokenizer, AutoModelWithLMHead
#
# tokenizer = AutoTokenizer.from_pretrained("TsinghuaAI/CPM-Generate")
# model = AutoModelWithLMHead.from_pretrained("TsinghuaAI/CPM-Generate")
#
# text_generator = TextGenerationPipeline(model, tokenizer)
# text_generator('清华大学', max_length=50, do_sample=True, top_p=0.9)

# from transformers import BertTokenizer, BartForConditionalGeneration, Text2TextGenerationPipeline
# tokenizer = BertTokenizer.from_pretrained("fnlp/bart-base-chinese")
# model = BartForConditionalGeneration.from_pretrained("fnlp/bart-base-chinese")
# text2text_generator = Text2TextGenerationPipeline(model, tokenizer)
# print(text2text_generator("f-22是第五代隐身战斗机，其设计最小雷达反射面为0.005～0.01平方米左右）。f-22的雷达反射截面积是[MASK]", max_length=50, do_sample=True))
#
