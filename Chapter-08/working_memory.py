class WorkingMemory:
    """工作记忆实现

    模拟人类「短期记忆」，存放最近、最相关的少量上下文。

    特点：
    - 容量有限（默认50条）+ TTL自动清理：既控制内存占用，又保证记忆新鲜
    - 纯内存存储，访问速度极快：适合 Agent 每轮对话都要读取的高频场景
    - 混合检索：TF-IDF向量化（抓语义） + 关键词匹配（抓精确命中）
    """

    def __init__(self, config: MemoryConfig):
        """初始化工作记忆

        Args:
            config: 记忆配置对象，提供容量与 TTL 参数
        """
        # 最大容量：超过则按优先级淘汰最低的一条（config 未配置时默认 50）
        self.max_capacity = config.working_memory_capacity or 50
        # 记忆过期时间（分钟）：超过该时长的记忆在下次操作时被清理（默认 60 分钟）
        self.max_age_minutes = config.working_memory_ttl or 60
        # 记忆列表：按插入顺序存储，检索时再动态评分排序
        self.memories = []

    def add(self, memory_item: MemoryItem) -> str:
        """添加一条工作记忆

        写入前做两件事：先清理过期记忆，再在超容量时淘汰优先级最低的一条。
        这样保证插入后总条数始终 <= max_capacity。

        Args:
            memory_item: 待写入的记忆条目

        Returns:
            该记忆的唯一 ID（用于后续 update/remove/检索定位）
        """
        # 1. 过期清理：先把超过 TTL 的旧记忆删掉，腾出空间
        self._expire_old_memories()  # 过期清理

        # 2. 容量管理：若清理后仍满，则淘汰优先级最低的一条
        if len(self.memories) >= self.max_capacity:
            self._remove_lowest_priority_memory()  # 容量管理

        # 3. 追加新记忆并返回其 ID
        self.memories.append(memory_item)
        return memory_item.id

    def retrieve(self, query: str, limit: int = 5, **kwargs) -> List[MemoryItem]:
        """混合检索：TF-IDF向量化 + 关键词匹配

        评分总公式（三因子相乘）：
            final_score = base_relevance × time_decay × importance_weight

        - 用「乘法」而非「加法」：任一因子为 0 即整体为 0，
          可自然淘汰「完全不相关」或「完全过期」的记忆。

        Args:
            query: 查询文本
            limit: 返回的最大条数，默认 5
            **kwargs: 预留扩展参数（如阈值过滤、类型筛选等）

        Returns:
            按分数降序排列的前 limit 条记忆
        """
        # 检索前先清理过期记忆，避免召回已失效内容
        self._expire_old_memories()

        # 第一步：批量做 TF-IDF 向量检索，拿到每条记忆的语义相似度分数
        # 返回 {memory_id: vector_score} 字典；无索引或 query 过短时可能返回空
        vector_scores = self._try_tfidf_search(query)

        # 第二步：逐条计算综合分数
        scored_memories = []
        for memory in self.memories:
            # —— 因子①：相关度 base_relevance ——
            # 取本条的向量分（没有则 0）
            vector_score = vector_scores.get(memory.id, 0.0)
            # 关键词匹配分：字面命中度，通常基于词频/覆盖率
            keyword_score = self._calculate_keyword_score(query, memory.content)

            # 混合评分：向量分>0 时按 7:3 加权融合（向量主导语义，关键词补精确命中）；
            # 否则退化为仅用关键词分，保证没有索引也能检索
            base_relevance = vector_score * 0.7 + keyword_score * 0.3 if vector_score > 0 else keyword_score

            # —— 因子②：时间衰减 time_decay ——
            # 记忆越旧值越小（通常 0~1），模拟「近期记得清、远期模糊」
            time_decay = self._calculate_time_decay(memory.timestamp)

            # —— 因子③：重要性加权 importance_weight ——
            # importance∈[0,1] → 权重∈[0.8, 1.2]
            #   importance=0   → 0.8（轻度下调，但不清零）
            #   importance=0.5 → 1.0（中性，不影响）
            #   importance=1   → 1.2（最多放大 20%）
            # 设计意图：重要性只做微调，不喧宾夺主，相关度仍是主导
            importance_weight = 0.8 + (memory.importance * 0.4)

            # 最终分数：三因子相乘
            final_score = base_relevance * time_decay * importance_weight
            # 只保留有分数的记忆（=0 的意味着既不相关又过期，直接丢弃）
            if final_score > 0:
                scored_memories.append((final_score, memory))

        # 第三步：按分数降序排序，取前 limit 条
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        return [memory for _, memory in scored_memories[:limit]]
