"""
题目: 复原 IP 地址
LeetCode: #93 (Medium)
高频公司: 字节跳动、腾讯

题目描述:
有效 IP 地址正好由四个整数（每个整数位于 0 到 255 之间组成，且不能含有前导 0），
整数之间用 '.' 分隔。
给定一个只包含数字的字符串 s，用以表示一个 IP 地址，
返回所有可能从 s 获得的 有效 IP 地址。你可以按任何顺序返回答案。

示例 1: s = "25525511135" -> ["255.255.11.135","255.255.111.35"]
示例 2: s = "0000" -> ["0.0.0.0"]
示例 3: s = "1111111111111111" -> []（太长）

IP 地址段规则：
- 每段 1-3 位数字
- 每段值在 0-255 之间
- 不能有前导零（"01" "00" 不合法，"0" 合法）

================================================================================
TL;DR（核心思路）:
- 回溯：每次截取 1-3 位，合法则加入路径，递归处理剩余字符串
- 终止：path 中有 4 段且字符串恰好用完
- 剪枝：
  * 剩余字符长度不在合理范围 [segments_left, segments_left * 3] 内则跳过
  * 当前段超过 255 或有前导零则跳过

时间复杂度: O(3^4) = O(81)，每次最多取3位，最多4段，近似常数
空间复杂度: O(4) 递归深度
================================================================================
"""

from typing import List


def restoreIpAddresses(s: str) -> List[str]:
    """
    回溯：逐段切割，合法则递归，找到4段且用完字符串则记录。
    """
    result = []

    def is_valid_segment(seg: str) -> bool:
        """判断一个 IP 段是否合法：无前导零，值在 [0, 255]"""
        if len(seg) > 1 and seg[0] == '0':  # 前导零（"01", "001" 等不合法）
            return False
        return 0 <= int(seg) <= 255

    def backtrack(start: int, path: List[str]):
        # 找到 4 段且字符串用完
        if len(path) == 4:
            if start == len(s):
                result.append(".".join(path))
            return

        remaining_segments = 4 - len(path)
        remaining_chars = len(s) - start

        # 剪枝：剩余字符太少或太多
        if remaining_chars < remaining_segments or remaining_chars > remaining_segments * 3:
            return

        # 尝试取 1、2、3 位
        for length in range(1, 4):
            if start + length > len(s):
                break
            seg = s[start:start + length]
            if is_valid_segment(seg):
                path.append(seg)
                backtrack(start + length, path)
                path.pop()

    backtrack(0, [])
    return result


def restoreIpAddresses_iterative(s: str) -> List[str]:
    """
    三层循环枚举三个分隔点（等价思路，更直观）：
    将字符串分成 4 段：s[0:a], s[a:b], s[b:c], s[c:]
    """
    n = len(s)
    result = []

    def valid(seg):
        if len(seg) > 1 and seg[0] == '0':
            return False
        return 1 <= len(seg) <= 3 and 0 <= int(seg) <= 255

    for a in range(1, 4):
        for b in range(a + 1, a + 4):
            for c in range(b + 1, b + 4):
                if c >= n:
                    break
                seg1, seg2, seg3, seg4 = s[:a], s[a:b], s[b:c], s[c:]
                if valid(seg1) and valid(seg2) and valid(seg3) and valid(seg4):
                    result.append(f"{seg1}.{seg2}.{seg3}.{seg4}")

    return result


# ============================================================
# 测试
# ============================================================
if __name__ == "__main__":
    # 基础测试
    r1 = sorted(restoreIpAddresses("25525511135"))
    assert r1 == sorted(["255.255.11.135","255.255.111.35"]), f"got {r1}"

    r2 = restoreIpAddresses("0000")
    assert r2 == ["0.0.0.0"], f"got {r2}"

    r3 = restoreIpAddresses("1111111111111111")
    assert r3 == [], "太长，无解"

    r4 = restoreIpAddresses("101023")
    assert sorted(r4) == sorted(["1.0.10.23","1.0.102.3","10.1.0.23","10.10.2.3","101.0.2.3"]), f"got {r4}"

    # 边界
    assert restoreIpAddresses("1") == []          # 太短
    assert restoreIpAddresses("1234567890123") == []  # 太长
    assert restoreIpAddresses("1111") == ["1.1.1.1"]
    assert restoreIpAddresses("010010") is not None  # 含0的情况

    # 两种实现结果一致
    test_strs = ["25525511135", "0000", "101023", "11111111"]
    for s in test_strs:
        r_back = sorted(restoreIpAddresses(s))
        r_iter = sorted(restoreIpAddresses_iterative(s))
        assert r_back == r_iter, f"两种实现不一致: s={s}, back={r_back}, iter={r_iter}"

    print("所有测试通过!")

    print(f"\n示例结果:")
    print(f"'25525511135' -> {restoreIpAddresses('25525511135')}")
    print(f"'0000'        -> {restoreIpAddresses('0000')}")
    print(f"'101023'      -> {restoreIpAddresses('101023')}")
    print(f"'1111'        -> {restoreIpAddresses('1111')}")
