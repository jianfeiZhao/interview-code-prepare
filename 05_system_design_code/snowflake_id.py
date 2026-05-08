"""
题目：雪花算法（Snowflake ID 生成器）
难度：Medium | 高频出现：字节/阿里/美团（后端岗）
标签：分布式ID、Snowflake、系统设计


题目描述
---------
设计并实现雪花算法（Snowflake ID Generator），生成全局唯一的 64 位分布式 ID。
雪花 ID 由以下部分组成：
  - 1 bit：符号位（固定为 0）
  - 41 bit：毫秒时间戳（相对于纪元，可使用约 69 年）
  - 10 bit：机器/节点 ID（5 bit 数据中心 + 5 bit 工作机器）
  - 12 bit：毫秒内序列号（每毫秒最多生成 4096 个 ID）

接口设计：
  - next_id() → int：生成下一个唯一 ID（趋势递增）

示例
------
gen = SnowflakeID(worker_id=1, datacenter_id=1)
id1 = gen.next_id()  # 64 位整数，全局唯一
id2 = gen.next_id()  # id2 > id1（趋势递增）

约束
------
- 需处理时钟回拨问题
- 同毫秒内序列号溢出时等待到下一毫秒

TL;DR（30秒速览）
- 64 bit ID = 1bit符号位 + 41bit时间戳 + 10bit机器ID + 12bit序列号
- 每毫秒每台机器最多生成 4096 个 ID（2^12）
- 趋势递增，适合数据库索引；全局唯一；高性能无锁（单机）

详细解析
---------
ID 结构（64 bit）：
  bit[63]：符号位，固定 0
  bit[22-62]（41位）：毫秒时间戳，可用 69 年
  bit[12-21]（10位）：机器/节点 ID（5位数据中心 + 5位机器）
  bit[0-11]（12位）：毫秒内序列号，每毫秒可生成 4096 个

时钟回拨问题：
  系统时钟可能回拨（NTP校时），导致 ID 重复
  解决：检测回拨，等待时间追上，或记录最大 timestamp 拒绝回拨
"""

import time
import threading


class SnowflakeID:
    # 各段位数
    WORKER_ID_BITS = 5
    DATACENTER_ID_BITS = 5
    SEQUENCE_BITS = 12

    # 最大值
    MAX_WORKER_ID = (1 << WORKER_ID_BITS) - 1       # 31
    MAX_DATACENTER_ID = (1 << DATACENTER_ID_BITS) - 1  # 31
    MAX_SEQUENCE = (1 << SEQUENCE_BITS) - 1           # 4095

    # 位移量
    WORKER_SHIFT = SEQUENCE_BITS                      # 12
    DATACENTER_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS  # 17
    TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS  # 22

    # 起始纪元（2024-01-01 00:00:00 UTC，单位ms）
    EPOCH = 1704067200000

    def __init__(self, worker_id: int = 0, datacenter_id: int = 0):
        assert 0 <= worker_id <= self.MAX_WORKER_ID
        assert 0 <= datacenter_id <= self.MAX_DATACENTER_ID
        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = 0
        self.last_timestamp = -1
        self._lock = threading.Lock()

    def _current_ms(self) -> int:
        return int(time.time() * 1000)

    def _wait_next_ms(self, last_ts: int) -> int:
        ts = self._current_ms()
        while ts <= last_ts:
            ts = self._current_ms()
        return ts

    def next_id(self) -> int:
        with self._lock:
            ts = self._current_ms()

            if ts < self.last_timestamp:
                # 时钟回拨，等待追上
                ts = self._wait_next_ms(self.last_timestamp)

            if ts == self.last_timestamp:
                # 同一毫秒内，序列号递增
                self.sequence = (self.sequence + 1) & self.MAX_SEQUENCE
                if self.sequence == 0:
                    # 序列号溢出，等待下一毫秒
                    ts = self._wait_next_ms(self.last_timestamp)
            else:
                self.sequence = 0

            self.last_timestamp = ts

            return (
                ((ts - self.EPOCH) << self.TIMESTAMP_SHIFT)
                | (self.datacenter_id << self.DATACENTER_SHIFT)
                | (self.worker_id << self.WORKER_SHIFT)
                | self.sequence
            )

    @staticmethod
    def parse(snowflake_id: int) -> dict:
        """解析 Snowflake ID 各字段"""
        sequence       = snowflake_id & 0xFFF
        worker_id      = (snowflake_id >> 12) & 0x1F
        datacenter_id  = (snowflake_id >> 17) & 0x1F
        timestamp_ms   = (snowflake_id >> 22) + SnowflakeID.EPOCH
        return {
            'timestamp_ms': timestamp_ms,
            'datacenter_id': datacenter_id,
            'worker_id': worker_id,
            'sequence': sequence,
        }


if __name__ == "__main__":
    gen = SnowflakeID(worker_id=1, datacenter_id=0)

    ids = [gen.next_id() for _ in range(1000)]

    # 唯一性
    assert len(set(ids)) == 1000, "IDs should be unique"

    # 递增性（趋势）
    assert ids == sorted(ids), "IDs should be roughly increasing"

    # 解析验证
    info = SnowflakeID.parse(ids[0])
    assert info['worker_id'] == 1
    assert info['datacenter_id'] == 0
    assert info['sequence'] == 0

    # 线程安全
    gen2 = SnowflakeID(worker_id=2)
    results = []
    def generate_ids():
        for _ in range(100):
            results.append(gen2.next_id())
    threads = [threading.Thread(target=generate_ids) for _ in range(10)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert len(set(results)) == 1000, "Thread-safe ID generation failed"

    print(f"Sample ID: {ids[0]}")
    print(f"Parsed: {info}")
    print("All tests passed.")
