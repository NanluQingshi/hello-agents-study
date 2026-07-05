'''
Author: NanluQingshi
Date: 2026-07-05 15:27:09
LastEditors: NanluQingshi
LastEditTime: 2026-07-05 15:27:21
Description: BPE 算法，字节对编码
'''
import re                           # re 模块：正则表达式，用于字符串匹配和替换
import collections                  # collections 模块：提供 defaultdict 等额外数据结构


def get_stats(vocab):
    """
    统计词元对（相邻两个子词）的出现频率。

    参数 vocab: dict，格式如 {"h u g </w>": 1, ...}
                键是空格分隔的子词序列（字符串），值是它在语料中的出现次数。
    返回值:     dict（defaultdict），键是 (子词A, 子词B) 元组，值是它们相邻出现的总频次。
    """
    # collections.defaultdict(int) 创建一个"默认字典"：访问不存在的键时自动赋默认值 0
    # 效果等同于普通 dict + 手动判断键是否存在，但更简洁
    pairs = collections.defaultdict(int)

    # .items() 以 (键, 值) 元组的形式遍历字典
    # 这里 word = "h u g </w>", freq = 1
    for word, freq in vocab.items():
        # str.split() 默认按空白字符（空格、制表符等）切分字符串
        # symbols = ["h", "u", "g", "</w>"]
        symbols = word.split()

        # range(len(symbols)-1) 生成 [0, 1, 2]（共 4 个符号，最后一对索引是 2→3）
        # 遍历所有相邻位置，提取相邻符号对
        for i in range(len(symbols) - 1):
            # symbols[i] 和 symbols[i+1] 构成一对相邻子词
            # 例如 ("h", "u")、("u", "g")、("g", "</w>")
            # pairs[("h", "u")] += 1   ← 因为 freq=1，所以加的是这个词的频次
            pairs[symbols[i], symbols[i+1]] += freq

    return pairs


def merge_vocab(pair, v_in):
    """
    合并词表中指定的一对相邻子词，生成新词表。

    参数 pair: tuple (子词A, 子词B)，要合并的目标对
    参数 v_in: dict，旧词表
    返回值:    dict，合并后的新词表（词频保持不变）
    """
    v_out = {}  # 空字典，用来存放合并后的结果

    # 将 pair 里的两个字符串用空格拼起来，再用 re.escape() 转义特殊字符
    # 例如 pair = ("u", "g") → bigram = "u g"（空格刚好是原来的分隔符）
    bigram = re.escape(' '.join(pair))

    # 编译正则表达式：(?<!\S) 表示"前面不能是非空白字符"（即必须是词边界）
    # (?!\S) 表示"后面不能是非空白字符"
    # 合起来就是精确匹配整个"u g"，不匹配某个更长词的一部分
    # 例如在 "x u g x" 中，u g 前后有空格，所以能匹配
    p = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')

    # 遍历旧词表的每个词（键）
    for word in v_in:
        # p.sub(替换成什么, 在哪个字符串里替换)
        # 把 word 中所有匹配的 "u g" 替换成 "ug"（去掉空格，合并成一个子词）
        # sub = substitute（替换）
        w_out = p.sub(''.join(pair), word)

        # 将合并后的词和原来的频次存入新字典
        # 注意：词频不变，因为合并只是改变词的写法，不改变它出现了多少次
        v_out[w_out] = v_in[word]

    return v_out


# ========== 准备语料库 ==========
# 每个字符串是一个词，末尾加上 </w> 表示"词的结束"（这个符号本身作为一个子词）
# 每个字符之间用空格隔开，表示初始时每个字符都是一个独立的子词（token）
# 冒号右边是该词在语料中的出现次数（频次）
vocab = {
    'h u g </w>': 1,   # 单词 "hug" 出现 1 次
    'p u g </w>': 1,   # 单词 "pug" 出现 1 次
    'p u n </w>': 1,   # 单词 "pun" 出现 1 次
    'b u n </w>': 1,   # 单词 "bun" 出现 1 次
}

num_merges = 4  # 设置迭代合并次数（BPE 的核心超参数）

# ========== 主循环：迭代执行 BPE 合并 ==========
for i in range(num_merges):     # range(4) → i = 0, 1, 2, 3，共循环 4 次
    pairs = get_stats(vocab)    # 统计当前词表中所有相邻子词对的频次

    # 如果没有相邻对了（每个词都只剩一个子词），提前退出循环
    if not pairs:               # not 对空字典判定为 True
        break

    # max(字典, key=字典.get) 的意思是：遍历字典的键，用 字典.get(键) 的值作为比较依据
    # 返回"值最大"的那个键，即出现频次最高的子词对
    best = max(pairs, key=pairs.get)

    # 用最高频的子词对去合并整个词表，生成新词表
    vocab = merge_vocab(best, vocab)

    # 打印本次合并的信息
    # f-string（格式化字符串）：花括号 { } 内放变量或表达式，运行时自动替换
    # .join(list) 将列表中的元素用指定字符串连接，这里用空字符串 ''.join(...) 表示直接拼起来
    print(f"第{i+1}次合并: {best} -> {''.join(best)}")

    # 打印当前词表的所有键（合并后的词）
    # list(dict.keys()) 获取所有键并转成列表，方便查看
    print(f"新词表（部分）: {list(vocab.keys())}")
    print("-" * 20)  # 打印 20 个横线，作为分隔

